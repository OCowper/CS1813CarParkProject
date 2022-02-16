from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class enterCustNP(FlaskForm):
    customerNP = StringField('Customer Number Plate')
    submit = SubmitField('Next')

class enterTime(FlaskForm):
    timePeriod = StringField('Hour Number')
    submit = SubmitField('Next')
    
class paymentForm(FlaskForm):
    submit = SubmitField('Done: Enter Car Park')
