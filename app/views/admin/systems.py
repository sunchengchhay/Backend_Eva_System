from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, flash
from wtforms import PasswordField
from werkzeug.security import generate_password_hash

from app.customs.cambodia_datetime import current_time_cambodia


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


# custom class for password_hash at admin page
class CustomPasswordField(PasswordField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] != '':
            self.data = generate_password_hash(valuelist[0])
        elif self.data is None:
            self.data = ''


class SysUserModelView(ModelView):
    page_size = 10
    form_columns = [
        'sys_person', 'username', 'password', 'sys_profile', 'status']
    column_list = ('id',
                   'username',
                   'sys_person',
                   'sys_profile',
                   'status',
                   'last_login_at')
    form_overrides = {
        'password': CustomPasswordField,
    }

    column_sortable_list = {"id"}

    column_searchable_list = {'username','sys_person.name_latin'}

    column_labels = {
        'id': 'id',
        'username': 'username',
        'sys_person': 'full name',
        'sys_profile': 'role'
    }
    column_filters = ('id', 'username')
    can_edit = True

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.last_login_at = current_time_cambodia()
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysPersonModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer', 'sys_gender',
        'sys_nationality', 'sys_position', 'sys_organization',
        'sys_department', 'phone', 'email'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer',
        'sys_gender': 'gender',
        'sys_nationality': 'nationality',
        'sys_organization': 'organization',
        'sys_department': 'department',
        'sys_position': 'position',
        'phone': 'phone',
        'email': 'email'
    }
    form_columns = (
        'name_latin', 'name_khmer', 'sys_gender',
        'sys_nationality', 'sys_position', 'sys_organization',
        'sys_department', 'phone', 'email'
    )
    column_sortable_list = {"id"}
    column_searchable_list = {'name_latin', 'name_khmer',
                              'sys_gender.name_latin', 'sys_department.name_latin'}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysGenderModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer'
    }
    form_columns = (
        'name_latin', 'name_khmer'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysOrganizationModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer'
    }
    form_columns = (
        'name_latin', 'name_khmer'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysNationalityModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer'
    }
    form_columns = (
        'name_latin', 'name_khmer'
    )
    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysPositionModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer'
    }
    form_columns = (
        'name_latin', 'name_khmer'
    )
    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysDepartmentModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer'
    }
    form_columns = [
        'name_latin', 'name_khmer'
    ]

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysProfileAccessRightModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'sys_profile', 'sys_sub_menu', 'sys_right'
    )
    column_labels = {
        'id': 'id',
        'sys_profile': 'role',
        'sys_sub_menu': 'sub_menu',
        'sys_right': 'right'
    }
    form_columns = (
        'sys_profile', 'sys_sub_menu', 'sys_right'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysProfileModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'acronym', 'name_latin'
    )
    column_labels = {
        'id': 'id',
        'acronym': 'acronym',
        'name_latin': 'name_latin'
    }
    form_columns = (
        'acronym', 'name_latin'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysRightModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'acronym', 'description'
    )
    column_labels = {
        'id': 'id',
        'acronym': 'acronym',
        'description': 'description',
    }
    form_columns = (
        'acronym', 'description'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysMenuModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'order'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'order': 'order',
    }
    form_columns = (
        'name_latin', 'order'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))


class SysSubMenuModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'sys_menu', 'order', 'endpoint'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'sys_menu': 'sys_menu',
        'order': 'order',
        'endpoint': 'endpoint'
    }
    form_columns = (
        'name_latin', 'sys_menu', 'order', 'endpoint'
    )

    column_sortable_list = {"id"}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = current_time_cambodia()
            model.created_by = current_user.id
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()
        else:
            model.updated_by = current_user.id
            model.updated_at = current_time_cambodia()

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.sys_profile_id == 1)

    def inaccessible_callback(self, name, **kwargs):
        flash('please login to access this page', 'danger')
        return redirect(url_for('auth_bp.login_bp.login'))
