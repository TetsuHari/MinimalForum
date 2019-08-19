from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ThreadForm(FlaskForm):
    _title_validators = [
        validators.Length( min=3
                         , message="The title must be at least three characters!")
                    ]
    title = StringField("Thread title", _title_validators)
    content = StringField("Content",
        [ validators.Length(min=1, message="Content must be non-empty")])

    class Meta:
        csrf = False
