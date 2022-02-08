from flask import render_template
from app import app
from app.forms import enterCustID

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = enterCustID()
    return render_template('enterID.html', title='Enter Your Customer ID', form=form)
