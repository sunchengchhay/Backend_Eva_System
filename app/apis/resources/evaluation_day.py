from app.apis.models.committee import output_eve_committee_score
from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import func, desc
from collections import defaultdict


from app.customs.authorizations import authorizations
from app.extensions import db
from app.apis.models import *
from app.models import *

ns = Namespace("Evaluation Day Managements",
               description="Evaluation day Management endpoints", path="/", authorizations=authorizations)

ns.decorators = [jwt_required()]


@ns.route('/events/<int:eid>/evaluation-forms/eve-project-id/<int:shid>')
class EveEvalForm(Resource):

    @ns.doc(security='jsonWebToken')
    @ns.marshal_with(output_eve_eval_category_forms)
    def get(self, eid, shid):
        try:
            result = db.session.query(
                EveEvalCategory.id.label('category_id'),
                EveEvalCategory.name_latin,
                EveEvalCategory.weight,
                EveEvalCriteria.id.label('criteria_id'),
                EveEvalCriteria.name_latin.label('criteria_name'),
                EveEvalCriteriaRubric.score.label('criteria_score')
            ).join(
                EveEvalCriteria, EveEvalCategory.id == EveEvalCriteria.eve_eval_category_id
            ).join(
                EveEvalCriteriaRubric, EveEvalCriteria.id == EveEvalCriteriaRubric.eve_eval_criteria_id
            ).filter(
                EveEvalCategory.eve_event_id == eid
            ).order_by(
                EveEvalCriteriaRubric.id.asc()
            ).all()

            if result:
                eve_project_shortlist = EveProjectShortlist.query.filter_by(
                    id=shid).first()

                if eve_project_shortlist:
                    # Initialize a dictionary to structure the data
                    data = {
                        'category': {},
                    }

                    # Iterate through the query results and organize the data
                    for row in result:
                        category_id = row.category_id
                        category_name = row.name_latin
                        category_weight = row.weight
                        criteria_id = row.criteria_id
                        criteria_name = row.criteria_name
                        criteria_score = row.criteria_score

                        if category_name not in data['category']:
                            data['category'][category_name] = {
                                'id': category_id, 'name': category_name, 'weight': category_weight, 'criteria': []}

                        if criteria_name not in {c['name'] for c in data['category'][category_name]['criteria']}:
                            data['category'][category_name]['criteria'].append(
                                {'id': criteria_id, 'name': criteria_name, 'score': []})

                        current_criteria = next(
                            c for c in data['category'][category_name]['criteria'] if c['id'] == criteria_id)
                        current_criteria['score'].append(criteria_score)

                    # Convert the data to the desired JSON format
                    result_json = {
                        'category': list(data['category'].values()),
                        'project_code': eve_project_shortlist.eve_project.code,
                        'project_topic': eve_project_shortlist.eve_project.topic
                    }

                return result_json, 200
            return {"msg": "not found"}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong!'}, 500


@ns.route('/events/<int:eid>/departments/<int:did>')
class EveGenYear(Resource):

    @ns.doc(security='jsonWebToken')
    @ns.marshal_with(output_eve_generation_model)
    def get(self, eid, did):
        try:
            eve_gen = EveGeneration.query.filter_by(
                sys_department_id=did, eve_event_id=eid).all()
            if eve_gen:
                return eve_gen, 200
            return {"msg": "not found"}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong!'}, 500


@ns.route('/events/<int:eid>/departments/<int:did>/years/<string:year>/eve_project_shortlists/<int:shid>')
class EveProjectDetials(Resource):
    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(output_custom_project_shortlist_model)
    def get(self, eid, did, year, shid):
        try:
            results = db.session.query(
                EveProjectShortlist.id.label('eve_project_shortlist_id'),
                EveEvent.name_latin.label('eve_event_name'),
                EveProjectType.name_latin.label('eve_project_type'),
                EveCommittee.id.label('eve_project_committee_id'),
                EveGeneration.name_latin.label('eve_project_generation'),
                EveGeneration.year.label('eve_project_year'),
                SysDepartment.name_latin.label('department'),
                SysPerson.name_latin.label('eve_project_committee_name'),
                EveProject.id.label('eve_project_id'),
                EveProject.code.label('eve_project_code'),
                EveProject.topic.label('eve_project_topic'),
                EveSupervisor.name_latin.label('eve_project_supervisor_name')
            )\
                .join(EveProject, (EveProject.id == EveProjectShortlist.eve_project_id) & (EveProject.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectType, (EveProjectShortlist.eve_project_type_id == EveProjectType.id) & (EveProjectType.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectCommittee, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id)\
                .join(EveEvent, EveEvent.id == EveProjectShortlist.eve_event_id)\
                .join(EveSupervisor, EveProject.eve_supervisor_id == EveSupervisor.id)\
                .join(EveCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id)\
                .join(SysPerson, SysPerson.id == EveCommittee.sys_person_id)\
                .join(EveGeneration, (EveGeneration.year == year) & (EveGeneration.sys_department_id == EveProject.sys_department_id) & (EveGeneration.id == EveProject.eve_generation_id) & (EveGeneration.sys_department_id == did))\
                .join(SysDepartment, SysDepartment.id == EveGeneration.sys_department_id)\
                .filter(EveProjectShortlist.eve_event_id == eid, EveProjectShortlist.id == shid)\
                .group_by(
                    EveProjectShortlist.id,
                    EveEvent.name_latin,
                    EveProjectType.name_latin,
                    EveCommittee.id,
                    EveGeneration.name_latin,
                    EveGeneration.year,
                    SysDepartment.name_latin,
                    SysPerson.name_latin,
                    EveProject.id,
                    EveProject.code,
                    EveProject.topic,
                    EveSupervisor.name_latin
            ).order_by(EveProjectShortlist.id.asc()).all()

            projects = []
            group = None

            for row in results:
                eve_committee_score = EveCommitteeScore.query.filter_by(
                    eve_committee_id=row.eve_project_committee_id, eve_project_shortlist_id=row.eve_project_shortlist_id).count()
                total_score = db.session.query(func.coalesce(func.sum(EveCommitteeScore.score), 0)).filter(
                    EveCommitteeScore.eve_project_shortlist_id == row.eve_project_shortlist_id,
                    EveCommitteeScore.eve_committee_id == row.eve_project_committee_id
                ).scalar()

                if group is None or row.eve_project_shortlist_id != group['eve_shortlist_id']:
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=row.eve_project_shortlist_id).first()

                    if group is not None:
                        projects.append(group)

                    # Create a new group for a new project
                    if eve_result:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': eve_result.total_score,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                    else:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': 0,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                else:
                    if eve_committee_score and eve_committee_score == 9:
                        # Append committee data to the eve_project_committee list
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': True,
                            'project_score': total_score
                        })
                    else:
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': False,
                            'project_score': total_score
                        })

                members = []
                eve_project_members = EveProjectMember.query.filter_by(
                    eve_event_id=eid, eve_project_id=row.eve_project_id).all()

                for member in eve_project_members:
                    members.append({
                        'id': member.id,
                        'name_latin': member.name_latin,
                        'name_khmer': member.name_khmer,
                        'sys_gender': {
                            'id': member.sys_gender.id,
                            'name_latin': member.sys_gender.name_latin
                        }
                    })

                group['eve_project_members'] = members

            # Append the last group after the loop
            if group:
                projects.append(group)

            return projects, 200
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong!!"}, 500


# all projects
@ns.route('/events/eve-projects')
class EveAllProjectShortlist(Resource):
    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(output_custom_project_shortlist_model)
    def get(self):
        """Get all Project Shortlists"""
        try:
            results = db.session.query(
                EveProjectShortlist.id.label('eve_project_shortlist_id'),
                EveEvent.name_latin.label('eve_event_name'),
                EveProjectType.name_latin.label('eve_project_type'),
                SysDepartment.name_latin.label('department'),
                EveCommittee.id.label('eve_project_committee_id'),
                SysPerson.name_latin.label('eve_project_committee_name'),
                EveGeneration.name_latin.label('eve_project_generation'),
                EveGeneration.year.label('eve_project_year'),
                EveProject.id.label('eve_project_id'),
                EveProject.code.label('eve_project_code'),
                EveProject.topic.label('eve_project_topic'),
                EveSupervisor.name_latin.label('eve_project_supervisor_name')
            ).join(EveProject, (EveProject.id == EveProjectShortlist.eve_project_id) & (EveProject.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectType, (EveProjectShortlist.eve_project_type_id == EveProjectType.id) & (EveProjectType.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectCommittee, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id)\
                .join(EveEvent, EveEvent.id == EveProjectShortlist.eve_event_id)\
                .join(EveSupervisor, EveProject.eve_supervisor_id == EveSupervisor.id)\
                .join(EveCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id)\
                .join(SysPerson, SysPerson.id == EveCommittee.sys_person_id)\
                .join(EveGeneration, (EveGeneration.sys_department_id == EveProject.sys_department_id) & (EveGeneration.id == EveProject.eve_generation_id))\
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)\
                .filter(EveProjectShortlist.eve_event_id == 1)\
                .group_by(
                EveProjectShortlist.id,
                EveEvent.name_latin,
                EveProjectType.name_latin,
                SysDepartment.name_latin,
                SysPerson.name_latin,
                EveCommittee.id,
                EveGeneration.year,
                EveGeneration.name_latin,
                EveProject.id,
                EveProject.code,
                EveProject.topic,
                EveSupervisor.name_latin
            ).order_by(EveProjectShortlist.id.asc()).all()

            projects = []
            group = None

            for row in results:
                eve_committee_score = EveCommitteeScore.query.filter_by(
                    eve_committee_id=row.eve_project_committee_id, eve_project_shortlist_id=row.eve_project_shortlist_id).count()
                total_score = db.session.query(func.coalesce(func.sum(EveCommitteeScore.score), 0)).filter(
                    EveCommitteeScore.eve_project_shortlist_id == row.eve_project_shortlist_id,
                    EveCommitteeScore.eve_committee_id == row.eve_project_committee_id
                ).scalar()

                if group is None or row.eve_project_shortlist_id != group['eve_shortlist_id']:
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=row.eve_project_shortlist_id).first()

                    if group is not None:
                        projects.append(group)

                    # Create a new group for a new project
                    if eve_result:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': eve_result.total_score,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                    else:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': 0,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                else:
                    if eve_committee_score and eve_committee_score == 9:
                        # Append committee data to the eve_project_committee list
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': True,
                            'project_score': total_score
                        })
                    else:
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': False,
                            'project_score': total_score
                        })

                members = []
                eve_project_members = EveProjectMember.query.filter_by(
                    eve_event_id=1, eve_project_id=row.eve_project_id).all()

                for member in eve_project_members:
                    members.append({
                        'id': member.id,
                        'name_latin': member.name_latin,
                        'name_khmer': member.name_khmer,
                        'sys_gender': {
                            'id': member.sys_gender.id,
                            'name_latin': member.sys_gender.name_latin
                        }
                    })

                group['eve_project_members'] = members

            # Append the last group after the loop
            if group:
                projects.append(group)

            return projects, 200
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong!!"}, 500


