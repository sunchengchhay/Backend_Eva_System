from app.apis.models.projects import output_eve_project_model
from app.extensions import api
from flask_restx import fields

from app.models.events import EveProject

# evaluation form get
output_eve_eval_form_model = api.model(
    'Output Event Evaluation Form', {
        "category_name": fields.String(),
        "category_weight": fields.Float(),
        "criteria_name": fields.String(),
        "criteria_score": fields.List(fields.Integer)
    }
)
output_eve_eval_criteria_form = api.model(
    'Output Criteria', {
        "id": fields.Integer(),
        "name": fields.String(),
        "score": fields.List(fields.Integer)
    }
)

output_eve_eval_category_form = api.model(
    'Output Category', {
        "id": fields.Integer(),
        "name": fields.String(),
        "weight": fields.Float(),
        "criteria": fields.List(fields.Nested(output_eve_eval_criteria_form))
    }
)


output_eve_eval_category_forms = api.model(
    'Output Categories', {
        'project_code': fields.String(),
        'project_topic': fields.String(),
        'category': fields.List(fields.Nested(output_eve_eval_category_form))
    }
)
# project shortlist get version 1
output_project_model = api.model('OutPut Project', {
    "id": fields.Integer(description='ID'),
    "code": fields.String(description='Code'),
    "eve_event_id": fields.Integer(description='Event'),
    "sys_department_id": fields.Integer(description='Department'),
    "topic": fields.String(description='Topic'),
    "eve_project_type_id": fields.Integer(description='Project Type'),
    "eve_generation_id": fields.Integer(description='Generation'),
    "eve_supervisor_id": fields.Integer(description='Supervisor'),
    "contact_name": fields.String(description='Contact Name'),
    "telegram_number": fields.String(description='Telegram Number'),
    "email_address": fields.String(description='Email Address'),
    "created_by": fields.Integer(),
    "created_at": fields.DateTime(),
    "updated_by": fields.Integer(),
    "updated_at": fields.DateTime()
})


output_project_filter_model = api.model('Filter Project', {
    'id': fields.Integer(),
    'project_type': fields.String(),
    'eve_project': fields.List(fields.Nested(output_project_model)),
    'judge': fields.Integer()
})

output_filter_project_shortlist_model = api.model(
    'Search Project Shortlist', {
        'shortlist_projects': fields.List(fields.Nested(output_project_filter_model))
    }
)

# form fields post
input_eve_project_results_model = api.model(
    'Project Result Input', {
        "criteria_id": fields.Integer(),
        "score": fields.Integer(),
    }
)

input_eve_project_score_model = api.model(
    'Project Score Input', {
        'project_id': fields.Integer(),
        'committee_id': fields.Integer(),
        'comment': fields.String(),
        'results': fields.List(fields.Nested(input_eve_project_results_model))
    }
)

# project shortlist get version 2 ( search by event_id , department_id and Year)
output_committee_model = api.model(
    'Committee Output', {
        'id': fields.Integer(),
        'name': fields.String(),
        'is_evaluated': fields.Boolean(),
        'project_score': fields.Float()
    }
)

output_sys_gender_model = api.model(
    'Gender Output', {
        "id": fields.Integer(),
        "name_latin": fields.String()
    }
)

output_project_member_model = api.model(
    'Project Member Output', {
        "id": fields.Integer(),
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "sys_gender": fields.Nested(output_sys_gender_model)
    }
)

output_project_member_certificate_model = api.model(
    'Project Member Output', {
        "id": fields.Integer(),
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "sys_gender": fields.Nested(output_sys_gender_model),
        "page_index": fields.Integer
    }
)

output_custom_project_shortlist_model = api.model(
    'Custom Project Shortlist Output', {
        'eve_shortlist_id': fields.Integer(),
        'eve_event_name': fields.String(),
        'eve_project_type': fields.String(),
        'eve_project_id': fields.Integer(),
        'eve_project_code': fields.String(),
        'eve_project_topic': fields.String(),
        'eve_project_generation': fields.String(),
        'eve_project_department': fields.String(),
        'eve_project_year': fields.String(),
        'eve_project_supervisor_name': fields.String(),
        'project_total_score': fields.Float(),
        'eve_project_committee': fields.List(fields.Nested(output_committee_model)),
        'eve_project_members': fields.List(fields.Nested(output_project_member_model))
    }
)


# show project_shortlist by committee
output_criteria_model = api.model(
    'Criterias Model Output', {
        "id": fields.Integer,
        "name": fields.String,
        "score": fields.Integer,
        "eva_score": fields.List(fields.Integer),
        "rubric": fields.String
    }
)

output_eval_form_model = api.model(
    'Eval Model Output', {
        "id": fields.Integer,
        "name": fields.String,
        "criterias": fields.List(fields.Nested(output_criteria_model))
    }
)

output_project_model = api.model(
    'Porject Ouput Model', {
        "id": fields.Integer,
        "code": fields.String,
        "topic": fields.String,
        "total_score": fields.Integer,
        "comment": fields.String,
        "categories": fields.List(fields.Nested(output_eval_form_model))
    }
)

output_all_committee_score_data_model = api.model(
    'Output Data', {
        "id": fields.Integer,
        "name": fields.String,
        "projects": fields.List(fields.Nested(output_project_model))}
)


output_all_committee_score = api.model(
    'Output Data', {
        "committees": fields.List(fields.Nested(output_all_committee_score_data_model))
    }
)


# new version of project detial
output_committee_detial_model = api.model(
    'Committee Output', {
        'id': fields.Integer(),
        'name': fields.String(),
        'project_score': fields.Float(),
        'comment': fields.String,
        "categories": fields.List(fields.Nested(output_eval_form_model))
    }
)


