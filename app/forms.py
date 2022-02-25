from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired


class enterCustNP(FlaskForm):
    customerNP = StringField("")
    submit = SubmitField('Enter the Car Park')


class enterTime(FlaskForm):
    timePeriod = StringField('Hour Number')
    submit = SubmitField('Next')


class paymentForm(FlaskForm):
    submit = SubmitField('Done: Exit Car Park')


class entryButton(FlaskForm):
    submit = SubmitField('Enter the Car Park')


class enterTicket(FlaskForm):
    ticketNumber = IntegerField('Ticket Number', validators=[DataRequired()])
    submit = SubmitField('Next')


class returnB(FlaskForm):
    submit = SubmitField('Return')


class mLoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class startHappy(FlaskForm):
    happyHourToggle = SubmitField('Start Happy Hour')


class endHappy(FlaskForm):
    happyHourToggle = SubmitField('End Happy Hour')


    
class dateSelect(FlaskForm):
    date = DateField('Start Date: ', format="%Y-%m-%d") # rename to start date later
    enddate = DateField('End Date: ', format="%Y-%m-%d")
    starthour = TimeField('Start Time: ', format="%H:%M")
    endhour = TimeField('End Time: ', format="%H:%M")
    submit = SubmitField()
