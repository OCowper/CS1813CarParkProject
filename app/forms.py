from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class enterCustID(FlaskForm):
    customerID = StringField('Customer Number')
    submit = SubmitField('Enter Car Park')
    
