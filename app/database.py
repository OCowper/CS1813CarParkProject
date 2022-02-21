from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# -------- database.db --------

# Initialise Database
db = SQLAlchemy(app)

# Create Model
MAX_PLATE_LENGTH = 8
MAX_NAME_LENGTH = 20
MAX_FEE_LENGTH = 20

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(MAX_PLATE_LENGTH), nullable=False)
    entry_time = db.Column(db.Integer, nullable=False)
    exit_time = db.Column(db.Integer)
    fee = db.Column(db.String(MAX_FEE_LENGTH))
    paid = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "ID {}, License Plate {}, Entry Time {}".format(self.id, self.plate, self.entry_time)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(MAX_PLATE_LENGTH), nullable=False)
    first_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    surname = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    local_authority = db.Column(db.Boolean, nullable=False)
    local_consultancy = db.Column(db.Boolean, nullable=False)
    employee = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "License Plate {}, First Name {}, Surname {}, Local Authority {}, Local Consultancy {}".format(self.plate, self.first_name, self.surname, self.local_authority, self.local_consultancy)

class ManagerLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    password = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    first_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    surname = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)

    def __repr__(self):
        return "ID {}, Username {}, Password {}, First Name {}, Surname {}".format(self.id, self.plate, self.entry_time)
