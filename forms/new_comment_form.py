from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewCommentForm(FlaskForm):
    text = TextAreaField('text', validators=[DataRequired()])
    submit = SubmitField('add')