@ns.route('/events/departments/<int:did>/eve-projects')
class EveProjectShortlistByDepartment(Resource):
    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(output_custom_project_shortlist_model)
    def get(self, did):
        """Get all Project Shortlists By Department"""
        try:
            results = db.session.query(
                EveProjectShortlist.id.label('eve_project_shortlist_id'),
                EveEvent.name_latin.label('eve_event_name'),
                EveProjectType.name_latin.label('eve_project_type'),
                SysDepartment.name_latin.label('department'),
                EveCommittee.id.label('eve_project_committee_id'),
                SysPerson.name_latin.label('eve_project_committee_name'),
                EveGeneration.name_latin.label('eve_project_generation'),
                EveGeneration.year.label('eve_project_year'),
                EveProject.id.label('eve_project_id'),
                EveProject.code.label('eve_project_code'),
                EveProject.topic.label('eve_project_topic'),
                EveSupervisor.name_latin.label('eve_project_supervisor_name')
            ).join(EveProject, (EveProject.id == EveProjectShortlist.eve_project_id) & (EveProject.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectType, (EveProjectShortlist.eve_project_type_id == EveProjectType.id) & (EveProjectType.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectCommittee, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id)\
                .join(EveEvent, EveEvent.id == EveProjectShortlist.eve_event_id)\
                .join(EveSupervisor, EveProject.eve_supervisor_id == EveSupervisor.id)\
                .join(EveCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id)\
                .join(SysPerson, SysPerson.id == EveCommittee.sys_person_id)\
                .join(EveGeneration, (EveGeneration.sys_department_id == EveProject.sys_department_id) & (EveGeneration.id == EveProject.eve_generation_id))\
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)\
                .filter(EveProjectShortlist.eve_event_id == 1, SysDepartment.id == did)\
                .group_by(
                EveProjectShortlist.id,
                EveEvent.name_latin,
                EveProjectType.name_latin,
                SysDepartment.name_latin,
                SysPerson.name_latin,
                EveCommittee.id,
                EveGeneration.year,
                EveGeneration.name_latin,
                EveProject.id,
                EveProject.code,
                EveProject.topic,
                EveSupervisor.name_latin
            ).order_by(EveProjectShortlist.id.asc()).all()

            projects = []
            group = None

            for row in results:
                eve_committee_score = EveCommitteeScore.query.filter_by(
                    eve_committee_id=row.eve_project_committee_id, eve_project_shortlist_id=row.eve_project_shortlist_id).count()
                total_score = db.session.query(func.coalesce(func.sum(EveCommitteeScore.score), 0)).filter(
                    EveCommitteeScore.eve_project_shortlist_id == row.eve_project_shortlist_id,
                    EveCommitteeScore.eve_committee_id == row.eve_project_committee_id
                ).scalar()
                # total_score = 100.00

                if group is None or row.eve_project_shortlist_id != group['eve_shortlist_id']:
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=row.eve_project_shortlist_id).first()

                    if group is not None:
                        projects.append(group)

                    # Create a new group for a new project
                    if eve_result:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': eve_result.total_score,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                    else:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': 0,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                else:
                    if eve_committee_score and eve_committee_score == 9:
                        # Append committee data to the eve_project_committee list
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': True,
                            'project_score': total_score
                        })
                    else:
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': False,
                            'project_score': total_score
                        })

                members = []
                eve_project_members = EveProjectMember.query.filter_by(
                    eve_event_id=1, eve_project_id=row.eve_project_id).all()

                for member in eve_project_members:
                    members.append({
                        'id': member.id,
                        'name_latin': member.name_latin,
                        'name_khmer': member.name_khmer,
                        'sys_gender': {
                            'id': member.sys_gender.id,
                            'name_latin': member.sys_gender.name_latin
                        }
                    })

                group['eve_project_members'] = members

            # Append the last group after the loop
            if group:
                projects.append(group)

            return projects, 200
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong!!"}, 500


@ns.route('/events/<int:eid>/departments/<int:did>/years/<string:year>')
class EveProjectShortlistTable(Resource):

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(output_custom_project_shortlist_model)
    def get(self, eid, did, year):
        try:
            results = db.session.query(
                EveProjectShortlist.id.label('eve_project_shortlist_id'),
                EveEvent.name_latin.label('eve_event_name'),
                EveProjectType.name_latin.label('eve_project_type'),
                EveCommittee.id.label('eve_project_committee_id'),
                EveGeneration.name_latin.label('eve_project_generation'),
                EveGeneration.year.label('eve_project_year'),
                SysDepartment.name_latin.label('department'),
                SysPerson.name_latin.label('eve_project_committee_name'),
                EveProject.id.label('eve_project_id'),
                EveProject.code.label('eve_project_code'),
                EveProject.topic.label('eve_project_topic'),
                EveSupervisor.name_latin.label('eve_project_supervisor_name')
            )\
                .join(EveProject, (EveProject.id == EveProjectShortlist.eve_project_id) & (EveProject.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectType, (EveProjectShortlist.eve_project_type_id == EveProjectType.id) & (EveProjectType.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectCommittee, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id)\
                .join(EveEvent, EveEvent.id == EveProjectShortlist.eve_event_id)\
                .join(EveSupervisor, EveProject.eve_supervisor_id == EveSupervisor.id)\
                .join(EveCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id)\
                .join(SysPerson, SysPerson.id == EveCommittee.sys_person_id)\
                .join(EveGeneration, (EveGeneration.year == year) & (EveGeneration.sys_department_id == EveProject.sys_department_id) & (EveGeneration.id == EveProject.eve_generation_id) & (EveGeneration.sys_department_id == did))\
                .join(SysDepartment, SysDepartment.id == EveGeneration.sys_department_id)\
                .filter(EveProjectShortlist.eve_event_id == eid)\
                .group_by(
                    EveProjectShortlist.id,
                    EveEvent.name_latin,
                    EveProjectType.name_latin,
                    EveCommittee.id,
                    EveGeneration.name_latin,
                    EveGeneration.year,
                    SysDepartment.name_latin,
                    SysPerson.name_latin,
                    EveProject.id,
                    EveProject.code,
                    EveProject.topic,
                    EveSupervisor.name_latin
            ).order_by(EveProjectShortlist.id.asc()).all()

            projects = []
            group = None

            for row in results:
                eve_committee_score = EveCommitteeScore.query.filter_by(
                    eve_committee_id=row.eve_project_committee_id, eve_project_shortlist_id=row.eve_project_shortlist_id).count()
                total_score = db.session.query(func.coalesce(func.sum(EveCommitteeScore.score), 0)).filter(
                    EveCommitteeScore.eve_project_shortlist_id == row.eve_project_shortlist_id,
                    EveCommitteeScore.eve_committee_id == row.eve_project_committee_id
                ).scalar()

                if group is None or row.eve_project_shortlist_id != group['eve_shortlist_id']:
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=row.eve_project_shortlist_id).first()

                    if group is not None:
                        projects.append(group)

                    # Create a new group for a new project
                    if eve_result:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': eve_result.total_score,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                    else:
                        group = {
                            'eve_shortlist_id': row.eve_project_shortlist_id,
                            'eve_event_name': row.eve_event_name,
                            'eve_project_type': row.eve_project_type,
                            'eve_project_id': row.eve_project_id,
                            'eve_project_code': row.eve_project_code,
                            'eve_project_topic': row.eve_project_topic,
                            'eve_project_generation': row.eve_project_generation,
                            'eve_project_department': row.department,
                            'eve_project_year': row.eve_project_year,
                            'eve_project_supervisor_name': row.eve_project_supervisor_name,
                            'project_total_score': 0,
                            'eve_project_committee': [
                                {
                                    'id': row.eve_project_committee_id,
                                    'name': row.eve_project_committee_name,
                                    'is_evaluated': eve_committee_score == 9,
                                    'project_score': total_score
                                }
                            ],
                            'eve_project_members': []
                        }
                else:
                    if eve_committee_score and eve_committee_score == 9:
                        # Append committee data to the eve_project_committee list
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': True,
                            'project_score': total_score
                        })
                    else:
                        group['eve_project_committee'].append({
                            'id': row.eve_project_committee_id,
                            'name': row.eve_project_committee_name,
                            'is_evaluated': False,
                            'project_score': total_score
                        })

                members = []
                eve_project_members = EveProjectMember.query.filter_by(
                    eve_event_id=eid, eve_project_id=row.eve_project_id).all()

                for member in eve_project_members:
                    members.append({
                        'id': member.id,
                        'name_latin': member.name_latin,
                        'name_khmer': member.name_khmer,
                        'sys_gender': {
                            'id': member.sys_gender.id,
                            'name_latin': member.sys_gender.name_latin
                        }
                    })

                group['eve_project_members'] = members

            # Append the last group after the loop
            if group:
                projects.append(group)

            return projects, 200
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong!!"}, 500


