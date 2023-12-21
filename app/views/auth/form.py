from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={
                           'placeholder': 'Username'})
    password = PasswordField('Password', widget=PasswordInput(hide_value=True), validators=[
                             DataRequired()], render_kw={'placeholder': 'Password'})
    submit_login = SubmitField('Login')
