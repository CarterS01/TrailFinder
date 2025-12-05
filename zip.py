from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class zipForm(FlaskForm):
    location = StringField('ZIP CODE', validators=[DataRequired()])
    radius = SelectField('FIND TRAILS WITHIN', choices=[(5, '5 MILES'), (10, '10 MILES'), (15, '15 MILES'), (25, '25 MILES'), (50, '50 MILES'), (100, '100 MILES')])
    submit = SubmitField('SEARCH')