@ns.route('/events/eve-committees/<int:cid>/project-shortlists/<int:sid>')
class EveCommitteeProjectShortlist(Resource):

    @ns.marshal_with(output_all_committee_score)
    @ns.doc(security='jsonWebToken')
    def get(self, sid, cid):
        try:
            static1 = [10, 9, 8, 7, 6, 5, 4, 3]
            static2 = [20, 18, 16, 14, 12, 10, 8, 6]
            results = db.session.query(
                EveCommittee.id.label('committee_id'),
                SysPerson.name_latin.label('committee_name'),
                EveProject.code.label('code'),
                EveProject.topic.label('topic'),
                EveProjectShortlist.id.label('project_shortlist_id'),
                EveEvalCategory.id.label('category_id'),
                EveEvalCategory.name_latin.label('category_name'),
                EveEvalCriteria.id.label('criteria_id'),
                EveEvalCriteria.name_latin.label('criteria_name'),
                EveRubricCategory.name_latin.label('rubric'),
                EveCommitteeScore.score.label('criteria_score'),
                EveCommitteeScore.updated_at.label('updated_at')
            ).join(
                SysPerson, EveCommittee.sys_person_id == SysPerson.id
            ).join(
                EveProjectCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id
            ).join(
                EveProjectShortlist, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id
            ).join(
                EveProject, EveProjectShortlist.eve_project_id == EveProject.id
            ).join(
                EveCommitteeScore, (EveCommittee.id == EveCommitteeScore.eve_committee_id) & (
                    EveProjectShortlist.id == EveCommitteeScore.eve_project_shortlist_id)
            ).join(
                EveEvalCriteria, EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteria.id
            ).join(
                EveEvalCategory, EveEvalCriteria.eve_eval_category_id == EveEvalCategory.id
            ).join(
                EveEvalCriteriaRubric, (EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteriaRubric.eve_eval_criteria_id) & (
                    EveCommitteeScore.score == EveEvalCriteriaRubric.score)
            ).join(
                EveRubricCategory, EveEvalCriteriaRubric.eve_rubric_category_id == EveRubricCategory.id
            ).filter(
                EveProjectShortlist.id == sid, EveCommittee.id == cid
            ).group_by(
                EveCommittee.id, SysPerson.name_latin, EveProject.code, EveProject.topic, EveProjectShortlist.id, EveEvalCategory.id, EveEvalCategory.name_latin, EveEvalCriteria.id, EveEvalCriteria.name_latin, EveCommitteeScore.score, EveRubricCategory.name_latin, EveCommitteeScore.updated_at
            ).order_by(
                EveCommittee.id, EveProjectShortlist.id.asc()
            ).all()

            grouped_data = []

            for row in results:
                # Check if committee is already in the grouped_data
                committee = next(
                    (comm for comm in grouped_data if comm['id'] == row.committee_id), None)
                if not committee:
                    committee = {
                        "id": row.committee_id,
                        "name": row.committee_name,
                        "projects": []
                    }
                    grouped_data.append(committee)

                # Check if project is already in the committee's projects
                project = None
                for proj in committee['projects']:
                    if proj['id'] == row.project_shortlist_id:
                        project = proj
                        break

                if not project:
                    eve_committee_project_score = EveCommitteeScore.query.filter_by(
                        eve_project_shortlist_id=row.project_shortlist_id, eve_event_id=1,
                        eve_committee_id=row.committee_id).first()
                    project = {
                        "id": row.project_shortlist_id,
                        "code": row.code,
                        "topic": row.topic,
                        "total_score": 0,
                        "comment": eve_committee_project_score.comment,
                        "categories": []
                    }
                    committee['projects'].append(project)

                # Check if category is already in the project's categories
                category = None
                for cat in project['categories']:
                    if cat['id'] == row.category_id:
                        category = cat
                        break

                if not category:
                    category = {
                        "id": row.category_id,
                        "name": row.category_name,
                        "criterias": []
                    }
                    project['categories'].append(category)

                eva_score = static1
                if row.criteria_id == 4:
                    eva_score = static2

                criteria_data = {
                    "id": row.criteria_id,
                    "name": row.criteria_name,
                    "eva_score": eva_score,
                    "score": row.criteria_score,
                    "rubric": row.rubric
                }
                category['criterias'].append(criteria_data)

            # Calculate total_score for each project and print the result
            for committee in grouped_data:
                for project in committee['projects']:
                    total_score = sum(criteria['score'] for category in project['categories']
                                      for criteria in category['criterias'])
                    project['total_score'] = total_score

            return {"committees": grouped_data}, 200
        except Exception as e:
            print(e)
            return {"msg": "something went wrong!!"}, 500


# evaluate
@ns.route('/events/<int:eid>/project-scores')
class Evaluations(Resource):

    @ns.expect(input_eve_project_score_model)
    @ns.doc(security='jsonWebToken')
    def post(self, eid):
        try:
            data = ns.payload or request.json
            results = data["results"]
            if EveProjectCommittee.query.filter_by(
                eve_committee_id=data["committee_id"],
                eve_event_id=eid,
                eve_project_shortlist_id=data["project_id"]
            ).first():
                if not EveCommitteeScore.query.filter_by(eve_committee_id=data['committee_id'], eve_project_shortlist_id=data["project_id"]).count() >= 9:
                    if len(results) == 9:
                        for result in results:
                            eve_committee_score = EveCommitteeScore(
                                eve_committee_id=data["committee_id"],
                                eve_project_shortlist_id=data["project_id"],
                                eve_event_id=eid,
                                eve_eval_criteria_id=result["criteria_id"],
                                score=result["score"],
                                comment=data['comment'],
                                created_by=get_jwt()['user_id'],
                                created_at=current_time_cambodia(),
                                updated_by=get_jwt()['user_id'],
                                updated_at=current_time_cambodia()
                            )
                            db.session.add(eve_committee_score)
                            db.session.commit()
                    else:
                        return {'msg': 'missing some data!!'}, 400

                    # find total score of EveCommitteeScore
                    new_total_score = db.session.query(func.sum(EveCommitteeScore.score)).filter(
                        EveCommitteeScore.eve_project_shortlist_id == data["project_id"]).scalar()

                    # count committee with the same project and event but different committee_id to avoid duplicate
                    count_committee = db.session.query(EveCommitteeScore.eve_committee_id).filter_by(
                        eve_event_id=eid, eve_project_shortlist_id=data["project_id"]).distinct().count()

                    # calculate average
                    average = new_total_score/count_committee

                    # query result in database
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=data["project_id"]).first()
                    if eve_result:
                        eve_result.total_score = average
                        db.session.commit()
                    else:
                        eve_project_shortlist = EveProjectShortlist.query.filter_by(
                            id=data["project_id"]).first()
                        eve_project = EveProject.query.filter_by(
                            id=eve_project_shortlist.eve_project_id).first()
                        if eve_project_shortlist and eve_project:
                            eve_result = EveResult(
                                eve_project_shortlist_id=data["project_id"],
                                eve_project_id=eve_project_shortlist.eve_project_id,
                                eve_project_type_id=eve_project.eve_project_type_id,
                                eve_generation_id=eve_project.eve_generation_id,
                                total_score=average,
                                is_locked=False,
                                created_by=get_jwt()['user_id'],
                                created_at=current_time_cambodia(),
                                updated_by=get_jwt()['user_id'],
                                updated_at=current_time_cambodia()
                            )
                            db.session.add(eve_result)
                            db.session.commit()
                    return {"msg": "created"}, 201
                else:
                    return {"msg": "user already evaluated"}, 400

            else:
                return {"msg": "user not an project committee"}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong!'}, 500


