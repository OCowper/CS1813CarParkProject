from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired



class enterCustNP(FlaskForm):
    customerNP = StringField('Customer Number Plate')
    submit = SubmitField('Enter the Car Park')

class enterTime(FlaskForm):
    timePeriod = StringField('Hour Number')
    submit = SubmitField('Next')
    
class paymentForm(FlaskForm):
    submit = SubmitField('Done: Exit Car Park')

class entryButton(FlaskForm):
    submit = SubmitField('Enter the Car Park')

class enterTicket(FlaskForm):
    ticketNumber = IntegerField('Ticket Number', validators = [DataRequired()])
    submit = SubmitField('Next')

class returnB(FlaskForm):
    submit = SubmitField('Return')

class mLoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class startHappy(FlaskForm):
    happyHourToggle = SubmitField('Start Happy Hour')
    
class endHappy(FlaskForm):
    happyHourToggle = SubmitField('End Happy Hour')

    
class dateSelect(FlaskForm):
    date = SelectField('Date: ', choices=[])
    starthour = SelectField('Start Hour: ', choices=[])
    endhour = SelectField('End Hour: ', choices=[])
    submit = SubmitField()
