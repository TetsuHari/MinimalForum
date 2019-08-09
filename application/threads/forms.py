from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ThreadForm(FlaskForm):
    _title_validators = [
        validators.Length( min=3
                         , message="The title must be at least three characters!")
                    ]
    title = StringField("Thread title", _title_validators)
    content = StringField("Content") # TODO this needs to be comment form

    class Meta:
        csrf = False
