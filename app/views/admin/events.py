from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash

from app.customs.cambodia_datetime import current_time_cambodia


class EveCommitteeModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'sys_person', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'sys_person': 'full_name',
        'eve_event': 'event',
    }
    form_columns = (
        'sys_person', 'eve_event'
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


class EveGenerationModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'eve_event', 'sys_department', 'name_latin', 'year'
    )
    column_labels = {
        'id': 'id',
        'eve_event': 'event',
        'sys_department': 'department',
        'name_latin': 'name_latin',
        'year': 'year'
    }
    form_columns = (
        'eve_event', 'sys_department', 'name_latin', 'year'
    )

    column_searchable_list = {
        'sys_department.name_latin', 'year', 'name_latin'}

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


class EveProjectCommitteeModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'eve_committee', 'eve_project_shortlist', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'eve_committee': 'committee',
        'eve_project_shortlist': 'project_shortlist',
        'eve_event': 'event'
    }
    form_columns = (
        'eve_committee', 'eve_project_shortlist', 'eve_event'
    )

    column_searchable_list = {
        'eve_project_shortlist.eve_project.code', 'eve_committee.sys_person.name_latin'}

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


class EveEventModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer', 'description', 'start_date', 'end_date'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer',
        'description': 'description',
        'start_date': 'start_date',
        'end_date': 'end_date'
    }
    form_columns = (
        'name_latin', 'name_khmer', 'description', 'start_date', 'end_date'
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


class EveResultModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'eve_project_shortlist', 'eve_project', 'eve_generation', 'eve_project_type', 'total_score', 'is_locked'
    )
    column_labels = {
        'id': 'id',
        'eve_project_shortlist': 'project_shortlist',
        'eve_project': 'project',
        'eve_generation': 'generation',
        'eve_project_type': 'project_type',
        'total_score': 'total_score',
        'is_locked': 'is_locked'
    }
    form_columns = (
        'eve_project_shortlist', 'eve_project', 'eve_generation', 'eve_project_type', 'total_score', 'is_locked'
    )
    column_searchable_list = {'eve_project.code', 'eve_generation.name_latin',
                              'eve_generation.year', 'eve_project_type.name_latin', 'total_score'}
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


class EveProjectShortlistModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'eve_event', 'eve_project', 'eve_project_type'
    )
    column_labels = {
        'id': 'id',
        'eve_event': 'event',
        'eve_project': 'project',
        'eve_project_type': 'project_type'
    }
    form_columns = (
        'eve_event', 'eve_project', 'eve_project_type'
    )

    column_searchable_list = {
        'eve_project_type.name_latin', 'eve_project.code'}

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


class EveSupervisorModel(ModelView):
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

    column_searchable_list = {'name_latin'}

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


class EveProjectTypeModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'eve_event': 'event'
    }
    form_columns = (
        'name_latin', 'eve_event'
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


class EveEvalCategoryModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'weight', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'weight': 'weight',
        'eve_event': 'event'
    }
    form_columns = (
        'name_latin', 'weight', 'eve_event'
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


class EveEvalCriteriaModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'eve_eval_category', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'eve_eval_category': 'eval_category',
        'eve_event': 'event'
    }
    form_columns = (
        'name_latin', 'eve_eval_category', 'eve_event'
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


class EveRubricCategoryModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'eve_event'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'eve_event': 'event'
    }
    form_columns = (
        'name_latin', 'eve_event'
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


class EveEvalCriteriaRubricModel(ModelView):
    can_edit = True
    page_size = 8
    column_list = (
        'id', 'eve_eval_criteria', 'eve_event', 'score', 'eve_rubric_category'
    )
    column_labels = {
        'id': 'id',
        'eve_eval_criteria': 'eval_criteria',
        'eve_event': 'event',
        'score': 'score',
        'eve_rubric_category': 'rubric_category'
    }
    form_columns = (
        'eve_eval_criteria', 'eve_event', 'score', 'eve_rubric_category'
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


class EveCommitteeScoreModel(ModelView):
    can_edit = True
    page_size = 9
    column_list = (
        'id', 'eve_committee', 'eve_project_shortlist', 'eve_event', 'eve_eval_criteria', 'score', 'comment', 'is_locked'
    )
    column_labels = {
        'id': 'id',
        'eve_committee': 'committee',
        'eve_project_shortlist': 'project_shortlist',
        'eve_event': 'event',
        'eve_eval_criteria': 'eval_criteria',
        'score': 'score',
        'is_locked': 'is_locked'
    }
    form_columns = (
        'eve_committee', 'eve_project_shortlist', 'eve_event', 'score', "comment", 'eve_eval_criteria'
    )

    column_searchable_list = {
        'eve_committee.sys_person.name_latin', 'eve_project_shortlist.eve_project.code'}

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


class EveProjectModel(ModelView):
    can_edit = True
    page_size = 10
    column_searchable_list = ['code', 'topic']
    column_list = (
        'id', 'code', 'eve_event', 'sys_department', 'topic', 'eve_project_type', 'eve_generation',
        'eve_supervisor', 'contact_name', 'telegram_number', 'email_address'
    )
    column_labels = {
        'id': 'id',
        'code': 'code',
        'eve_event': 'event',
        'sys_department': 'department',
        'eve_project_type': 'project_type',
        'eve_generation': 'generation',
        'eve_supervisor': 'supervisor',
        'contact_name': 'contact_name',
        'telegram_number': 'telegram',
        'email_address': 'email_address'
    }

    column_searchable_list = {
        "sys_department.name_latin", "code", "eve_project_type.name_latin", "eve_generation.year", "eve_supervisor.name_latin"}

    form_columns = (
        'code', 'eve_event', 'sys_department', 'topic', 'eve_project_type', 'eve_generation',
        'eve_supervisor', 'contact_name', 'telegram_number', 'email_address'
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


class EveProjectMemberModel(ModelView):
    can_edit = True
    page_size = 10
    column_list = (
        'id', 'name_latin', 'name_khmer', 'sys_gender', 'eve_event', 'eve_project'
    )
    column_labels = {
        'id': 'id',
        'name_latin': 'name_latin',
        'name_khmer': 'name_khmer',
        'sys_gender': 'gender',
        'eve_event': 'event',
        'eve_project': 'project'
    }
    form_columns = (
        'name_latin', 'name_khmer', 'sys_gender', 'eve_event', 'eve_project'
    )
    column_searchable_list = {'name_latin',
                              'eve_project.code', 'sys_gender.name_latin'}

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