# project detial by committees
@ns.route('/events/committee-project-shortlist-details/<int:sid>')
class CommitteeProjectShortlistDetails(Resource):

    @ns.marshal_with(output_all_committee_score)
    @ns.doc(security='jsonWebToken')
    def get(self, sid):
        results = db.session.query(
            EveCommittee.id.label('committee_id'),
            SysPerson.name_latin.label('committee_name'),
            EveProject.code.label('code'),
            EveProjectShortlist.id.label('project_shortlist_id'),
            EveEvalCategory.id.label('category_id'),
            EveEvalCategory.name_latin.label('category_name'),
            EveEvalCriteria.id.label('criteria_id'),
            EveEvalCriteria.name_latin.label('criteria_name'),
            EveRubricCategory.name_latin.label('rubric'),
            EveCommitteeScore.score.label('criteria_score'),
            EveCommitteeScore.updated_at.label('updated_at')
        ).join(
            SysPerson, EveCommittee.sys_person_id == SysPerson.id
        ).join(
            EveProjectCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id
        ).join(
            EveProjectShortlist, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id
        ).join(
            EveProject, EveProjectShortlist.eve_project_id == EveProject.id
        ).join(
            EveCommitteeScore, (EveCommittee.id == EveCommitteeScore.eve_committee_id) & (
                EveProjectShortlist.id == EveCommitteeScore.eve_project_shortlist_id)
        ).join(
            EveEvalCriteria, EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteria.id
        ).join(
            EveEvalCategory, EveEvalCriteria.eve_eval_category_id == EveEvalCategory.id
        ).join(
            EveEvalCriteriaRubric, (EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteriaRubric.eve_eval_criteria_id) & (
                EveCommitteeScore.score == EveEvalCriteriaRubric.score)
        ).join(
            EveRubricCategory, EveEvalCriteriaRubric.eve_rubric_category_id == EveRubricCategory.id
        ).filter(
            EveProjectShortlist.id == sid
        ).group_by(
            EveCommittee.id, SysPerson.name_latin, EveProject.code, EveProjectShortlist.id, EveEvalCategory.id, EveEvalCategory.name_latin, EveEvalCriteria.id, EveEvalCriteria.name_latin, EveCommitteeScore.score, EveRubricCategory.name_latin, EveCommitteeScore.updated_at
        ).order_by(
            EveCommittee.id, EveProjectShortlist.id.asc()
        ).all()

        grouped_data = []

        for row in results:
            # Check if committee is already in the grouped_data
            committee = next(
                (comm for comm in grouped_data if comm['id'] == row.committee_id), None)
            if not committee:
                committee = {
                    "id": row.committee_id,
                    "name": row.committee_name,
                    "projects": []
                }
                grouped_data.append(committee)

            # Check if project is already in the committee's projects
            project = None
            for proj in committee['projects']:
                if proj['id'] == row.project_shortlist_id:
                    project = proj
                    break

            if not project:
                project = {
                    "id": row.project_shortlist_id,
                    "code": row.code,
                    "total_score": 0,
                    "categories": []
                }
                committee['projects'].append(project)

            # Check if category is already in the project's categories
            category = None
            for cat in project['categories']:
                if cat['id'] == row.category_id:
                    category = cat
                    break

            if not category:
                category = {
                    "id": row.category_id,
                    "name": row.category_name,
                    "criterias": []
                }
                project['categories'].append(category)

            criteria_data = {
                "id": row.criteria_id,
                "name": row.criteria_name,
                "score": row.criteria_score,
                "rubric": row.rubric
            }
            category['criterias'].append(criteria_data)

        # Calculate total_score for each project and print the result
        for committee in grouped_data:
            for project in committee['projects']:
                total_score = sum(criteria['score'] for category in project['categories']
                                  for criteria in category['criterias'])
                project['total_score'] = total_score

        return {"committees": grouped_data}, 200


