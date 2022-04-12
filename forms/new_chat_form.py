from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class NewChatForm(FlaskForm):
    text = TextAreaField('name', validators=[DataRequired()])
    user = TextAreaField('user', validators=[FileRequired()])
    submit = SubmitField('add')

