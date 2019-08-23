from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ThreadForm(FlaskForm):
    title_len_msg       = "The length of the title must be between 3 and 140 characters"
    _title_validators   = [ validators.Length( min=3, max=140,
                            message=title_len_msg)]
    title               = StringField("Thread title", _title_validators)

    content_len_msg    = "You can't post an empty post"
    _content_validators = [ validators.Length(min=1,
                                message=content_len_msg)]
    content             = StringField("Content", _content_validators)

    class Meta:
        csrf = False
