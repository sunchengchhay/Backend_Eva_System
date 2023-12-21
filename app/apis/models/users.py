from app.extensions import api
from flask_restx import fields

from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

# for SysUser
sys_user_model = api.model('SysUser', {
    "id": fields.Integer(required=True, description='Id'),
    "sys_profile_id": fields.Integer(required=True, description='Sys profile'),
    "sys_person_id": fields.Integer(required=True, description='Person'),
    "username": fields.String(required=True, description='Login name'),
    "status": fields.Integer(defualt=1, required=True, description='Status'),
    "last_login_at": fields.DateTime(default=time_cambodia, description='Last login at'),
    "created_at": fields.DateTime(default=time_cambodia, description='Created at'),
    "created_by": fields.Integer(required=True, description='Created by'),
    "updated_at": fields.DateTime(default=time_cambodia, description='Updated at'),
    "updated_by": fields.Integer(required=True, description='Updated by')
})

sys_user_model_post = api.model('SysUserPost', {
    "username": fields.String(required=True, description='Login name'),
    "password": fields.String(required=True, description='Password'),
    "status": fields.Integer(default=1, required=False, description='Status'),
    "sys_profile_id": fields.Integer(required=True, description='Sys profile'),
    "sys_person_id": fields.Integer(required=True, description='Person'),
    "last_login_at": fields.DateTime(default=time_cambodia, description='Last login at'),
})

sys_user_model_put = api.model('SysUserPut', {
    "username": fields.String(required=True, description='Login name'),
    "password": fields.String(required=True, description='Password'),
    "status": fields.Integer(default=1, required=False, description='Status'),
    "sys_profile_id": fields.Integer(required=True, description='Sys profile'),
    "sys_person_id": fields.Integer(required=True, description='Person'),
    "last_login_at": fields.DateTime(default=time_cambodia, description='Last login at'),
})
