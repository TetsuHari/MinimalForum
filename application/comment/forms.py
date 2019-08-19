from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CommentForm(FlaskForm):

    content = StringField("Content",
        validators.Length(min=1, message = "You can't have an empty content"))

    class Meta:
        csrf = False
