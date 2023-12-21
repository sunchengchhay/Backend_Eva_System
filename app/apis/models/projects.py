from app.apis.models.user_infos import output_same_state_model
from app.apis.models.events import output_event_model
from flask_restx import fields

from app.extensions import api
from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

input_eve_project_model = api.model(
    'Input Project', {
        "code": fields.String(required=True, description='Code'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
        "sys_department_id": fields.Integer(required=True, description='Department'),
        "topic": fields.String(required=True, description='Topic'),
        "eve_project_type_id": fields.Integer(required=True, description='Project Type'),
        "eve_generation_id": fields.Integer(required=True, description='Generation'),
        "member1_name_latin": fields.String(required=True, description='Member 1'),
        "member1_name_khmer": fields.String(required=True, description='Member 1'),
        "member2_name_latin": fields.String(required=False, description='Member 2'),
        "member2_name_khmer": fields.String(required=False, description='Member 2'),
        "member3_name_latin": fields.String(required=False, description='Member 3'),
        "member3_name_khmer": fields.String(required=False, description='Member 3'),
        "member4_name_latin": fields.String(required=False, description='Member 4'),
        "member4_name_khmer": fields.String(required=False, description='Member 4'),
        "member5_name_latin": fields.String(required=False, description='Member 5'),
        "member5_name_khmer": fields.String(required=False, description='Member 5'),
        "eve_supervisor_id": fields.Integer(required=True, description='Supervisor'),
        "contact_name": fields.String(required=True, description='Contact Name'),
        "telegram_number": fields.String(required=True, description='Telegram Number'),
        "email_address": fields.String(description='Email Address'),
    }
)

update_eve_project_model = api.model(
    'Update Project', {
        "code": fields.String(required=True, description='Code'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
        "sys_department_id": fields.Integer(required=True, description='Department'),
        "topic": fields.String(required=True, description='Topic'),
        "eve_project_type_id": fields.Integer(required=True, description='Project Type'),
        "eve_generation_id": fields.Integer(required=True, description='Generation'),
        "member1_name_latin": fields.String(required=True, description='Member 1'),
        "member1_name_khmer": fields.String(required=True, description='Member 1'),
        "member2_name_latin": fields.String(description='Member 2'),
        "member2_name_khmer": fields.String(description='Member 2'),
        "member3_name_latin": fields.String(description='Member 3'),
        "member3_name_khmer": fields.String(description='Member 3'),
        "member4_name_latin": fields.String(description='Member 4'),
        "member4_name_khmer": fields.String(description='Member 4'),
        "member5_name_latin": fields.String(description='Member 5'),
        "member5_name_khmer": fields.String(description='Member 5'),
        "eve_supervisor_id": fields.Integer(required=True, description='Supervisor'),
        "contact_name": fields.String(required=True, description='Contact Name'),
        "telegram_number": fields.String(required=True, description='Telegram Number'),
        "email_address": fields.String(description='Email Address'),
    }
)
input_eve_project_type_model = api.model(
    'Input Project Type', {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "eve_event_id": fields.Integer(required=True, description='Event ID'),
    }
)

output_eve_project_type_model = api.model(
    'Output Project Type', {
        "id": fields.Integer(description='ID'),
        "name_latin": fields.String(description='Name Latin'),
        "eve_event_id": fields.Integer(description='Event ID'),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(description='Created at'),
        "updated_by": fields.Integer(description='Updated by'),
        "updated_at": fields.DateTime(description='Updated at')
    }
)


update_eve_project_type_model = api.model(
    'Update Project Type', {
        "name_latin": fields.String(required=True, description='Name Latin'),
        "eve_event_id": fields.Integer(required=True, description='Event ID'),
    }
)

input_eve_project_shortlist_model = api.model(
    'Input Project Shortlist', {
        "eve_event_id": fields.Integer(required=True, description='Event'),
        "eve_project_id": fields.Integer(required=True, description='Project'),
        "eve_project_type_id": fields.Integer(required=True, description='Shortlist Type'),
    }
)


update_eve_project_shortlist_model = api.model(
    'Update Project Shortlist', {
        "eve_event_id": fields.Integer(required=True, description='Event'),
        "eve_project_id": fields.Integer(required=True, description='Project'),
        "eve_project_type_id": fields.Integer(required=True, description='Shortlist Type'),
    }
)

input_eve_project_committee_model = api.model(
    'Input Project Committee', {
        "eve_committee_id": fields.Integer(required=True, description='Committee'),
        "eve_project_shortlist_id": fields.Integer(required=True, description='Project Shortlist'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
    }
)

output_eve_project_committee_model = api.model(
    'Output Project Committee', {
        "id": fields.Integer(description='ID'),
        "eve_committee_id": fields.Integer(description='Committee'),
        "eve_project_shortlist_id": fields.Integer(description='Project Shortlist'),
        "eve_event_id": fields.Integer(description='Event'),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(description='Created at'),
        "updated_by": fields.Integer(description='Updated by'),
        "updated_at": fields.DateTime(description='Updated at')
    }
)

update_eve_project_committee_model = api.model(
    'Update Project Committee', {
        "eve_committee_id": fields.Integer(required=True, description='Committee'),
        "eve_project_shortlist_id": fields.Integer(required=True, description='Project Shortlist'),
        "eve_event_id": fields.Integer(required=True, description='Event'),
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
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(required=True, default=1, description='Updated by'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
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

input_eve_supervisor_model = api.model(
    'Input Event Supervisor', {
        "name_latin": fields.String(required=True),
        "name_khmer": fields.String(required=True),
        "created_by": fields.Integer(default=1, description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(default=1, required=True, description='Updated by'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
    }
)

output_eve_supervisor_model = api.model(
    'Output Event Supervisor', {
        "id": fields.Integer(),
        "name_latin": fields.String(),
        "name_khmer": fields.String(),
        "created_by": fields.Integer(default=1, description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(default=1, required=True, description='Updated by'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
    }
)

update_eve_supervisor_model = api.model(
    'Update Event Supervisor', {
        "name_latin": fields.String(required=True),
        "name_khmer": fields.String(required=True),
        "updated_by": fields.Integer(default=1, required=True, description='Updated by'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
    }
)


output_eve_project_model = api.model(
    'Output Project', {
        "id": fields.Integer(description='ID'),
        "code": fields.String(description='Code'),
        # "eve_event_id": fields.Integer(description='Event'),
        "eve_event": fields.List(fields.Nested(output_event_model)),
        # "sys_department_id": fields.Integer(description='Department'),
        "sys_department": fields.List(fields.Nested(output_same_state_model)),
        "topic": fields.String(description='Topic'),
        # "eve_project_type_id": fields.Integer(description='Project Type'),
        "eve_project_type": fields.List(fields.Nested(output_eve_project_type_model)),
        "eve_generation_id": fields.Integer(description='Generation'),
        "eve_generation": fields.List(fields.Nested(output_eve_generation_model)),
        "member1_name_latin": fields.String(description='Member 1'),
        "member1_name_khmer": fields.String(description='Member 1'),
        "member2_name_latin": fields.String(description='Member 2'),
        "member2_name_khmer": fields.String(description='Member 2'),
        "member3_name_latin": fields.String(description='Member 3'),
        "member3_name_khmer": fields.String(description='Member 3'),
        "member4_name_latin": fields.String(description='Member 4'),
        "member4_name_khmer": fields.String(description='Member 4'),
        "member5_name_latin": fields.String(description='Member 5'),
        "member5_name_khmer": fields.String(description='Member 5'),
        "eve_supervisor_id": fields.Integer(description='Supervisor'),
        "contact_name": fields.String(description='Contact Name'),
        "telegram_number": fields.String(description='Telegram Number'),
        "email_address": fields.String(description='Email Address'),
        "created_by": fields.Integer(default=1, description='Created by'),
        "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
        "updated_by": fields.Integer(default=1, description='Updated by'),
        "updated_at": fields.DateTime(default=time_cambodia, description='Updated at')
    }
)

output_eve_project_shortlist_model = api.model(
    'Output Project Shortlist', {
        "id": fields.Integer(description='ID'),
        # "eve_event_id": fields.Integer(description='Event'),
        "eve_event": fields.List(fields.Nested(output_event_model)),
        # "eve_project_id": fields.Integer(description='Project'),
        "eve_project": fields.List(fields.Nested(output_eve_project_model)),
        # "eve_project_type_id": fields.Integer(description='Shortlist Type'),
        "eve_project_type": fields.List(fields.Nested(output_eve_project_type_model)),
        "created_by": fields.Integer(description='Created by'),
        "created_at": fields.DateTime(description='Created at'),
        "updated_by": fields.Integer(description='Updated by'),
        "updated_at": fields.DateTime(description='Updated at')
    }
)