# project detial by projects
@ns.route('/events/project-shortlist-committee-details/<int:sid>')
class ProjectShortlistCommitteeDetails(Resource):

    @ns.marshal_with(output_project_shortlist_detial_model)
    @ns.doc(security='jsonWebToken')
    def get(self, sid):
        """Get a Project Shortlist Detial By ID"""
        try:
            results = db.session.query(
                EveProjectShortlist.id.label('project_shortlist_id'),
                EveProject.code.label('code'),
                EveProject.topic.label('project_topic'),
                EveProjectType.name_latin.label('project_type'),
                EveSupervisor.name_latin.label('project_supervisor'),
                SysDepartment.name_latin.label('department'),
                EveGeneration.name_latin.label('project_generation'),
                EveGeneration.year.label('year'),
                EveResult.total_score.label('total_score'),
                EveCommittee.id.label('committee_id'),
                SysPerson.name_latin.label('committee_name'),
                EveEvalCategory.id.label('category_id'),
                EveEvalCategory.name_latin.label('category_name'),
                EveEvalCriteria.id.label('criteria_id'),
                EveEvalCriteria.name_latin.label('criteria_name'),
                EveRubricCategory.name_latin.label('rubric'),
                EveCommitteeScore.score.label('criteria_score'),
            ).join(
                SysPerson, EveCommittee.sys_person_id == SysPerson.id
            ).join(
                EveProjectCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id
            ).join(
                EveProjectShortlist, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id
            ).join(
                EveProject, EveProjectShortlist.eve_project_id == EveProject.id
            ).join(
                EveCommitteeScore, (EveCommittee.id == EveCommitteeScore.eve_committee_id) & (
                    EveProjectShortlist.id == EveCommitteeScore.eve_project_shortlist_id)
            ).join(
                EveEvalCriteria, EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteria.id
            ).join(
                EveEvalCategory, EveEvalCriteria.eve_eval_category_id == EveEvalCategory.id
            ).join(
                EveEvalCriteriaRubric, (EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteriaRubric.eve_eval_criteria_id) & (
                    EveCommitteeScore.score == EveEvalCriteriaRubric.score)
            ).join(
                EveRubricCategory, EveEvalCriteriaRubric.eve_rubric_category_id == EveRubricCategory.id
            ).join(
                EveProjectType, EveProjectType.id == EveProject.eve_project_type_id
            ).join(
                EveGeneration, EveGeneration.id == EveProject.eve_generation_id
            ).join(
                SysDepartment, (SysDepartment.id == EveGeneration.sys_department_id) & (
                    SysDepartment.id == EveProject.sys_department_id)
            ).join(
                EveSupervisor, EveSupervisor.id == EveProject.eve_supervisor_id
            ).join(
                EveResult, EveResult.eve_project_id == EveProject.id
            ).filter(
                EveProjectShortlist.id == sid
            ).group_by(
                EveProjectShortlist.id, EveProject.code,
                EveProject.topic, EveProjectType.name_latin,
                EveProject.eve_supervisor, SysDepartment.name_latin,
                EveGeneration.name_latin, EveGeneration.year, EveResult.total_score,
                EveSupervisor.name_latin,
                EveCommittee.id, SysPerson.name_latin,  EveEvalCategory.id,
                EveEvalCategory.name_latin, EveEvalCriteria.id, EveEvalCriteria.name_latin,
                EveCommitteeScore.score, EveRubricCategory.name_latin
            ).order_by(
                EveCommittee.id, EveProjectShortlist.id, EveEvalCriteria.id.asc()
            ).all()

            results2 = db.session.query(
                EveProjectShortlist.id.label('eve_project_shortlist_id'),
                EveEvent.name_latin.label('eve_event_name'),
                EveProjectType.name_latin.label('eve_project_type'),
                SysDepartment.name_latin.label('department'),
                EveCommittee.id.label('eve_project_committee_id'),
                SysPerson.name_latin.label('eve_project_committee_name'),
                EveGeneration.name_latin.label('eve_project_generation'),
                EveGeneration.year.label('eve_project_year'),
                EveProject.id.label('eve_project_id'),
                EveProject.code.label('eve_project_code'),
                EveProject.topic.label('eve_project_topic'),
                EveSupervisor.name_latin.label('eve_project_supervisor_name')
            ).join(EveProject, (EveProject.id == EveProjectShortlist.eve_project_id) & (EveProject.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectType, (EveProjectShortlist.eve_project_type_id == EveProjectType.id) & (EveProjectType.eve_event_id == EveProjectShortlist.eve_event_id))\
                .join(EveProjectCommittee, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id)\
                .join(EveEvent, EveEvent.id == EveProjectShortlist.eve_event_id)\
                .join(EveSupervisor, EveProject.eve_supervisor_id == EveSupervisor.id)\
                .join(EveCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id)\
                .join(SysPerson, SysPerson.id == EveCommittee.sys_person_id)\
                .join(EveGeneration, (EveGeneration.sys_department_id == EveProject.sys_department_id) & (EveGeneration.id == EveProject.eve_generation_id))\
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)\
                .filter(EveProjectShortlist.eve_event_id == 1, EveProjectShortlist.id == sid)\
                .group_by(
                EveProjectShortlist.id,
                EveEvent.name_latin,
                EveProjectType.name_latin,
                SysDepartment.name_latin,
                SysPerson.name_latin,
                EveCommittee.id,
                EveGeneration.year,

                EveGeneration.name_latin,
                EveProject.id,
                EveProject.code,
                EveProject.topic,
                EveSupervisor.name_latin
            ).order_by(EveProjectShortlist.id.asc()).all()

            final_result = {}
            projects = []
            group = None

            if results:
                # Iterate through the query result
                for row in results:
                    # Check if the shortlist ID is already in the final result
                    if row.project_shortlist_id not in final_result:
                        # If not, add basic project information
                        final_result[row.project_shortlist_id] = {
                            "eve_shortlist_id": row.project_shortlist_id,
                            "eve_event_name": "Engineering Day",
                            "eve_project_type": row.project_type,
                            "eve_project_code": row.code,
                            "eve_project_topic": row.project_topic,
                            "eve_project_generation": row.project_generation,
                            "eve_project_department": row.department,
                            "eve_project_year": row.year,
                            "eve_project_total_score": row.total_score,
                            "eve_project_supervisor_name": row.project_supervisor,
                            "eve_project_members": [],
                            "eve_project_committee": []
                        }

                        eve_project_shortlist = EveProjectShortlist.query.get(
                            row.project_shortlist_id
                        )

                        # Fetch project members
                        eve_project_members = EveProjectMember.query.filter_by(
                            eve_event_id=1, eve_project_id=eve_project_shortlist.eve_project_id).all()

                        # Add member information to the project
                        for member in eve_project_members:
                            final_result[row.project_shortlist_id]["eve_project_members"].append({
                                'id': member.id,
                                'name_latin': member.name_latin,
                                'name_khmer': member.name_khmer,
                                'sys_gender': {
                                    'id': member.sys_gender.id,
                                    'name_latin': member.sys_gender.name_latin
                                }
                            })

                    # Check if the committee ID is already in the project's committee list
                    committee_exists = any(
                        committee["id"] == row.committee_id for committee in final_result[row.project_shortlist_id]["eve_project_committee"]
                    )

                    if not committee_exists:
                        eve_committee_score = EveCommitteeScore.query.filter_by(
                            eve_project_shortlist_id=row.project_shortlist_id, eve_event_id=1,
                            eve_committee_id=row.committee_id).first()
                        # If not, add committee information
                        committee_info = {
                            "id": row.committee_id,
                            "name": row.committee_name,
                            "comment": eve_committee_score.comment,
                            "project_score": 0,  # You may need to calculate the total score for the committee
                            "categories": []
                        }
                        final_result[row.project_shortlist_id]["eve_project_committee"].append(
                            committee_info)
                    else:
                        # If committee exists, get the committee_info
                        committee_info = next(
                            c for c in final_result[row.project_shortlist_id]["eve_project_committee"] if c["id"] == row.committee_id
                        )

                    # Check if the category ID is already in the committee's categories list
                    category_exists = any(
                        category["id"] == row.category_id for category in committee_info["categories"]
                    )

                    if not category_exists:
                        # If not, add category information
                        category_info = {
                            "id": row.category_id,
                            "name": row.category_name,
                            "criterias": [
                                {
                                    "id": row.criteria_id,
                                    "name": row.criteria_name,
                                    "score": row.criteria_score,
                                    "rubric": row.rubric
                                }
                            ]
                        }
                        committee_info["categories"].append(category_info)

                        # Update the total score for the committee
                        committee_info["project_score"] += row.criteria_score
                    else:
                        # If category exists, get the category_info
                        category_info = next(
                            c for c in committee_info["categories"] if c["id"] == row.category_id
                        )

                        # Check if the criteria ID is already in the category's criterias list
                        criteria_exists = any(
                            criteria["id"] == row.criteria_id for criteria in category_info["criterias"]
                        )

                        if not criteria_exists:
                            # If not, add criteria information
                            criteria_info = {
                                "id": row.criteria_id,
                                "name": row.criteria_name,
                                "score": row.criteria_score,
                                "rubric": row.rubric
                            }
                            category_info["criterias"].append(criteria_info)

                            # Update the total score for the committee
                            committee_info["project_score"] += row.criteria_score

                # Query all committees for the current project_shortlist_id
                all_project_committees = EveProjectCommittee.query.filter_by(
                    eve_event_id=1,
                    eve_project_shortlist_id=sid
                ).all()

                # Iterate through all committees and check if they are in the project result
                for committee in all_project_committees:
                    # Check if the committee is already in the project result
                    committee_in_result = any(
                        existing_committee["id"] == committee.eve_committee_id
                        for existing_committee in final_result[row.project_shortlist_id]["eve_project_committee"]
                    )

                    # If the committee is not in the result, add it with a default score of zero
                    if not committee_in_result:
                        eve_committee = EveCommittee.query.get(
                            committee.eve_committee_id)
                        sys_person = SysPerson.query.get(
                            eve_committee.sys_person_id)

                        committee_info = {
                            "id": eve_committee.id,
                            "name": sys_person.name_latin,
                            "project_score": 0,  # Default score
                        }
                        final_result[row.project_shortlist_id]["eve_project_committee"].append(
                            committee_info)

                # Convert the final result to a list for a cleaner structure
                final_result_list = list(final_result.values())

                # print(final_result_list)
                return final_result_list, 200

            elif results2:
                for row in results2:
                    eve_committee_score = EveCommitteeScore.query.filter_by(
                        eve_committee_id=row.eve_project_committee_id, eve_project_shortlist_id=row.eve_project_shortlist_id).count()
                    total_score = db.session.query(func.coalesce(func.sum(EveCommitteeScore.score), 0)).filter(
                        EveCommitteeScore.eve_project_shortlist_id == row.eve_project_shortlist_id,
                        EveCommitteeScore.eve_committee_id == row.eve_project_committee_id
                    ).scalar()
                    # total_score = 100.00

                    if group is None or row.eve_project_shortlist_id != group['eve_shortlist_id']:
                        eve_result = EveResult.query.filter_by(
                            eve_project_shortlist_id=row.eve_project_shortlist_id).first()

                        if group is not None:
                            projects.append(group)

                        # Create a new group for a new project
                        if eve_result:
                            group = {
                                'eve_shortlist_id': row.eve_project_shortlist_id,
                                'eve_event_name': row.eve_event_name,
                                'eve_project_type': row.eve_project_type,
                                'eve_project_id': row.eve_project_id,
                                'eve_project_code': row.eve_project_code,
                                'eve_project_topic': row.eve_project_topic,
                                'eve_project_generation': row.eve_project_generation,
                                'eve_project_department': row.department,
                                'eve_project_year': row.eve_project_year,
                                'eve_project_supervisor_name': row.eve_project_supervisor_name,
                                'project_total_score': eve_result.total_score,
                                'eve_project_committee': [
                                    {
                                        'id': row.eve_project_committee_id,
                                        'name': row.eve_project_committee_name,
                                        'is_evaluated': eve_committee_score == 9,
                                        'project_score': total_score
                                    }
                                ],
                                'eve_project_members': []
                            }
                        else:
                            group = {
                                'eve_shortlist_id': row.eve_project_shortlist_id,
                                'eve_event_name': row.eve_event_name,
                                'eve_project_type': row.eve_project_type,
                                'eve_project_id': row.eve_project_id,
                                'eve_project_code': row.eve_project_code,
                                'eve_project_topic': row.eve_project_topic,
                                'eve_project_generation': row.eve_project_generation,
                                'eve_project_department': row.department,
                                'eve_project_year': row.eve_project_year,
                                'eve_project_supervisor_name': row.eve_project_supervisor_name,
                                'project_total_score': 0,
                                'eve_project_committee': [
                                    {
                                        'id': row.eve_project_committee_id,
                                        'name': row.eve_project_committee_name,
                                        'is_evaluated': eve_committee_score == 9,
                                        'project_score': total_score
                                    }
                                ],
                                'eve_project_members': []
                            }
                    else:
                        if eve_committee_score and eve_committee_score == 9:
                            # Append committee data to the eve_project_committee list
                            group['eve_project_committee'].append({
                                'id': row.eve_project_committee_id,
                                'name': row.eve_project_committee_name,
                                'is_evaluated': True,
                                'project_score': total_score
                            })
                        else:
                            group['eve_project_committee'].append({
                                'id': row.eve_project_committee_id,
                                'name': row.eve_project_committee_name,
                                'is_evaluated': False,
                                'project_score': total_score
                            })

                    members = []
                    eve_project_members = EveProjectMember.query.filter_by(
                        eve_event_id=1, eve_project_id=row.eve_project_id).all()

                    for member in eve_project_members:
                        members.append({
                            'id': member.id,
                            'name_latin': member.name_latin,
                            'name_khmer': member.name_khmer,
                            'sys_gender': {
                                'id': member.sys_gender.id,
                                'name_latin': member.sys_gender.name_latin
                            }
                        })

                    group['eve_project_members'] = members

                # Append the last group after the loop
                if group:
                    projects.append(group)
                return projects, 200
            else:
                return {"msg": "not found"}, 404
        except Exception as e:
            print(e)
            return {"error": "something went wrong!!"}, 500


