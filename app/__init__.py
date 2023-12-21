from flask import Flask

from app.views import register_blueprint, add_views
from app.config import Config
from app.extensions import db, api, jwt, admin, login_manager
from app.apis import api
from app.customs import jwt_identity


def create_app():

    app = Flask(__name__)
    # config
    config = Config()
    app.config.from_object(config)

    # init extensions
    db.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    # flask-login config
    login_manager.login_view = 'auth_bp.login_bp.login'
    login_manager.login_message_category = "warning"

    from app.views import CustomExportView
    admin.add_view(CustomExportView(
        name='Export Data', endpoint='excel'))

    # register blueprint
    register_blueprint(app)

    # add all flask-admin views
    add_views(admin)

    jwt_identity

    return app
