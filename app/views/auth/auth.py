from flask import Blueprint, render_template, redirect,  url_for, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash

from app.views.auth.form import LoginForm
from app.models import SysUser
from app.extensions import login_manager

login_bp = Blueprint('login_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    return SysUser.query.get(int(user_id))


@login_bp.route('/login', methods=('GET', 'POST'))
@login_bp.route('/', methods=('GET', 'POST'))
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = SysUser.query.filter_by(
            username=form_login.username.data).first()
        if user and check_password_hash(user.password, form_login.password.data) and user.sys_profile_id == 1:
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid credentials!!', 'danger')
            return redirect(url_for('auth_bp.login_bp.login'))

    return render_template('auth/login.html', form=form_login)


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you are signed out !", "success")
    return redirect(url_for('auth_bp.login_bp.login'))