# update form data
@ns.route('/events/<int:eid>/project_shortlist/<int:sid>/committees/<int:cid>')
class Evaluation(Resource):

    @ns.expect(input_eve_project_score_model)
    @ns.doc(security='jsonWebToken')
    def put(self, eid, sid, cid):
        try:
            eve_committee_scores = EveCommitteeScore.query.filter_by(
                eve_event_id=eid,
                eve_project_shortlist_id=sid,
                eve_committee_id=cid
            ).all()

            data = ns.payload or request.json
            results = data['results']

            if eve_committee_scores:
                if len(results) == 9:
                    for eve_committee_score, result in zip(eve_committee_scores, results):
                        eve_committee_score.eve_committee_id = data["committee_id"],
                        eve_committee_score.eve_project_shortlist_id = data["project_id"],
                        eve_committee_score.eve_event_id = eid,
                        eve_committee_score.eve_eval_criteria_id = result["criteria_id"],
                        eve_committee_score.score = result["score"],
                        eve_committee_score.comment = data['comment'],
                        eve_committee_score.updated_by = get_jwt()['user_id'],
                        eve_committee_score.updated_at = current_time_cambodia()
                        db.session.commit()

                    # find total score of EveCommitteeScore
                    new_total_score = db.session.query(func.sum(EveCommitteeScore.score)).filter(
                        EveCommitteeScore.eve_project_shortlist_id == data["project_id"]).scalar()

                    # count committee with the same project and event but different committee_id to avoid duplicate
                    count_committee = db.session.query(EveCommitteeScore.eve_committee_id).filter_by(
                        eve_event_id=eid, eve_project_shortlist_id=data["project_id"]).distinct().count()

                    # calculate average
                    average = new_total_score/count_committee

                    # query result in database
                    eve_result = EveResult.query.filter_by(
                        eve_project_shortlist_id=data["project_id"]).first()
                    if eve_result:
                        eve_result.total_score = average
                        db.session.commit()
                    else:
                        eve_project_shortlist = EveProjectShortlist.query.filter_by(
                            id=data["project_id"]).first()
                        eve_project = EveProject.query.filter_by(
                            id=eve_project_shortlist.eve_project_id).first()
                        if eve_project_shortlist and eve_project:
                            eve_result = EveResult(
                                eve_project_shortlist_id=data["project_id"],
                                eve_project_id=eve_project_shortlist.eve_project_id,
                                eve_project_type_id=eve_project.eve_project_type_id,
                                eve_generation_id=eve_project.eve_generation_id,
                                total_score=average,
                                is_locked=False,
                                created_by=get_jwt()['user_id'],
                                created_at=current_time_cambodia(),
                                updated_by=get_jwt()['user_id'],
                                updated_at=current_time_cambodia()
                            )
                            db.session.add(eve_result)
                            db.session.commit()
                    return {"msg": "created"}, 201
                else:
                    return {"msg": "missing some part of data"}, 400
            else:
                return {"msg": "user not project committee"}, 404
        except Exception as e:
            print(e)
            return {"error": "something went wrong!"}, 500


@ns.route('/events/all-eve-committee-scores')
class AllCommitteeScore(Resource):

    @ns.marshal_with(output_all_committee_score)
    @ns.doc(security='jsonWebToken')
    def get(self):
        results = db.session.query(
            EveCommittee.id.label('committee_id'),
            SysPerson.name_latin.label('committee_name'),
            EveProject.code.label('code'),
            EveProjectShortlist.id.label('project_shortlist_id'),
            EveEvalCategory.id.label('category_id'),
            EveEvalCategory.name_latin.label('category_name'),
            EveEvalCriteria.id.label('criteria_id'),
            EveEvalCriteria.name_latin.label('criteria_name'),
            EveRubricCategory.name_latin.label('rubric'),
            EveCommitteeScore.score.label('criteria_score'),
            EveCommitteeScore.updated_at.label('updated_at')
        ).join(
            SysPerson, EveCommittee.sys_person_id == SysPerson.id
        ).join(
            EveProjectCommittee, EveCommittee.id == EveProjectCommittee.eve_committee_id
        ).join(
            EveProjectShortlist, EveProjectCommittee.eve_project_shortlist_id == EveProjectShortlist.id
        ).join(
            EveProject, EveProjectShortlist.eve_project_id == EveProject.id
        ).join(
            EveCommitteeScore, (EveCommittee.id == EveCommitteeScore.eve_committee_id) & (
                EveProjectShortlist.id == EveCommitteeScore.eve_project_shortlist_id)
        ).join(
            EveEvalCriteria, EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteria.id
        ).join(
            EveEvalCategory, EveEvalCriteria.eve_eval_category_id == EveEvalCategory.id
        ).join(
            EveEvalCriteriaRubric, (EveCommitteeScore.eve_eval_criteria_id == EveEvalCriteriaRubric.eve_eval_criteria_id) & (
                EveCommitteeScore.score == EveEvalCriteriaRubric.score)
        ).join(
            EveRubricCategory, EveEvalCriteriaRubric.eve_rubric_category_id == EveRubricCategory.id
        ).group_by(
            EveCommittee.id, SysPerson.name_latin, EveProject.code, EveProjectShortlist.id, EveEvalCategory.id, EveEvalCategory.name_latin, EveEvalCriteria.id, EveEvalCriteria.name_latin, EveCommitteeScore.score, EveRubricCategory.name_latin, EveCommitteeScore.updated_at
        ).order_by(
            EveCommittee.id, EveProjectShortlist.id.asc()
        ).all()

        grouped_data = []

        for row in results:
            # Check if committee is already in the grouped_data
            committee = next(
                (comm for comm in grouped_data if comm['id'] == row.committee_id), None)
            if not committee:
                committee = {
                    "id": row.committee_id,
                    "name": row.committee_name,
                    "projects": []
                }
                grouped_data.append(committee)

            # Check if project is already in the committee's projects
            project = None
            for proj in committee['projects']:
                if proj['id'] == row.project_shortlist_id:
                    project = proj
                    break

            if not project:
                project = {
                    "id": row.project_shortlist_id,
                    "code": row.code,
                    "total_score": 0,
                    "categories": []
                }
                committee['projects'].append(project)

            # Check if category is already in the project's categories
            category = None
            for cat in project['categories']:
                if cat['id'] == row.category_id:
                    category = cat
                    break

            if not category:
                category = {
                    "id": row.category_id,
                    "name": row.category_name,
                    "criterias": []
                }
                project['categories'].append(category)

            criteria_data = {
                "id": row.criteria_id,
                "name": row.criteria_name,
                "score": row.criteria_score,
                "rubric": row.rubric
            }
            category['criterias'].append(criteria_data)

        # Calculate total_score for each project and print the result
        for committee in grouped_data:
            for project in committee['projects']:
                total_score = sum(criteria['score'] for category in project['categories']
                                  for criteria in category['criterias'])
                project['total_score'] = total_score

        return {"committees": grouped_data}, 200