output_project_shortlist_detial_model = api.model(
    'Custom Project Shortlist Output', {
        'eve_shortlist_id': fields.Integer(),
        'eve_project_type': fields.String(),
        'eve_project_code': fields.String(),
        'eve_project_topic': fields.String(),
        'eve_project_generation': fields.String(),
        'eve_project_department': fields.String(),
        'eve_project_year': fields.String(),
        'eve_project_supervisor_name': fields.String(),
        'eve_project_total_score': fields.Float(),
        'eve_project_committee': fields.List(fields.Nested(output_committee_detial_model)),
        'eve_project_members': fields.List(fields.Nested(output_project_member_model))
    }
)


# poster year 1 result
output_poster_year_rank_project_model = api.model(
    'Poster Year Rank Project Model', {
        # 'id': fields.Integer(),
        'code': fields.String(),
        'topic': fields.String()
    }
)

output_poster_year_rank_model = api.model(
    'Poster Year Rank Model', {
        "rank": fields.Integer(),
        "department": fields.String(),
        "project": fields.Nested(output_poster_year_rank_project_model)
    }
)

output_poster_year_model = api.model(
    'Poster Year Model', {
        "year": fields.String(),
        "ranks": fields.List(fields.Nested(output_poster_year_rank_model))
    }
)

output_poster_award_detial_model = api.model(
    'Poster Award Detial Model', {
        "years": fields.List(fields.Nested(output_poster_year_model))
    }
)

output_poster_award_model = api.model(
    'Poster Output Model', {
        "poster": fields.Nested(output_poster_award_detial_model)
    }
)
# end poster year 1


# poster and present year 2 up result
output_project_detial_model = api.model(
    'Project Detial Model', {
        'project_code': fields.String(),
        'project_topic': fields.String()
    }
)

output_ranking_detial_model = api.model(
    'Ranking Detial Model', {
        'rank': fields.Integer(),
        'total_score': fields.Float(),
        'projects': fields.Nested(output_project_detial_model)
    }
)

output_year_detial_model = api.model(
    'Year Detial Model', {
        'year': fields.String(),
        'ranks': fields.List(fields.Nested(output_ranking_detial_model))
    }
)

output_departments_detial_model = api.model(
    'Department Detial Model', {
        'id': fields.Integer(),
        'department_name': fields.String(),
        'years': fields.List(fields.Nested(output_year_detial_model))
    }
)

output_type_detial_model = api.model(
    'Type Detial Model', {
        'id': fields.Integer(),
        'project_type_name': fields.String(),
        'departments': fields.List(fields.Nested(output_departments_detial_model))
    }
)

output_project_type_award_result_model = api.model(
    'Award By Project Type Year2 up', {
        'project_types': fields.List(fields.Nested(output_type_detial_model))
    }
)
# end poster and present year2 up #

# certificate model
# poster year 1 result
output_certificate_poster_year_rank_project_model = api.model(
    'Poster Year Rank Project Model', {
        'project_code': fields.String(),
        'project_topic': fields.String(),
        'project_members': fields.List(fields.Nested(output_project_member_certificate_model))
    }
)

output_certificate_poster_year_rank_model = api.model(
    'Poster Year Rank Model', {
        "rank": fields.Integer(),
        "department": fields.String(),
        "project": fields.Nested(output_certificate_poster_year_rank_project_model)
    }
)

output_certificate_poster_year_model = api.model(
    'Poster Year Model', {
        "year": fields.String(),
        "ranks": fields.List(fields.Nested(output_certificate_poster_year_rank_model))
    }
)

# end poster year 1

output_certificate_project_detial_model = api.model(
    'Project Detial Model', {
        'project_code': fields.String(),
        'project_topic': fields.String(),
        'project_members': fields.List(fields.Nested(output_project_member_certificate_model))
    }
)

output_certificate_ranking_detial_model = api.model(
    'Ranking Detial Model', {
        'rank': fields.Integer(),
        'total_score': fields.Float(),
        'project': fields.Nested(output_certificate_project_detial_model)
    }
)

output_certificate_year_detial_model = api.model(
    'Year Detial Model', {
        'year': fields.String(),
        'ranks': fields.List(fields.Nested(output_certificate_ranking_detial_model))
    }
)

output_certificate_departments_detial_model = api.model(
    'Department Detial Model', {
        'id': fields.Integer(),
        'department_name': fields.String(),
        'years': fields.List(fields.Nested(output_certificate_year_detial_model))
    }
)

output_certicate_type_detial_model = api.model(
    'Type Detial Model', {
        'id': fields.Integer(),
        'project_type_name': fields.String(),
        'departments': fields.List(fields.Nested(output_certificate_departments_detial_model))
    }
)

output_cerificate_result_model = api.model(
    'Award By Project Type Year2 up', {
        'poster_year1': fields.Nested(output_certificate_poster_year_model),
        'poster_and_presentation_year2_up': fields.List(fields.Nested(output_certicate_type_detial_model))
    }
)
# end certificate


# best supervisors
output_supervisor_model = api.model(
    'Supervisor Model', {
        'name_latin': fields.String(),
        'name_khmer': fields.String(),
        'total_score': fields.Float(),
        'total_gold': fields.Integer(),
        'total_silver': fields.Integer(),
        'total_bronze': fields.Integer()
    }
)
output_supervisor_by_department_model = api.model(
    'Supervisor By Department Model', {
        'department_name': fields.String(),
        'supervisors': fields.List(fields.Nested(output_supervisor_model))
    }
)
