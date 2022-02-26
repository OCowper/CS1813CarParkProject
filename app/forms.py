from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, TimeField, BooleanField
from wtforms.validators import DataRequired


class enterCustNP(FlaskForm):
    customerNP = StringField("", validators=[DataRequired()])
    submit = SubmitField('Enter the Car Park')


class enterTime(FlaskForm):
    timePeriod = StringField('Hour Number')
    submit = SubmitField('Next')


class paymentForm(FlaskForm):
    submit = SubmitField('Done: Exit Car Park')


class entryButton(FlaskForm):
    submit = SubmitField('Enter the Car Park')


class enterTicket(FlaskForm):
    ticketNumber = IntegerField('', validators=[DataRequired()])
    submit = SubmitField('Exit')


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


class setRecHappyHourForm(FlaskForm):
    start = TimeField('Start Time: ', format="%H:%M")
    end = TimeField('End Time: ', format="%H:%M")
    submit = SubmitField('Enter')


class dateSelect(FlaskForm):
    startdate = DateField('Start Date: ', format="%Y-%m-%d")
    enddate = DateField('End Date: ', format="%Y-%m-%d")
    startTime = TimeField('Start Time: ', format="%H:%M")
    endTime = TimeField('End Time: ', format="%H:%M")
    
    averageCars = BooleanField("View average cars per hour chart")
    minimumCars = BooleanField("View minimum cars per hour chart")
    maximumCars = BooleanField("View maximum cars per hour chart")
    entriesexits = BooleanField("View parked cars, entires and exits graph")
    
    submit = SubmitField()
