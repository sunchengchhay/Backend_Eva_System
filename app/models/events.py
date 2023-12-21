from app.extensions import db


class EveCommittee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sys_person_id = db.Column(db.Integer, db.ForeignKey('sys_person.id'))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_project_committees = db.relationship(
        'EveProjectCommittee', back_populates='eve_committee')
    eve_committee_scores = db.relationship(
        'EveCommitteeScore', back_populates='eve_committee')
    sys_person = db.relationship('SysPerson', back_populates='eve_committees')
    eve_event = db.relationship('EveEvent', back_populates='eve_committees')

    def __repr__(self):
        return self.sys_person.name_latin


class EveGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    sys_department_id = db.Column(
        db.Integer, db.ForeignKey('sys_department.id'))
    name_latin = db.Column(db.String(120))
    year = db.Column(db.String(50), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_projects = db.relationship(
        'EveProject', back_populates='eve_generation')

    # one department many results
    eve_results = db.relationship('EveResult', back_populates='eve_generation')
    sys_department = db.relationship(
        'SysDepartment', back_populates='eve_generations')
    eve_event = db.relationship('EveEvent', back_populates='eve_generations')

    def __repr__(self):
        return f"{self.sys_department} {self.name_latin} {self.year}"


class EveProjectCommittee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_committee_id = db.Column(db.Integer, db.ForeignKey('eve_committee.id'))
    eve_project_shortlist_id = db.Column(
        db.Integer, db.ForeignKey('eve_project_shortlist.id'))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_committee = db.relationship(
        'EveCommittee', back_populates='eve_project_committees')
    eve_project_shortlist = db.relationship(
        'EveProjectShortlist', back_populates='eve_project_committees')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_project_committees')


class EveEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String, nullable=False)
    name_khmer = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    photo_url = db.Column(db.String)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_committees = db.relationship(
        'EveCommittee', back_populates='eve_event')
    eve_generations = db.relationship(
        'EveGeneration', back_populates='eve_event')
    eve_project_committees = db.relationship(
        'EveProjectCommittee', back_populates='eve_event')
    eve_project_shortlists = db.relationship(
        'EveProjectShortlist', back_populates='eve_event')
    eve_projects = db.relationship('EveProject', back_populates='eve_event')
    eve_project_types = db.relationship(
        'EveProjectType', back_populates='eve_event')
    eve_eval_categories = db.relationship(
        'EveEvalCategory', back_populates='eve_event')
    eve_eval_criterias = db.relationship(
        'EveEvalCriteria', back_populates='eve_event')
    eve_rubric_categories = db.relationship(
        'EveRubricCategory', back_populates='eve_event')
    eve_eval_criteria_rubrics = db.relationship(
        'EveEvalCriteriaRubric', back_populates='eve_event')
    eve_committee_scores = db.relationship(
        'EveCommitteeScore', back_populates='eve_event')

    eve_project_members = db.relationship(
        'EveProjectMember', back_populates='eve_event')

    def __repr__(self):
        return self.name_latin


class EveProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    sys_department_id = db.Column(
        db.Integer, db.ForeignKey('sys_department.id'))
    topic = db.Column(db.String)
    eve_project_type_id = db.Column(
        db.Integer, db.ForeignKey('eve_project_type.id'))
    eve_generation_id = db.Column(
        db.Integer, db.ForeignKey('eve_generation.id'))
    eve_supervisor_id = db.Column(
        db.Integer, db.ForeignKey('eve_supervisor.id'))
    contact_name = db.Column(db.String(100), nullable=False)
    telegram_number = db.Column(db.String(50))
    email_address = db.Column(db.String(200))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # one project one result
    eve_results = db.relationship('EveResult', back_populates='eve_project')
    sys_department = db.relationship(
        'SysDepartment', back_populates='eve_projects')
    eve_event = db.relationship('EveEvent', back_populates='eve_projects')
    sys_department = db.relationship(
        'SysDepartment', back_populates='eve_projects')
    eve_project_type = db.relationship(
        'EveProjectType', back_populates='eve_projects')
    eve_generation = db.relationship(
        'EveGeneration', back_populates='eve_projects')
    eve_supervisor = db.relationship(
        'EveSupervisor', back_populates='eve_projects')
    eve_project_shortlists = db.relationship(
        'EveProjectShortlist', back_populates='eve_project')
    eve_project_members = db.relationship(
        'EveProjectMember', back_populates='eve_project')

    def __repr__(self):
        return f"{self.code}"


class EveProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_event_id = db.Column(db.ForeignKey('eve_event.id'))
    eve_project_id = db.Column(db.ForeignKey('eve_project.id'))
    name_latin = db.Column(db.String(150))
    name_khmer = db.Column(db.String(150))
    sys_gender_id = db.Column(db.ForeignKey('sys_gender.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    sys_gender = db.relationship(
        'SysGender', back_populates='eve_project_members')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_project_members')
    eve_project = db.relationship(
        'EveProject', back_populates='eve_project_members')


class EveResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_project_shortlist_id = db.Column(
        db.ForeignKey('eve_project_shortlist.id'))
    eve_project_id = db.Column(db.ForeignKey('eve_project.id'))
    eve_generation_id = db.Column(
        db.Integer, db.ForeignKey('eve_generation.id'))
    eve_project_type_id = db.Column(db.ForeignKey(
        'eve_project_type.id'))
    total_score = db.Column(db.Float)
    is_locked = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_project_shortlist = db.relationship(
        'EveProjectShortlist', back_populates='eve_results')
    eve_project = db.relationship(
        'EveProject', back_populates='eve_results')
    eve_generation = db.relationship(
        'EveGeneration', back_populates='eve_results')
    eve_project_type = db.relationship(
        'EveProjectType', back_populates='eve_results')


class EveProjectShortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    eve_project_id = db.Column(db.Integer, db.ForeignKey('eve_project.id'))
    eve_project_type_id = db.Column(db.ForeignKey(
        'eve_project_type.id'))    # poster or presentation
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_project_committees = db.relationship(
        'EveProjectCommittee', back_populates='eve_project_shortlist')
    # one shortlist = one result
    eve_results = db.relationship(
        'EveResult', back_populates='eve_project_shortlist')
    eve_committee_scores = db.relationship(
        'EveCommitteeScore', back_populates='eve_project_shortlist')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_project_shortlists')
    eve_project = db.relationship(
        'EveProject', back_populates='eve_project_shortlists')
    eve_project_type = db.relationship(
        'EveProjectType', back_populates='eve_project_shortlists')

    def __repr__(self):
        return self.eve_project.code


class EveSupervisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100))
    name_khmer = db.Column(db.String(100))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_projects = db.relationship(
        'EveProject', back_populates='eve_supervisor')

    def __repr__(self):
        return self.name_latin


class EveProjectType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_projects = db.relationship(
        'EveProject', back_populates='eve_project_type')
    eve_project_shortlists = db.relationship(
        'EveProjectShortlist', back_populates='eve_project_type')
    eve_results = db.relationship(
        'EveResult', back_populates='eve_project_type')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_project_types')

    def __repr__(self):
        return self.name_latin


class EveEvalCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String(100))
    weight = db.Column(db.Float(precision=2))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_eval_criterias = db.relationship(
        'EveEvalCriteria', back_populates='eve_eval_category')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_eval_categories')

    def __repr__(self):
        return self.name_latin


class EveEvalCriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String)
    eve_eval_category_id = db.Column(
        db.Integer, db.ForeignKey('eve_eval_category.id'))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # alot of rubric in one criteria
    eve_eval_criteria_rubrics = db.relationship(
        'EveEvalCriteriaRubric', back_populates='eve_eval_criteria')
    eve_committee_scores = db.relationship(
        'EveCommitteeScore', back_populates='eve_eval_criteria')
    eve_eval_category = db.relationship(
        'EveEvalCategory', back_populates='eve_eval_criterias')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_eval_criterias')

    def __repr__(self):
        return self.name_latin


class EveRubricCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_latin = db.Column(db.String)
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_event = db.relationship(
        'EveEvent', back_populates='eve_rubric_categories')
    eve_eval_criteria_rubrics = db.relationship(
        'EveEvalCriteriaRubric', back_populates='eve_rubric_category')

    def __repr__(self):
        return self.name_latin


class EveEvalCriteriaRubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_eval_criteria_id = db.Column(
        db.Integer, db.ForeignKey('eve_eval_criteria.id'))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    score = db.Column(db.Integer)
    eve_rubric_category_id = db.Column(
        db.Integer, db.ForeignKey('eve_rubric_category.id'))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_eval_criteria = db.relationship(
        'EveEvalCriteria', back_populates='eve_eval_criteria_rubrics')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_eval_criteria_rubrics')
    eve_rubric_category = db.relationship(
        'EveRubricCategory', back_populates='eve_eval_criteria_rubrics')


class EveCommitteeScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eve_committee_id = db.Column(db.Integer, db.ForeignKey('eve_committee.id'))
    eve_project_shortlist_id = db.Column(
        db.Integer, db.ForeignKey('eve_project_shortlist.id'))
    eve_event_id = db.Column(db.Integer, db.ForeignKey('eve_event.id'))
    eve_eval_criteria_id = db.Column(
        db.Integer, db.ForeignKey('eve_eval_criteria.id'))
    score = db.Column(db.Float)
    is_locked = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    eve_committee = db.relationship(
        'EveCommittee', back_populates='eve_committee_scores')
    eve_project_shortlist = db.relationship(
        'EveProjectShortlist', back_populates='eve_committee_scores')
    eve_event = db.relationship(
        'EveEvent', back_populates='eve_committee_scores')
    eve_eval_criteria = db.relationship(
        'EveEvalCriteria', back_populates='eve_committee_scores')
