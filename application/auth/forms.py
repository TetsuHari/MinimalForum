from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError, BooleanField

from application import db
from application.auth.models import User

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False



def validate_username(form, field):
    check_user = User.query.filter_by(username=field.data).first()
    if check_user:
        raise ValidationError("Username taken")

username_len_text    = "Username length must be between 4 and 30 characters"
_username_validators = [ validators.Length(min=4, max=30,
                                message = username_len_text),
                         validate_username ]

pass_len_text        = "Password length must be between 8 and 140 characters!"
_pass_validators     = [ validators.Length(min=8, max=140,
                                message = pass_len_text)]
def _passc_validators(fieldname):
    return [ validators.EqualTo(fieldname,
                message = "Passwords must match")]

class RegisterForm(FlaskForm):
    username         = StringField("Username", _username_validators)
    password         = PasswordField("Password", _pass_validators)
    password_confirm = PasswordField("Confirm password", _passc_validators('password'))
    class Meta:
        csrf = False

class ModifyUserForm(FlaskForm):

    new_username = StringField("Change username",
        _username_validators.insert(0, validators.Optional(True)))

    new_password = PasswordField("Change password",
        _pass_validators.insert(0, validators.Optional(True)))
    new_passwordc = PasswordField("Confirm new password",
        _passc_validators('new_password'))
    delete_user = BooleanField("Delete user")

    class Meta:
        csrf = False
