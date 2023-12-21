from flask_restx import fields

from app.extensions import api
from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

input_eve_eval_category_model = api.model(
    'Input Evaluation Category',
    {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "weight": fields.Float(required=True, description='Weight'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
    }
)

output_eve_eval_category_model = api.model(
    'Output Evaluation Category',
    {
        "id": fields.Integer(description='ID'),
        "name_latin": fields.String(description='Name Latin'),
        "weight": fields.Float(description='Weight'),
        "eve_event_id": fields.Integer(description='Event'),
        "created_by": fields.Integer(default=1, description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(default=1, description='Updated by'),
        "updated_at": fields.DateTime(deualt=time_cambodia, description='Updated at')
    }
)

update_eve_eval_category_model = api.model(
    'Update Evaluation Category',
    {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "weight": fields.Float(required=True, description='Weight'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
    }
)

input_eve_eval_criteria_model = api.model(
    'Input EveEval Criteria',
    {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "eve_eval_category_id": fields.Integer(required=True, description='Eve Eval Category'),
        "eve_event_id": fields.Integer(required=True, description='Eve Event'),
    }
)

output_eve_eval_criteria_model = api.model(
    'Output EveEval Criteria',
    {
        "id": fields.Integer(),
        "name_latin": fields.String(description='Name Latin'),
        "eve_eval_category_id": fields.Integer(description='Eve Eval Category'),
        "eve_event_id": fields.Integer(description='Eve Event'),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(description='Updated By'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
    }
)

update_eve_eval_criteria_model = api.model(
    'Update EveEval Criteria',
    {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "eve_eval_category_id": fields.Integer(required=True, description='Eval Category'),
        "eve_event_id": fields.Integer(required=True, description='Event id'),
    }
)

input_eve_eval_criteria_rubric_model = api.model(
    'Input EveEval Critria rubric',
    {
        "eve_eval_criteria_id": fields.Integer(required=True, description='Eval Criteria Id'),
        "eve_event_id": fields.Integer(required=True, description='Event Id'),
        "score": fields.Float(description='Score'),
        "eve_rubric_category_id": fields.Integer(required=True, description='Rubric category id'),
    }
)

output_eve_eval_criteria_rubric_model = api.model(
    'Output Evaluation Criteria rubric',
    {
        "id": fields.Integer(description="id"),
        "eve_eval_criteria_id": fields.Integer(description='Eval Criteria Id'),
        "eve_event_id": fields.Integer(description='Event Id'),
        "score": fields.Float(description='Score'),
        "eve_rubric_category_id": fields.Integer(description='Rubric category id'),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia),
        "updated_by": fields.Integer(),
        "updated_at": fields.DateTime(default=time_cambodia)
    }
)

update_eve_eval_criteria_rubric_model = api.model(
    'Update evaluation criteria rubric',
    {
        "eve_eval_criteria_id": fields.Integer(required=True, description='Eval Criteria Id'),
        "eve_event_id": fields.Integer(required=True, description='Event Id'),
        "score": fields.Float(description='Score'),
        "eve_rubric_category_id": fields.Integer(required=True, description='Rubric category id'),
    }
)

input_eve_rubric_category_model = api.model(
    'Input Event Rubric Category',
    {
        "name_latin": fields.String(required=True, description='name latin'),
        "eve_event_id": fields.Integer(required=True, description='Event Id'),
    }
)

output_eve_rubric_category_model = api.model(
    'Output Event Rubric Category',
    {
        "id": fields.Integer(description='Id'),
        "name_latin": fields.String(description='name latin'),
        "eve_event_id": fields.Integer(description='Event Id'),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia),
        "updated_by": fields.Integer(description='Created by'),
        "updated_at": fields.DateTime(),
    }
)

update_eve_rubric_category_model = api.model(
    'Update Event Rubric Category',
    {
        "name_latin": fields.String(required=True, description='name latin'),
        "eve_event_id": fields.Integer(required=True, description='Event Id'),
    }
)

output_eve_result = api.model(
    'Output Event Result',
    {
        "id": fields.Integer(),
        "eve_project_shortlist_id": fields.Integer(),
        "eve_project_id": fields.Integer(),
        "eve_generation_id": fields.Integer(),
        "shortlist_type": fields.Raw(),
        "total_score": fields.Float(),
        "is_locked": fields.Boolean(),
        "created_by": fields.Integer(),
        "created_at": fields.DateTime(),
        "updated_by": fields.Integer(),
        "updated_at": fields.DateTime()
    }
)

update_eve_result = api.model(
    'Update Event Result',
    {
        "eve_project_shortlist_id": fields.Integer(),
        "eve_project_id": fields.Integer(),
        "eve_generation_id": fields.Integer(),
        "shortlist_type": fields.Raw(enum=["Presentation", "Poster"]),
        "total_score": fields.Float(),
        "is_locked": fields.Boolean(),
        "updated_by": fields.Integer(default=1),
        "updated_at": fields.DateTime(default=current_time_cambodia())
    }
)
