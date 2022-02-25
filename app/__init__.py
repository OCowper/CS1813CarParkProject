import sqlite3

from os import path
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def create_database(app):
    if not path.exists(path.join("app", "database.db")):
        print("Database does not exist, creating...")
        db.create_all(app=app)
        conn = sqlite3.connect(path.join("app", "database.db"))
        cur = conn.cursor()
        with open(path.join("app", "dummy_values.sql"), 'r') as dummyValuesFile:
            dummyValuesScript = dummyValuesFile.read()
            cur.executescript(dummyValuesScript)
        
        print("Created database file!")


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

from app import views
from app import database
from app.database import *

create_database(app)

login_manager = LoginManager()
login_manager.login_view = '/mLogin'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return ManagerLogin.query.get(int(id))
