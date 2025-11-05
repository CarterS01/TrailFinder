from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class findForm(FlaskForm):
    location = StringField('ZIP CODE', validators=[DataRequired()])
    terrain = SelectField('TRAIL TERRAIN', choices=[('flow','FLOWY'), ('tech','TECHNICAL'), ('*','NO PREFERENCE')])
    type = SelectField('TRAIL TYPE', choices=[('up','UPHILL'), ('down','DOWNHILL'), ('both','BOTH'), ('*','NO PREFERENCE')])
    jumps = BooleanField('JUMPS')
    berms = BooleanField('BERMS')
    drops = BooleanField('DROPS')
    rolls = BooleanField('ROCK ROLLS')
    skinnies = BooleanField('SKINNIES')
    submit = SubmitField('SEARCH')