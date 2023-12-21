from flask_restx import fields

from app.extensions import api
from app.customs.cambodia_datetime import current_time_cambodia, custom_datetime_cambodia

input_same_state_model = api.model(
    "SameStateInput",
    {
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
    }
)

output_same_state_model = api.model(
    "SameStateOutput",
    {
        "id": fields.Integer(),
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "created_by": fields.Integer(),
        "created_at": fields.DateTime(),
        "updated_by": fields.Integer(),
        "updated_at": fields.DateTime(),
    }
)

update_same_state_model = api.model(
    "SameStateUpdate",
    {
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
    }
)

input_eve_generation_model = api.model(
    'Input Event Generation', {
        "eve_event_id": fields.Integer(required=True),
        "sys_department_id": fields.Integer(required=True),
        "name_latin": fields.String(required=True),
        "year": fields.String(required=True),
    }
)

output_eve_generation_model = api.model(
    'Output Event Generation', {
        "id": fields.Integer(),
        "eve_event_id": fields.Integer(required=True),
        "sys_department_id": fields.Integer(required=True),
        "name_latin": fields.String(required=True),
        "year": fields.String(required=True),
        "created_by": fields.Integer(required=True, default=1, description='Created by'),
        "created_at": fields.DateTime(default=current_time_cambodia(), description='Created at'),
        "updated_by": fields.Integer(required=True, default=1, description='Updated by'),
        "updated_at": fields.DateTime(default=current_time_cambodia(), description='Updated at')
    }
)

update_eve_generation_model = api.model(
    'Update Event Generation', {
        "eve_event_id": fields.Integer(required=True),
        "sys_department_id": fields.Integer(required=True),
        "name_latin": fields.String(required=True),
        "year": fields.String(required=True),
    }
)



input_event_model = api.model(
    'EventInput',
    {
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "description": fields.String(),
        "start_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 7:00:00')),
        "end_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 17:00:00')),
        "photo_url": fields.String(default="null"),
    }
)

output_event_model = api.model(
    'EventOutput',
    {
        "id": fields.Integer(),
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "description": fields.String(),
        "start_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 7:00:00')),
        "end_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 17:00:00')),
        "photo_url": fields.String(default="null"),
        "created_by": fields.Integer(default=1),
        "created_at": fields.DateTime(default=current_time_cambodia()),
        "updated_by": fields.Integer(default=1),
        "updated_at": fields.DateTime(default=current_time_cambodia()),
    }
)


update_event_model = api.model(
    'EventUpdate',
    {
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "description": fields.String(),
        "start_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 7:00:00')),
        "end_date": fields.DateTime(default=custom_datetime_cambodia('2023-12-09 17:00:00')),
        "photo_url": fields.String(default="null"),
    }
)
