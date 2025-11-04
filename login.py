from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
    username = StringField('USERNAME', validators=[DataRequired()])
    password = StringField('PASSWORD', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')