from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

from application import db
from application.auth.models import User

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username")

    def validate_username(form, field):
        check_user = User.query.filter_by(username=field.data).first()
        if check_user:
            print("DIDNT FIND USER")
            raise ValidationError("Username taken")

    _password_validators = [ validators.Length(min=8,
                                message = "Password must be at least 8 characters")]
    password = PasswordField("Password", _password_validators)

    _password_conf_validators = [ validators.EqualTo('password',
                                message = "Passwords must match")]
    password_confirm = PasswordField("Confirm password", _password_conf_validators)

    class Meta:
        csrf = False
