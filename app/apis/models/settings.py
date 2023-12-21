from app.extensions import api
from flask_restx import fields

from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

# For SysMenu
sys_menu_model = api.model('SysMenu', {
    'id': fields.Integer(required=True, description='Id'),
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(default=1, required=True, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(default=1, required=True, description='Updated by')
})
sys_menu_model_post = api.model('SysMenuPost', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
})
sys_menu_model_put = api.model('SysMenuPut', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
})

# For SysSubMenu
sys_sub_menu_model = api.model('SysSubMenu', {
    'id': fields.Integer(required=True, description='Id'),
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
    'endpoint': fields.String(required=True, description='Endpoint'),
    'sys_menu_id': fields.Integer(required=True, description='Sys menu'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(default=1, required=True, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(default=1, required=True, description='Updated by'),
})
sys_sub_menu_model_post = api.model('SysSubMenuPost', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
    'endpoint': fields.String(required=True, description='Endpoint'),
    'sys_menu_id': fields.Integer(required=True, description='Sys menu'),
})
sys_sub_menu_model_put = api.model('SysSubMenuPut', {
    'name_latin': fields.String(required=True, description='Name latin'),
    'order': fields.Integer(required=True, description='Order'),
    'endpoint': fields.String(required=True, description='Endpoint'),
    'sys_menu_id': fields.Integer(required=True, description='Sys menu'),
})
#

# For SysRight
sys_right_model = api.model('SysRight', {
    'id': fields.Integer(required=True, description='Id'),
    'acronym': fields.String(required=True, description='Acronym'),
    'description': fields.String(required=True, description='Description'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(required=True, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(required=True, description='Updated by')
})
sys_right_model_post = api.model('SysRightPost', {
    'acronym': fields.String(required=True, description='Acronym'),
    'description': fields.String(required=True, description='Description'),
})
sys_right_model_put = api.model('SysRightPut', {
    'acronym': fields.String(required=True, description='Acronym'),
    'description': fields.String(required=True, description='Description')
})

# For SysProfileAccessRight
sys_profile_access_right_model = api.model('SysProfileAccessRight', {
    'id': fields.Integer(required=True, description='Id'),
    'sys_profile_id': fields.Integer(required=True, description='Sys profile'),
    'sys_right_id': fields.Integer(required=True, description='Sys right'),
    'sys_sub_menu_id': fields.Integer(required=True, description='Sys sub menu'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(required=True, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(required=True, description='Updated by'),
})
sys_profile_access_right_model_post = api.model('SysProfileAccessRightPost', {
    'sys_profile_id': fields.Integer(required=True, description='Sys profile'),
    'sys_right_id': fields.Integer(required=True, description='Sys right'),
    'sys_sub_menu_id': fields.Integer(required=True, description='Sys sub menu'),
})
sys_profile_access_right_model_put = api.model('SysProfileAccessRightPut', {
    'sys_profile_id': fields.Integer(required=True, description='Sys profile'),
    'sys_right_id': fields.Integer(required=True, description='Sys right'),
    'sys_sub_menu_id': fields.Integer(required=True, description='Sys sub menu'),
})


# For SysProfile
sys_profile_model = api.model('SysProfile', {
    'id': fields.Integer(required=True, description='Id'),
    'acronym': fields.String(required=True, description='Acronym'),
    'name_latin': fields.String(required=True, description='Name latin'),
    'created_at': fields.DateTime(default=time_cambodia, description='Created at'),
    'created_by': fields.Integer(default=1, required=True, description='Created by'),
    'updated_at': fields.DateTime(default=time_cambodia, description='Updated at'),
    'updated_by': fields.Integer(default=1, required=True, description='Updated by')
})
sys_profile_model_post = api.model('SysProfilePost', {
    'acronym': fields.String(required=True, description='Acronym'),
    'name_latin': fields.String(required=True, description='Name latin'),
})
sys_profile_model_put = api.model('SysProfilePut', {
    'acronym': fields.String(required=True, description='Acronym'),
    'name_latin': fields.String(required=True, description='Name latin'),
})
