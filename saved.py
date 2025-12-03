from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class savedForm(FlaskForm):
    note = TextAreaField('EDIT NOTE:')
    save = SubmitField('SAVE')