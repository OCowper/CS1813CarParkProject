from flask import render_template, flash, redirect
from app import app
from app.forms import *

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = enterCustID()
    if form.validate_on_submit():
            return redirect('/time')
    return render_template('enterID.html', title='Enter Your Customer ID', form=form)

@app.route('/time', methods = ['GET', 'POST'])
def time():
    form = enterTime()
    if form.validate_on_submit():
        return redirect('/payment')
    return render_template('enterTime.html', title = 'How long are you staying?', form=form)

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    form = paymentForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('enterPayment.html', title = 'Please Pay Now', form = form)

