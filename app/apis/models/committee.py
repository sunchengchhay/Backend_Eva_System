from flask_restx import fields

from app.extensions import api
from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

input_eve_committee_model = api.model(
    'Input Event Committee', {
        "sys_person_id": fields.Integer(required=True),
        "eve_event_id": fields.Integer(required=True),
    }
)

output_eve_committee_model = api.model(
    'Output Event Committee',
    {
        "id": fields.Integer(),
        "sys_person_id": fields.Integer(),
        "eve_event_id": fields.Integer(),
        "created_by": fields.Integer(default=1),
        "created_at": fields.DateTime(default=current_time_cambodia()),
        "updated_by": fields.Integer(default=1),
        "updated_at": fields.DateTime(default=current_time_cambodia())
    }
)

update_eve_committee_model = api.model(
    'Update Event Committee',
    {
        "sys_person_id": fields.Integer(),
        "eve_event_id": fields.Integer(),
    }
)

input_eve_committee_score = api.model(
    'Input Event Committee Score',
    {
        "eve_committee_id": fields.Integer(required=True),
        "eve_project_shortlist_id": fields.Integer(required=True),
        "eve_event_id": fields.Integer(required=True),
        "eve_eval_criteria_id": fields.Integer(required=True),
        "score": fields.Float(default=0),
        "is_locked": fields.Boolean(default=False),
    }
)

output_eve_committee_score = api.model(
    'Output Event Committee Score',
    {
        "id": fields.Integer(),
        "eve_committee_id": fields.Integer(),
        "eve_project_shortlist_id": fields.Integer(),
        "eve_event_id": fields.Integer(),
        "eve_eval_criteria_id": fields.Integer(),
        "score": fields.Float(),
        "is_locked": fields.Boolean(default=False),
        "created_by": fields.Integer(default=1),
        "created_at": fields.DateTime(default=current_time_cambodia()),
        "updated_by": fields.Integer(default=1),
        "updated_at": fields.DateTime(default=current_time_cambodia())
    }
)
update_eve_committee_score = api.model(
    'Update Event Committee Score',
    {
        "eve_committee_id": fields.Integer(required=True),
        "eve_project_shortlist_id": fields.Integer(required=True),
        "eve_event_id": fields.Integer(required=True),
        "eve_eval_criteria_id": fields.Integer(required=True),
        "score": fields.Float(required=True),
        "is_locked": fields.Boolean(default=False),
    }
)
