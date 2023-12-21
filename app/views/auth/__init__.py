from flask import Blueprint

from app.views.auth.auth import login_bp


auth_bp = Blueprint('auth_bp', __name__)
auth_bp.register_blueprint(login_bp)
