from sqlalchemy import func
from app.views.auth import auth_bp
from app.views.admin import *
from app.models import *
from app.extensions import db, blueprint_api
import pandas as pd
from io import BytesIO
from flask import send_file


def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blueprint_api)


class CustomExportView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    @expose('/export', methods=['GET'])
    def get(self):
        best_supervisor_results = []
        number_of_departments = len(SysDepartment.query.all())

        year1_subquery = (
            db.session.query(
                db.func.row_number().over(partition_by=EveGeneration.year,
                                          order_by=EveResult.total_score.desc()).label('ranking'),
                EveResult.total_score.label('total_score'),
                SysDepartment.name_latin.label('department_name'),
                EveGeneration.name_latin.label('eve_generation'),
                EveGeneration.year.label('eve_generation_year'),
                EveProject.code.label('code'),
                EveProject.topic.label('topic'),
                EveSupervisor.name_latin.label(
                    'supervisor_name_latin')
            )
            .join(EveProject, EveProject.id == EveResult.eve_project_id)
            .join(EveSupervisor, EveSupervisor.id == EveProject.eve_supervisor_id)
            .join(EveGeneration, EveGeneration.id == EveProject.eve_generation_id)
            .join(SysDepartment, SysDepartment.id == EveProject.sys_department_id)
            .filter(EveResult.eve_project_type_id == 2, EveGeneration.year == 'Year1', EveProject.eve_event_id == 1)
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
                    db.func.row_number().over(partition_by=EveGeneration.year,
                                              order_by=EveResult.total_score.desc()).label('ranking'),
                    EveResult.total_score.label('total_score'),
                    SysDepartment.name_latin.label('department_name'),
                    EveGeneration.name_latin.label('eve_generation'),
                    EveGeneration.year.label('eve_generation_year'),
                    EveProject.code.label('code'),
                    EveProject.topic.label('topic'),
                    EveSupervisor.name_latin.label(
                        'supervisor_name_latin')
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
                    db.func.row_number().over(partition_by=EveGeneration.year,
                                              order_by=EveResult.total_score.desc()).label('ranking'),
                    EveResult.total_score.label('total_score'),
                    SysDepartment.name_latin.label('department_name'),
                    EveGeneration.name_latin.label('eve_generation'),
                    EveGeneration.year.label('eve_generation_year'),
                    EveProject.code.label('code'),
                    EveProject.topic.label('topic'),
                    EveSupervisor.name_latin.label(
                        'supervisor_name_latin')
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

        # # Create a DataFrame from the result
        df = pd.DataFrame(
            best_supervisor_results,
            columns=[
                'Rank', 'Total_Score', 'Department', 'Generation', 'Study_Year',
                'Project Code', 'Project Topic',
                'Supervisor'
            ]
        )
        # Round the 'Total_Score' column to 2 decimal places
        df['Total_Score'] = df['Total_Score'].round(2)

        # Add a new column 'Project Member' to store project members
        df['Project Member'] = ''

        # Fetch project members for each project
        for index, row in df.iterrows():
            eve_project = EveProject.query.filter_by(
                code=row['Project Code']).first()
            if eve_project:
                eve_members = EveProjectMember.query.filter_by(
                    eve_project_id=eve_project.id).all()
                if eve_members:
                    members_str = ', '.join(
                        member.name_latin for member in eve_members)
                    df.at[index, 'Project Member'] = members_str

        # Create an in-memory Excel file
        excel_data = BytesIO()
        df.to_excel(excel_data, index=False)

        # Seek to the beginning of the file before sending it
        excel_data.seek(0)

        # Send the Excel file as a response
        return send_file(
            excel_data,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='result.xlsx'
        )


def add_views(admin):
    admin.add_views(
        SysUserModelView(
            SysUser, db.session, name='User Management'),
        SysPersonModel(
            SysPerson, db.session, name='User Profile Management'
        ),
        SysGenderModel(
            SysGender, db.session, name='Gender Management'
        ),
        SysNationalityModel(
            SysNationality, db.session, name='Nationality Management'
        ),
        SysDepartmentModel(
            SysDepartment, db.session, name='Department Management'
        ),
        SysPositionModel(
            SysPosition, db.session, name='Position Management'
        ),
        SysOrganizationModel(
            SysOrganization, db.session, name='Organization Management'
        ),
        SysProfileModel(
            SysProfile, db.session, name='Role Management'
        ),
        SysRightModel(
            SysRight, db.session, name='Right Management'
        ),
        SysProfileAccessRightModel(
            SysProfileAccessRight, db.session, name='Profile Access Right Management'
        ),
        SysMenuModel(
            SysMenu, db.session, name='Menu Management'
        ),
        SysSubMenuModel(
            SysSubMenu, db.session, name='Sub Menu Management'
        ),
        EveCommitteeModel(
            EveCommittee, db.session, name='Committee Management'),
        EveGenerationModel(
            EveGeneration, db.session, name='Generation Management'
        ),
        EveProjectCommitteeModel(
            EveProjectCommittee, db.session, name='Project Committee Management'
        ),
        EveEventModel(
            EveEvent, db.session, name='Event Management'
        ),
        EveResultModel(
            EveResult, db.session, name='Result Management'
        ),
        EveProjectModel(
            EveProject, db.session, name='Project Management'
        ),
        EveProjectShortlistModel(
            EveProjectShortlist, db.session, name='Project Shortlist Management'
        ),
        EveSupervisorModel(
            EveSupervisor, db.session, name='Supervisor Management'
        ),
        EveProjectTypeModel(
            EveProjectType, db.session, name='Project Type Management'
        ),
        EveEvalCategoryModel(
            EveEvalCategory, db.session, name='Evaluation Category Management'
        ),
        EveEvalCriteriaModel(
            EveEvalCriteria, db.session, name='Evaluation Criteria Management'
        ),
        EveRubricCategoryModel(
            EveRubricCategory, db.session, name='Evaluation Rubic Category Management'
        ),
        EveEvalCriteriaRubricModel(
            EveEvalCriteriaRubric, db.session, name='Evaluation Rubic Criteria Management'
        ),
        EveCommitteeScoreModel(
            EveCommitteeScore, db.session, name='Committee Score Management'
        ),
        EveProjectMemberModel(
            EveProjectMember, db.session, name='Project Member Management'
        )
    )
