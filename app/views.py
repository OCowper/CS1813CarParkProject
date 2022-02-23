from flask import render_template, flash, redirect, request
from app import app
from app.forms import *
import time
import math
from app import database

def ticketsUpdate(curNP, startTime):
    curTickets = database.Tickets.query.order_by(database.Tickets.id)
    tempNum = 0
    for ticket in curTickets:
        if ticket.id > tempNum:
            tempNum = ticket.id
    tempNum = tempNum + 1
    curTicket = database.Tickets(id = tempNum, plate = curNP, entry_time = startTime, paid = False)
    database.db.session.add(curTicket)
    database.db.session.commit()
    data.setCurTicket(tempNum)

class DataHandler:
    def __init__(self):
        self.customerNP = None # str
        self.timePeriod = None # int
        self.startTime = None # int
        self.totalTime = None # int
        self.happyHour = False # boolean
        self.curTicket = None
        self.curTID = None

    def setCurTID(self, curTID):
        self.curTID = curTID

    def getCurTID(self):
        return self.curTID

    def setCustomerNP(self, customerNP):
        self.customerNP = customerNP

    def getHappyHour(self):
        return self.happyHour
        
    def getDiscount(self):
        curCustomer = database.Customer.query.filter_by(plate = self.customerNP).first()
        if curCustomer != None:
            if curCustomer.local_authority == True or self.happyHour == True:
                return 0
            elif curCustomer.local_consultancy == True:
                return 0.5
            else:
                return 1
        elif self.happyHour == True:
            return 0
        else:
            return 1

    def setCurTicket(self, curTicket):
        self.curTicket = curTicket

    def getCurTicket(self):
        return self.curTicket

    def calculatePrice(self):
        price = 0
        if self.totalTime < 70:
            price = math.trunc(self.totalTime / 10) + 1
        else:
            price = 20

        return price * self.getDiscount()

    def startTimer(self):
        self.startTime = time.time()

    def endTimer(self):
        self.totalTime = time.time() - self.startTime

    def calcTime(self):
        self.totalTime = self.curTicket.exit_time - self.curTicket.entry_time

    def toggleHappyHour(self):
        self.happyHour = not(self.happyHour)


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
            startTime = time.time()
            ticketsUpdate(form.customerNP.data, startTime)
            return redirect('/entry')
    return render_template('enterNP.html', title='Enter Your Customer Number Plate', form=form)


@app.route('/timing', methods = ['GET', 'POST'])
def timing():
    if request.method == "POST":
        formData = dict(request.form)
        data.timePeriod = int(formData["timePeriod"])
    form = enterTime()
    if form.validate_on_submit():
        return redirect('/payment')
    return render_template('enterTime.html', title = 'How long are you staying?', form=form)

@app.route('/entry', methods = ['GET', 'POST'])
def entry():
    form = entryButton()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('entryB.html', title = 'Press to Enter', form = form, number = data.getCurTicket())

@app.route('/signOut', methods = ['GET', 'POST'])
def signOut():
    form = enterTicket()
    if form.validate_on_submit():
        curID = form.ticketNumber.data
        curTicket = database.Tickets.query.filter_by(id = curID).first()
        data.setCurTID(curID)
        if curTicket != None:
            if curTicket.paid == False:
                curTicket.exit_time = time.time()
                database.db.session.commit()
                data.setCurTicket(curTicket)
                data.calcTime()
                data.setCustomerNP(curTicket.plate)
                return redirect('/payment')
            return redirect ('/tryAgain')
        return redirect ('/tryAgain')
    return render_template('enterT.html', title = 'Enter Ticket Number', form = form)
    
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    form = paymentForm()
    if form.validate_on_submit():
        curID = data.getCurTID()
        curTicket = database.Tickets.query.filter_by(id = curID).first()
        curTicket.fee = data.calculatePrice()
        curTicket.paid = True
        database.db.session.commit()
        return redirect('/index')
    if data.getHappyHour():
        return render_template('enterPaymentHappy.html', title = 'Please Pay Now', form = form, price=f"{data.calculatePrice():.2f}")
    else:
        return render_template('enterPayment.html', title = 'Please Pay Now', form = form, price=f"{data.calculatePrice():.2f}")

@app.route('/mLogin', methods = ['GET', 'POST'])
def mLogin():
    form = mLoginForm()
    if form.validate_on_submit():
        curUsername = form.username.data
        curLogin = database.ManagerLogin.query.filter_by(username = curUsername).first()
        if curLogin != None:
            if curLogin.password == form.password.data:
                return redirect('/mView')
            return redirect('/mTryAgain')
        return redirect('/mTryAgain')
    return render_template('mLogin.html', title = 'Manager Sign In', form = form)

@app.route('/mView', methods = ['GET', 'POST'])
def mView():
    if data.getHappyHour():
        form = endHappy()
    else:
        form = startHappy()
    if form.validate_on_submit():
        data.toggleHappyHour()
        return redirect('/mView')
    return render_template('mView.html', title = 'Manager Menu', form = form)

@app.route('/tryAgain', methods = ['GET', 'POST'])
def tryAgain():
    form = returnB()
    if form.validate_on_submit():
        return redirect('/signOut')
    return render_template('tryAgain.html', title = 'Please Try Again', form = form)

@app.route('/mTryAgain', methods = ['GET', 'POST'])
def mTryAgain():
    form = returnB()
    if form.validate_on_submit():
        return redirect('/mLogin')
    return render_template('mTryAgain.html', title = 'Please Try Again', form = form)
