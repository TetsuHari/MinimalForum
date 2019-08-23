from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CommentForm(FlaskForm):
    content_len_m       = "You can't post an empty comment"
    _content_validators = [ validators.length(min=1, message = content_len_m) ]
    content             = StringField("Content", _content_validators)

    class Meta:
        csrf = False
