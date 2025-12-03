from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class findForm(FlaskForm):
    location = StringField('ZIP CODE', validators=[DataRequired()])
    radius = SelectField('FIND TRAILS WITHIN', choices=[(5, '5 MILES'), (10, '10 MILES'), (15, '15 MILES'), (25, '25 MILES'), (50, '50 MILES'), (100, '100 MILES')])
    terrain = SelectField('TRAIL TERRAIN', choices=[('flow','FLOWY'), ('tech','TECHNICAL'), ('*','NO PREFERENCE')])
    type = SelectField('TRAIL TYPE', choices=[('up','UPHILL'), ('down','DOWNHILL'), ('both','BOTH'), ('*','NO PREFERENCE')])
    difficulty = SelectField('DIFFICULTY', choices=[('green','GREEN'), ('blue','BLUE'), ('black','BLACK'), ('*','NO PREFERENCE')])
    jumps = BooleanField('JUMPS')
    berms = BooleanField('BERMS')
    drops = BooleanField('DROPS')
    rolls = BooleanField('ROCK ROLLS')
    skinnies = BooleanField('SKINNIES')
    submit = SubmitField('SEARCH')