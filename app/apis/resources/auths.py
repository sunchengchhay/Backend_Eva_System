from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt
)
from werkzeug.security import check_password_hash

from app.apis.models import login_model
from app.extensions import db
from app.models import SysUser
from app.customs.cambodia_datetime import current_time_cambodia

ns = Namespace("Authenthication", description="Authenthication endpoints")


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        """Login a user"""
        data = ns.payload or request.json
        user = SysUser.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.username)

            user.last_login_at = current_time_cambodia()
            db.session.commit()

            return {
                "access_token": access_token,
                "user_id ":  user.id,
            }, 200

        return {"message": "Invalid Credential"}, 401


@ns.route("/protected")
class Protected(Resource):
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    def get(self):
        return get_jwt()
