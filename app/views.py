from flask import render_template, flash, redirect, request
from app import app
from app.forms import *


class DataHandler:
    def __init__(self):
        self.customerNP = None # str
        self.timePeriod = None # int
        
    def getDiscount(self):
        if self.customerNP.endswith("A"):
            return 0.5

        elif self.customerNP.endswith("B"):
            return 0

        else:
            return 1

    def calculatePrice(self):
        price = 0
        if self.timePeriod < 7:
            price = self.timePeriod * 2 # £2

        else:
            price = 20

        return price * self.getDiscount()


data = DataHandler()


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        formData = dict(request.form)
        data.customerNP = formData["customerNP"]

    form = enterCustNP()
    if form.validate_on_submit():
            return redirect('/time')
    return render_template('enterNP.html', title='Enter Your Customer Number Plate', form=form)

@app.route('/time', methods = ['GET', 'POST'])
def time():
    if request.method == "POST":
        formData = dict(request.form)
        data.timePeriod = int(formData["timePeriod"])

    form = enterTime()
    if form.validate_on_submit():
        return redirect('/payment')
    return render_template('enterTime.html', title = 'How long are you staying?', form=form)

    
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    form = paymentForm()
    if form.validate_on_submit():
        return redirect('/index')

    return render_template('enterPayment.html', title = 'Please Pay Now', form = form, price=f"{data.calculatePrice():.2f}")