@ns.route('/events/eve-certificate')
class Certificate(Resource):

    @ns.marshal_with(output_cerificate_result_model)
    @ns.doc(security="jsonWebToken")
    def get(self):
        try:
            page_index = 1
            # year 1 poster query result
            year1_subquery = (
                db.session.query(
                    EveProject.id.label('project_id'),
                    EveProject.code.label('code'),
                    EveProject.topic.label('topic'),
                    EveResult.total_score.label('total_score'),
                    SysDepartment.name_latin.label('department'),
                    EveGeneration.year,
                    db.func.row_number().over(partition_by=EveGeneration.year,
                                              order_by=EveResult.total_score.desc()).label('ranking')
                )
                .join(EveProject, EveProject.id == EveResult.eve_project_id)
                .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                .filter(EveResult.eve_project_type_id == 2, EveGeneration.year == 'Year1')
                .subquery()
            )

            year1_poster_award_results = (
                db.session.query(year1_subquery)
                .filter(year1_subquery.c.ranking <= 3)
                .all()
            )

            years = []
            if year1_poster_award_results:
                for row in year1_poster_award_results:
                    # Check if the year is already in the list of years
                    year_exists = any(
                        item['year'] == row.year for item in years)

                    if not year_exists:
                        # If the year is not in the list, add it with an empty ranks list
                        years.append({
                            "year": row.year,
                            "ranks": []
                        })

                    # Get the year dictionary from the list
                    current_year = next(
                        item for item in years if item['year'] == row.year)

                    # Check if the rank is already in the project's rank list for the current year
                    rank_exists = any(
                        rank['rank'] == row.ranking for rank in current_year["ranks"])

                    if not rank_exists:

                        # If the rank is not in the list, add it
                        current_year["ranks"].append({
                            "rank": row.ranking,
                            "department": row.department,
                            "project": {
                                "project_code": row.code,
                                "project_topic": row.topic,
                                'project_members': []
                            }
                        })

                        members = []
                        eve_project_members = EveProjectMember.query.filter_by(
                            eve_project_id=row.project_id).all()

                        for member in eve_project_members:
                            members.append({
                                'id': member.id,
                                'name_latin': member.name_latin,
                                'name_khmer': member.name_khmer,
                                'sys_gender': {
                                    'id': member.sys_gender.id,
                                    'name_latin': member.sys_gender.name_latin
                                },
                                'page_index': page_index
                            })
                            page_index = page_index + 1
                        # Find the rank dictionary that was just added
                        current_rank = next(
                            item for item in current_year["ranks"] if item['rank'] == row.ranking)
                        # Assign the members list to the 'eve_project_members' key within the 'project' dictionary
                        current_rank["project"]['project_members'] = members
            # end year 1

            # year 2 up
            number_of_departments = len(SysDepartment.query.all())
            poster_results = []
            presentation_results = []
            project_types = []

            for sys_department_id in range(1, number_of_departments+1):
                poster_sub_query = (
                    db.session.query(
                        EveProjectType.id.label('eve_project_type_id'),
                        EveProjectType.name_latin.label(
                            'eve_project_type_name'),
                        EveProject.id.label('project_id'),
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.id.label('department_id'),
                        SysDepartment.name_latin.label('department_name'),
                        EveGeneration.year.label('year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 2, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                poster_query = (
                    db.session.query(poster_sub_query)
                    .filter(poster_sub_query.c.ranking <= 1)
                    .all()
                )

                poster_results.extend(poster_query)

            if poster_results:
                for poster in poster_results:
                    type_exist = any(
                        type_info["id"] == poster.eve_project_type_id
                        for type_info in project_types
                    )

                    if not type_exist:
                        project_types.append({
                            'id': poster.eve_project_type_id,
                            'project_type_name': poster.eve_project_type_name,
                            'departments': []
                        })

                    current_type = next(
                        (type_info for type_info in project_types if type_info['id'] == poster.eve_project_type_id),
                        None
                    )

                    department_exist = any(
                        department['id'] == poster.department_id
                        for department in current_type.get('departments', [])
                    )

                    if not department_exist:
                        current_type['departments'].append({
                            'id': poster.department_id,
                            'department_name': poster.department_name,
                            'years': []
                        })

                    current_department = next(
                        (department for department in current_type.get(
                            'departments', []) if department['id'] == poster.department_id),
                        None
                    )

                    years_exist = any(
                        year['year'] == poster.year
                        for year in current_department.get('years', [])
                    )

                    if not years_exist:
                        current_department['years'].append({
                            'year': poster.year,
                            'ranks': []
                        })

                    current_year = next(
                        (year for year in current_department.get(
                            'years', []) if year['year'] == poster.year),
                        None
                    )

                    rank_exist = any(
                        rank['rank'] == poster.ranking
                        for rank in current_year.get('ranks', [])
                    )

                    if not rank_exist:
                        current_year['ranks'].append({
                            'rank': poster.ranking,
                            'total_score': poster.total_score,
                            'project': {}  # Initialize as an empty dictionary
                        })

                    current_rank = next(
                        (rank for rank in current_year.get('ranks', [])
                         if rank['rank'] == poster.ranking),
                        None
                    )

                    current_rank['project'] = {
                        'project_code': poster.code,
                        'project_topic': poster.topic,
                        'project_members': []
                    }

                    members = []
                    eve_project_members = EveProjectMember.query.filter_by(
                        eve_project_id=poster.project_id).all()

                    for member in eve_project_members:
                        members.append({
                            'id': member.id,
                            'name_latin': member.name_latin,
                            'name_khmer': member.name_khmer,
                            'sys_gender': {
                                'id': member.sys_gender.id,
                                'name_latin': member.sys_gender.name_latin
                            },
                            'page_index': page_index
                        })
                        page_index = page_index+1

                    current_rank = next(
                        item for item in current_year["ranks"] if item['rank'] == poster.ranking)
                    # Assign the members list to the 'eve_project_members' key within the 'project' dictionary
                    current_rank["project"]['project_members'] = members

            # for presentation
            for sys_department_id in range(1, number_of_departments+1):
                presentation_sub_query = (
                    db.session.query(
                        EveProjectType.id.label('eve_project_type_id'),
                        EveProjectType.name_latin.label(
                            'eve_project_type_name'),
                        EveProject.id.label('project_id'),
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.id.label('department_id'),
                        SysDepartment.name_latin.label('department_name'),
                        EveGeneration.year.label('year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 1, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                presentation_query = (
                    db.session.query(presentation_sub_query)
                    .filter(presentation_sub_query.c.ranking <= 3)
                    .all()
                )

                presentation_results.extend(presentation_query)

            if presentation_results:
                for presentation in presentation_results:
                    type_exist = any(
                        type_info["id"] == presentation.eve_project_type_id
                        for type_info in project_types
                    )

                    if not type_exist:
                        project_types.append({
                            'id': presentation.eve_project_type_id,
                            'project_type_name': presentation.eve_project_type_name,
                            'departments': []
                        })

                    current_type = next(
                        (type_info for type_info in project_types if type_info['id']
                         == presentation.eve_project_type_id),
                        None
                    )

                    department_exist = any(
                        department['id'] == presentation.department_id
                        for department in current_type.get('departments', [])
                    )

                    if not department_exist:
                        current_type['departments'].append({
                            'id': presentation.department_id,
                            'department_name': presentation.department_name,
                            'years': []
                        })

                    current_department = next(
                        (department for department in current_type.get(
                            'departments', []) if department['id'] == presentation.department_id),
                        None
                    )

                    years_exist = any(
                        year['year'] == presentation.year
                        for year in current_department.get('years', [])
                    )

                    if not years_exist:
                        current_department['years'].append({
                            'year': presentation.year,
                            'ranks': []
                        })

                    current_year = next(
                        (year for year in current_department.get(
                            'years', []) if year['year'] == presentation.year),
                        None
                    )

                    rank_exist = any(
                        rank['rank'] == presentation.ranking
                        for rank in current_year.get('ranks', [])
                    )

                    if not rank_exist:
                        current_year['ranks'].append({
                            'rank': presentation.ranking,
                            'total_score': presentation.total_score,
                            'project': {}  # Initialize as an empty dictionary
                        })

                    current_rank = next(
                        (rank for rank in current_year.get('ranks', [])
                         if rank['rank'] == presentation.ranking),
                        None
                    )

                    current_rank['project'] = {
                        'project_code': presentation.code,
                        'project_topic': presentation.topic,
                        'project_members': []
                    }

                    members = []
                    eve_project_members = EveProjectMember.query.filter_by(
                        eve_project_id=presentation.project_id).all()

                    for member in eve_project_members:
                        members.append({
                            'id': member.id,
                            'name_latin': member.name_latin,
                            'name_khmer': member.name_khmer,
                            'sys_gender': {
                                'id': member.sys_gender.id,
                                'name_latin': member.sys_gender.name_latin
                            },
                            'page_index': page_index
                        })
                        page_index = page_index+1

                    current_rank = next(
                        item for item in current_year["ranks"] if item['rank'] == presentation.ranking)
                    # Assign the members list to the 'eve_project_members' key within the 'project' dictionary
                    current_rank["project"]['project_members'] = members
            return {
                'poster_year1': years[0],
                'poster_and_presentation_year2_up': project_types
            }, 200
        except Exception as e:
            print(e)
            return {"error": "something went wrong!!!"}, 500


@ns.route('/awards/posters/year1/all')
class Award(Resource):
    @ns.doc(security="jsonWebToken")
    @ns.marshal_with(output_poster_award_model)
    def get(self):
        try:
            # year 1 poster query result
            year1_subquery = (
                db.session.query(
                    EveProject.code.label('code'),
                    EveProject.topic.label('topic'),
                    EveResult.total_score.label('total_score'),
                    SysDepartment.name_latin.label('department'),
                    EveGeneration.year,
                    db.func.row_number().over(partition_by=EveGeneration.year,
                                              order_by=EveResult.total_score.desc()).label('ranking')
                )
                .join(EveProject, EveProject.id == EveResult.eve_project_id)
                .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                .filter(EveResult.eve_project_type_id == 2, EveGeneration.year == 'Year1')
                .subquery()
            )

            year1_poster_award_results = (
                db.session.query(year1_subquery)
                .filter(year1_subquery.c.ranking <= 3)
                .all()
            )

            years = []
            if year1_poster_award_results:
                for row in year1_poster_award_results:
                    # Check if the year is already in the list of years
                    year_exists = any(
                        item['year'] == row.year for item in years)

                    if not year_exists:
                        # If the year is not in the list, add it with an empty ranks list
                        years.append({
                            "year": row.year,
                            "ranks": []
                        })

                    # Get the year dictionary from the list
                    current_year = next(
                        item for item in years if item['year'] == row.year)

                    # Check if the rank is already in the project's rank list for the current year
                    rank_exists = any(
                        rank['rank'] == row.ranking for rank in current_year["ranks"])

                    if not rank_exists:
                        # If the rank is not in the list, add it
                        current_year["ranks"].append({
                            "rank": row.ranking,
                            "department": row.department,
                            "project": {
                                "code": row.code,
                                "topic": row.topic,
                            }
                        })

            return {"poster": {"years": years}}, 200
        except Exception as e:
            print(e)
            return {"error": "something went wrong!!!"}, 500


@ns.route('/awards/year2-up')
class Awards(Resource):
    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(output_project_type_award_result_model)
    def get(self):
        try:
            number_of_departments = len(SysDepartment.query.all())
            poster_results = []
            presentation_results = []
            project_types = []

            for sys_department_id in range(1, number_of_departments + 1):
                poster_sub_query = (
                    db.session.query(
                        EveProjectType.id.label('eve_project_type_id'),
                        EveProjectType.name_latin.label(
                            'eve_project_type_name'),
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.id.label('department_id'),
                        SysDepartment.name_latin.label('department_name'),
                        EveGeneration.year.label('year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 2, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                poster_query = (
                    db.session.query(poster_sub_query)
                    .filter(poster_sub_query.c.ranking <= 1)
                    .all()
                )

                poster_results.extend(poster_query)

            if poster_results:
                for poster in poster_results:
                    type_exist = any(
                        type_info["id"] == poster.eve_project_type_id
                        for type_info in project_types
                    )

                    if not type_exist:
                        project_types.append({
                            'id': poster.eve_project_type_id,
                            'project_type_name': poster.eve_project_type_name,
                            'departments': []
                        })

                    current_type = next(
                        (type_info for type_info in project_types if type_info['id'] == poster.eve_project_type_id),
                        None
                    )

                    department_exist = any(
                        department['id'] == poster.department_id
                        for department in current_type.get('departments', [])
                    )

                    if not department_exist:
                        current_type['departments'].append({
                            'id': poster.department_id,
                            'department_name': poster.department_name,
                            'years': []
                        })

                    current_department = next(
                        (department for department in current_type.get(
                            'departments', []) if department['id'] == poster.department_id),
                        None
                    )

                    years_exist = any(
                        year['year'] == poster.year
                        for year in current_department.get('years', [])
                    )

                    if not years_exist:
                        current_department['years'].append({
                            'year': poster.year,
                            'ranks': []
                        })

                    current_year = next(
                        (year for year in current_department.get(
                            'years', []) if year['year'] == poster.year),
                        None
                    )

                    rank_exist = any(
                        rank['rank'] == poster.ranking
                        for rank in current_year.get('ranks', [])
                    )

                    if not rank_exist:
                        current_year['ranks'].append({
                            'rank': poster.ranking,
                            'total_score': poster.total_score,
                            'projects': {}  # Initialize as an empty dictionary
                        })

                    current_rank = next(
                        (rank for rank in current_year.get('ranks', [])
                         if rank['rank'] == poster.ranking),
                        None
                    )

                    current_rank['projects'] = {
                        'project_code': poster.code,
                        'project_topic': poster.topic
                    }

            # for presentation
            for sys_department_id in range(1, number_of_departments+1):
                presentation_sub_query = (
                    db.session.query(
                        EveProjectType.id.label('eve_project_type_id'),
                        EveProjectType.name_latin.label(
                            'eve_project_type_name'),
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.id.label('department_id'),
                        SysDepartment.name_latin.label('department_name'),
                        EveGeneration.year.label('year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 1, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                presentation_query = (
                    db.session.query(presentation_sub_query)
                    .filter(presentation_sub_query.c.ranking <= 3)
                    .all()
                )

                presentation_results.extend(presentation_query)

            if presentation_results:
                for presentation in presentation_results:
                    type_exist = any(
                        type_info["id"] == presentation.eve_project_type_id
                        for type_info in project_types
                    )

                    if not type_exist:
                        project_types.append({
                            'id': presentation.eve_project_type_id,
                            'project_type_name': presentation.eve_project_type_name,
                            'departments': []
                        })

                    current_type = next(
                        (type_info for type_info in project_types if type_info['id']
                         == presentation.eve_project_type_id),
                        None
                    )

                    department_exist = any(
                        department['id'] == presentation.department_id
                        for department in current_type.get('departments', [])
                    )

                    if not department_exist:
                        current_type['departments'].append({
                            'id': presentation.department_id,
                            'department_name': presentation.department_name,
                            'years': []
                        })

                    current_department = next(
                        (department for department in current_type.get(
                            'departments', []) if department['id'] == presentation.department_id),
                        None
                    )

                    years_exist = any(
                        year['year'] == presentation.year
                        for year in current_department.get('years', [])
                    )

                    if not years_exist:
                        current_department['years'].append({
                            'year': presentation.year,
                            'ranks': []
                        })

                    current_year = next(
                        (year for year in current_department.get(
                            'years', []) if year['year'] == presentation.year),
                        None
                    )

                    rank_exist = any(
                        rank['rank'] == presentation.ranking
                        for rank in current_year.get('ranks', [])
                    )

                    if not rank_exist:
                        current_year['ranks'].append({
                            'rank': presentation.ranking,
                            'total_score': presentation.total_score,
                            'projects': {}  # Initialize as an empty dictionary
                        })

                    current_rank = next(
                        (rank for rank in current_year.get('ranks', [])
                         if rank['rank'] == presentation.ranking),
                        None
                    )

                    current_rank['projects'] = {
                        'project_code': presentation.code,
                        'project_topic': presentation.topic
                    }

            return {'project_types': project_types}, 200
        except Exception as e:
            print(e)
            return {"error": "something went wrong!!!"}, 500


@ns.route('/event/<int:eid>/best-supervisor')
class BestSupervisorssss(Resource):
    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(output_supervisor_by_department_model)
    def get(self, eid):
        try:
            best_supervisor_results = []
            number_of_departments = len(SysDepartment.query.all())

            year1_subquery = (
                db.session.query(
                    EveProject.code.label('code'),
                    EveProject.topic.label('topic'),
                    EveResult.total_score.label('total_score'),
                    SysDepartment.name_latin.label('department_name'),
                    EveSupervisor.id.label('supervisor_id'),
                    EveSupervisor.name_latin.label('supervisor_name_latin'),
                    EveSupervisor.name_khmer.label('name_khmer'),
                    EveGeneration.id.label('eve_generation_id'),
                    EveProject.eve_project_type_id,
                    EveGeneration.year.label('eve_generation_year'),
                    db.func.row_number().over(partition_by=EveGeneration.year,
                                              order_by=EveResult.total_score.desc()).label('ranking')
                )
                .join(EveProject, EveProject.id == EveResult.eve_project_id)
                .join(EveSupervisor, EveSupervisor.id == EveProject.eve_supervisor_id)
                .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                .filter(EveResult.eve_project_type_id == 2, EveGeneration.year == 'Year1', EveProject.eve_event_id == eid)
                .subquery()
            )

            poster_year1_results = (
                db.session.query(year1_subquery)
                .filter(year1_subquery.c.ranking <= 3)
                .all()
            )


            best_supervisor_results.extend(poster_year1_results)

            for sys_department_id in range(1, number_of_departments + 1):
                poster_sub_query = (
                    db.session.query(
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.name_latin.label('department_name'),
                        EveSupervisor.id.label('supervisor_id'),
                        EveSupervisor.name_latin.label(
                            'supervisor_name_latin'),
                        EveSupervisor.name_khmer.label('name_khmer'),
                        EveGeneration.id.label('eve_generation_id'),
                        EveProject.eve_project_type_id,
                        EveGeneration.year.label('eve_generation_year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveSupervisor, EveSupervisor.id == EveProject.eve_supervisor_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 2, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                poster_year2_up_query = (
                    db.session.query(poster_sub_query)
                    .filter(poster_sub_query.c.ranking <= 1)
                    .all()
                )

                best_supervisor_results.extend(poster_year2_up_query)

            # for presentation year1 to year4
            for sys_department_id in range(1, number_of_departments+1):
                presentation_sub_query = (
                    db.session.query(
                        EveProject.code.label('code'),
                        EveProject.topic.label('topic'),
                        EveResult.total_score.label('total_score'),
                        SysDepartment.name_latin.label('department_name'),
                        EveSupervisor.id.label('supervisor_id'),
                        EveSupervisor.name_latin.label(
                            'supervisor_name_latin'),
                        EveSupervisor.name_khmer.label('name_khmer'),
                        EveGeneration.id.label('eve_generation_id'),
                        EveProject.eve_project_type_id,
                        EveGeneration.year.label('eve_generation_year'),
                        db.func.row_number().over(partition_by=EveGeneration.year,
                                                  order_by=EveResult.total_score.desc()).label('ranking')
                    )
                    .join(EveProject, EveProject.id == EveResult.eve_project_id)
                    .join(EveSupervisor, EveSupervisor.id == EveProject.eve_supervisor_id)
                    .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
                    .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
                    .join(EveProjectType, EveProjectType.id == EveResult.eve_project_type_id)
                    .filter(EveResult.eve_project_type_id == 1, EveGeneration.year != 'Year1', SysDepartment.id == sys_department_id)
                    .subquery()
                )

                presentation_query = (
                    db.session.query(presentation_sub_query)
                    .filter(presentation_sub_query.c.ranking <= 3)
                    .all()
                )

                best_supervisor_results.extend(presentation_query)

            # Calculate scores and group supervisors by department
            supervisors_by_department = defaultdict(dict)
            department_scores = defaultdict(int)
            for result in best_supervisor_results:
                # Initialize medals
                gold = 0
                silver = 0
                bronze = 0
                # Calculate score based on the rules
                if result.eve_generation_year == "Year1" and result.eve_project_type_id == 2:
                    score = 4 if result.ranking == 1 else 2 if result.ranking == 2 else 1
                    # Assign medals based on score
                    gold = 1 if score == 4 else 0
                    silver = 1 if score == 2 else 0
                    bronze = 1 if score == 1 else 0

                elif result.eve_generation_year in ["Year2", "Year3", "Year4"] and result.eve_project_type_id == 2:
                    score = 1
                    gold = 1 if score == 1 else 0
                    silver = 0
                    bronze = 0

                elif result.eve_generation_year in ["Year2", "Year3", "Year4"] and result.eve_project_type_id == 1:
                    score = 8 if result.ranking == 1 else 4 if result.ranking == 2 else 2
                    # Assign medals based on score
                    gold = 1 if score == 8 else 0
                    silver = 1 if score == 4 else 0
                    bronze = 1 if score == 2 else 0

                # If supervisor already exists, add score, gold, silver, and bronze, else create new supervisor
                if result.supervisor_id in supervisors_by_department[result.department_name]:
                    supervisors_by_department[result.department_name][result.supervisor_id]['total_score'] += score
                    supervisors_by_department[result.department_name][result.supervisor_id]['total_gold'] += gold
                    supervisors_by_department[result.department_name][result.supervisor_id]['total_silver'] += silver
                    supervisors_by_department[result.department_name][result.supervisor_id]['total_bronze'] += bronze
                else:
                    supervisors_by_department[result.department_name][result.supervisor_id] = {
                        'name_latin': result.supervisor_name_latin,
                        'name_khmer': result.name_khmer,
                        'total_score': score,
                        'total_gold': gold,
                        'total_silver': silver,
                        'total_bronze': bronze
                    }

                department_scores[result.department_name] += score

            # Convert supervisors dictionaries to lists and sort by total score
            for department in supervisors_by_department:
                supervisors_by_department[department] = list(
                    supervisors_by_department[department].values())
                supervisors_by_department[department].sort(
                    key=lambda x: x['total_score'], reverse=True)

            # Create a list of dictionaries and sort by total department score
            output = [{'department_name': department, 'total_score': department_scores[department],
                       'supervisors': supervisors} for department, supervisors in supervisors_by_department.items()]
            output.sort(key=lambda x: x['total_score'], reverse=True)

            return output, 200
        except Exception as e:
            print(e)
            return {"error": "something went wrong!!!"}, 500
