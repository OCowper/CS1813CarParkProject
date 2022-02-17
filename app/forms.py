from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired



class enterCustNP(FlaskForm):
    customerNP = StringField('Customer Number Plate')
    submit = SubmitField('Enter the Car Park')

class enterTime(FlaskForm):
    timePeriod = StringField('Hour Number')
    submit = SubmitField('Next')
    
class paymentForm(FlaskForm):
    submit = SubmitField('Done: Exit Car Park')

class exitButton(FlaskForm):
    submit = SubmitField('Exit the Car Park')

class mLoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class startHappy(FlaskForm):
    happyHourToggle = SubmitField('Start Happy Hour')
    
class endHappy(FlaskForm):
    happyHourToggle = SubmitField('End Happy Hour')

    
    
