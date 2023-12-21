from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from app.models import (
    EveEvent,
    SysDepartment
)
from app.extensions import db
from app.apis.models import *

from app.customs.authorizations import authorizations


ns = Namespace("Event Managements",
               description="Event Management endpoints", path="/", authorizations=authorizations)

ns.decorators = [jwt_required()]


@ns.route("/events")
class Events(Resource):

    @ns.marshal_list_with(output_event_model)
    @ns.doc(security="jsonWebToken")
    def get(self):
        """Get all Events"""
        events = EveEvent.query.all()
        if events:
            return events, 200
        return {"msg": "not found"}, 404


@ns.route('/events/<int:id>')
class event(Resource):
    @ns.doc(security="jsonWebToken")
    @ns.marshal_with(output_event_model, code=201)
    def get(self, id):
        """Get an Event by ID"""
        event = EveEvent.query.get_or_404(id)
        return event, 200


# SysDepartment
@ns.route('/departments')
class Departments(Resource):

    @ns.marshal_list_with(output_same_state_model)
    @ns.doc(security="jsonWebToken")
    def get(self):
        """Get all Departments"""
        department = SysDepartment.query.all()
        if department:
            return department, 200
        return {"msg": "not found"}, 404


@ns.route('/departments/<int:id>')
class Department(Resource):

    @ns.marshal_with(output_same_state_model)
    @ns.doc(security="jsonWebToken")
    def get(self, id):
        """Get an Department by ID"""
        department = SysDepartment.query.get_or_404(id)
        if department:
            return department, 201
        return {"msg": "not found"}, 404
