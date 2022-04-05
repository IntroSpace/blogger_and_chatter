from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
    text = TextAreaField('text', validators=[DataRequired()])
    file = FileField('photo', validators=[FileRequired()])
    submit = SubmitField('add')

