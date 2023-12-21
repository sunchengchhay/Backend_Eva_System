from flask_restx import fields

from app.extensions import api
from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

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


# For SysPerson
sys_person_model_get = api.model('SysPerson', {
    'id': fields.Integer(required=True, description='Id'),
    'name_latin': fields.String(required=True, description='Name latin'),
    'name_khmer': fields.String(required=True, description='Name khmer'),
    'photo_url': fields.String(default="", description="user photo"),
    'sys_gender_id': fields.Integer(description='Phone'),
    'sys_nationality_id': fields.Integer(required=True, description='Nationality'),
    'sys_organization_id': fields.Integer(required=True, description='Organization'),
    'sys_department_id': fields.Integer(description='Department'),
    'sys_position_id': fields.Integer(description='Position'),
    'phone': fields.String(required=True, description='Phone'),
    'email': fields.String(required=True, description='Email'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(required=True, default=1, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(required=True, default=1, description='Updated by')
})

sys_person_model_post = api.model('SysPersonPost', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'name_khmer': fields.String(required=True, description='Name khmer'),
    'photo_url': fields.String(default="", description="user photo"),
    'sys_gender_id': fields.Integer(description='Gender'),
    'sys_position_id': fields.Integer(description='Position'),
    'sys_department_id': fields.Integer(description='Department'),
    'sys_nationality_id': fields.Integer(description='Nationality'),
    'sys_organization_id': fields.Integer(description='Organization'),
    'phone': fields.String(description='Phone'),
    'email': fields.String(description='Email'),
})

sys_person_model_put = api.model('SysPersonPut', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'name_khmer': fields.String(required=True, description='Name khmer'),
    'photo_url': fields.String(default="", description="user photo"),
    'sys_gender_id': fields.Integer(description='Gender'),
    'sys_nationality_id': fields.Integer(required=True, description='Nationality'),
    'sys_position_id': fields.Integer(required=True, description='Position'),
    'sys_department_id': fields.Integer(description='Department'),
    'sys_organization_id': fields.Integer(required=True, description='Organization'),
    'phone': fields.String(required=True, description='Phone'),
    'email': fields.String(required=True, description='Email'),
})
