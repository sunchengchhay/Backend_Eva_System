from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask import Blueprint
from flask_login import LoginManager

from app.customs.authorizations import authorizations
from app.views.admin.systems import MyAdminIndexView

blueprint_api = Blueprint('api',__name__,url_prefix='/api/v1')

api = Api(blueprint_api,version='1.0', title='API Document',
          description='API for System Design', authorizations=authorizations)

db = SQLAlchemy()
jwt = JWTManager()
admin = Admin(name='FE',template_mode='bootstrap4',index_view = MyAdminIndexView())
login_manager = LoginManager()
