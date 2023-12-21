from app.extensions import db
from flask_login import UserMixin
from app.customs.cambodia_datetime import current_time_cambodia


#
class SysUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sys_profile_id = db.Column(db.ForeignKey('sys_profile.id'))
    sys_person_id = db.Column(db.ForeignKey('sys_person.id'))
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(
        db.DateTime, default=current_time_cambodia(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_person = db.relationship('SysPerson', back_populates='sys_users')
    sys_profile = db.relationship('SysProfile', back_populates='sys_users')


class SysMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_sub_menus = db.relationship('SysSubMenu', back_populates='sys_menu')


class SysSubMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100), nullable=False)
    sys_menu_id = db.Column(db.Integer, db.ForeignKey('sys_menu.id'))
    order = db.Column(db.Integer, nullable=False)
    endpoint = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_profile_access_rights = db.relationship(
        'SysProfileAccessRight', back_populates='sys_sub_menu')
    sys_menu = db.relationship('SysMenu', back_populates='sys_sub_menus')

#


class SysProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(64), nullable=False)
    name_latin = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_users = db.relationship('SysUser', back_populates='sys_profile')
    sys_profile_access_rights = db.relationship(
        'SysProfileAccessRight', back_populates='sys_profile')

    def __repr__(self):
        return self.acronym


class SysRight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_profile_access_rights = db.relationship(
        'SysProfileAccessRight', back_populates='sys_right')

    def __repr__(self):
        return self.acronym


class SysProfileAccessRight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sys_profile_id = db.Column(db.Integer, db.ForeignKey('sys_profile.id'))
    sys_sub_menu_id = db.Column(db.Integer, db.ForeignKey('sys_sub_menu.id'))
    sys_right_id = db.Column(db.Integer, db.ForeignKey('sys_right.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_sub_menu = db.relationship(
        'SysSubMenu', back_populates='sys_profile_access_rights')
    sys_profile = db.relationship(
        'SysProfile', back_populates='sys_profile_access_rights')
    sys_right = db.relationship(
        'SysRight', back_populates='sys_profile_access_rights')


class SysPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100), nullable=False)
    name_khmer = db.Column(db.String(100))
    photo_url = db.Column(db.String)
    sys_gender_id = db.Column(db.ForeignKey('sys_gender.id'))
    sys_nationality_id = db.Column(db.ForeignKey('sys_nationality.id'))
    sys_position_id = db.Column(db.ForeignKey('sys_position.id'))
    sys_organization_id = db.Column(db.ForeignKey('sys_organization.id'))
    sys_department_id = db.Column(db.ForeignKey('sys_department.id'))
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_users = db.relationship('SysUser', back_populates='sys_person')
    sys_gender = db.relationship('SysGender', back_populates='sys_persons')
    sys_nationality = db.relationship(
        'SysNationality', back_populates='sys_persons')
    sys_position = db.relationship('SysPosition', back_populates='sys_persons')
    sys_organization = db.relationship(
        'SysOrganization', back_populates='sys_persons')
    sys_department = db.relationship(
        'SysDepartment', back_populates='sys_persons')
    eve_committees = db.relationship(
        'EveCommittee', back_populates='sys_person')

    def __repr__(self):
        return self.name_latin


class SysGender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(64), nullable=False)
    name_khmer = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_persons = db.relationship('SysPerson', back_populates='sys_gender')
    eve_project_members = db.relationship('EveProjectMember',back_populates='sys_gender')

    def __repr__(self):
        return self.name_latin


class SysDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String, nullable=False)
    name_khmer = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    eve_generations = db.relationship(
        'EveGeneration', back_populates='sys_department')
    eve_projects = db.relationship(
        'EveProject', back_populates='sys_department')
    sys_persons = db.relationship('SysPerson', back_populates='sys_department')

    def __repr__(self):
        return self.name_latin


class SysOrganization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String, nullable=False)
    name_khmer = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_persons = db.relationship(
        'SysPerson', back_populates='sys_organization')

    def __repr__(self):
        return self.name_latin


class SysPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100), nullable=False)
    name_khmer = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_persons = db.relationship('SysPerson', back_populates='sys_position')

    def __repr__(self):
        return self.name_latin


class SysNationality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100), nullable=False)
    name_khmer = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    sys_persons = db.relationship(
        'SysPerson', back_populates='sys_nationality')

    def __repr__(self):
        return self.name_latin
