import os
import time
import math

from flask import render_template, flash, redirect, request
from app import app
from app.forms import *
from app import database
from datetime import datetime, timedelta
from app.reports import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


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
        curCustomer = database.SpecialCustomer.query.filter_by(plate = self.customerNP).first()
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

    def calcTime(self):
        self.totalTime = self.curTicket.exit_time - self.curTicket.entry_time

    def toggleHappyHour(self):
        self.happyHour = not(self.happyHour)


data = DataHandler()


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', user=current_user)


@app.route('/mLogin', methods = ['GET', 'POST'])
def mLogin():
    if current_user.is_authenticated:
        return redirect('/mView')
    
    form = mLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            curUsername = form.username.data
            curLogin = database.ManagerLogin.query.filter_by(username = curUsername).first()
            if curLogin != None:
                if curLogin.password == form.password.data: #if check_password_hash(curLogin.password, form.password.data): 
                    flash("Logged in successfully!", category="success")
                    login_user(curLogin, remember=True)
                    return redirect('/mView')

                
                flash("Sorry, that username or password is incorrect.", category="error")

            else:
                flash("Sorry, that username or password is incorrect.", category="error")
        
        else:
            flash("Please enter all fields!", category="error")
    
    return render_template('mLogin.html', title = 'Manager Sign In', form = form, user=current_user)


@app.route('/mLogout')
@login_required
def mLogout():
    logout_user()
    return redirect('/index')


@app.route('/mView', methods = ['GET', 'POST'])
@login_required
def mView():
    if data.getHappyHour():
        form = endHappy()
    else:
        form = startHappy()
    if form.validate_on_submit():
        data.toggleHappyHour()
        return redirect('/mView')
    return render_template('mView.html', title = 'Manager Menu', form = form, user=current_user)

@app.route('/viewreport', methods=['GET', 'POST'])
@login_required
def viewReport():
    allCars = database.Tickets.query.order_by(database.Tickets.id)
    carsInside = 0
    for car in allCars:
        if car.paid == False:
            carsInside = carsInside + 1


    form = dateSelect()
    if request.method == 'GET':
        form.startdate.data = datetime.date(datetime.now())
        form.enddate.data = datetime.date(datetime.now())
        form.startTime.data = datetime.time(datetime.strptime("00:00", "%H:%M"))
        form.endTime.data = datetime.time(datetime.strptime("00:00", "%H:%M"))


    df = getDataFrame(os.path.join("app", "database.db"))


    if request.method == 'POST':
        table = getHTML(df, str(form.startdate.data), str(form.enddate.data), 
        str(form.startTime.data), str(form.endTime.data))

        graphList = []

        x = form.startdate.data

        while (x <= form.enddate.data):
            graphList.append(lineGraphReport(df, str(x), 
            str(form.startTime.data), str(form.endTime.data)))

            x += timedelta(days=1)

        return render_template('viewReport.html', title = 'View Reports', form=form, 
        numCars = carsInside, graphList=graphList, table=table, user=current_user)
    
    return render_template('viewReport.html', title = 'View Reports', form=form, 
    numCars = carsInside, graphList=[], user=current_user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are currently signed in as a manager, log out first!", category="error")
        return redirect('/index')

    if request.method == "POST":
        formData = dict(request.form)
        data.customerNP = formData["customerNP"]

    form = enterCustNP()
    if form.validate_on_submit():
            startTime = time.time()
            ticketsUpdate(form.customerNP.data, startTime)
            return redirect('/entry')
    return render_template('enterNP.html', title='Enter Your Customer Number Plate', form=form, user=current_user)

@app.route('/entry', methods = ['GET', 'POST'])
def entry():
    if current_user.is_authenticated:
        flash("You are currently signed in as a manager, log out first!", category="error")
        return redirect('/index')

    form = entryButton()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('entryB.html', title = 'Press to Enter', form = form, number = data.getCurTicket(), user=current_user)

@app.route('/signOut', methods = ['GET', 'POST'])
def signOut():
    if current_user.is_authenticated:
        flash("You are currently signed in as a manager, log out first!", category="error")
        return redirect('/index')

    form = enterTicket()
    if form.validate_on_submit():
        curID = form.ticketNumber.data
        curTicket = database.Tickets.query.filter_by(id = curID).first()
        data.setCurTID(curID)
        if curTicket != None:
            if not curTicket.paid:
                curTicket.exit_time = time.time()
                database.db.session.commit()
                data.setCurTicket(curTicket)
                data.calcTime()
                data.setCustomerNP(curTicket.plate)
                return redirect('/payment')
            else:
                flash("Sorry, that ticket has already been paid. Please try again!", category="error")
                return redirect('/signOut')
                
        flash("Sorry, that ticket does not exist. Please try again!", category="error")
        return redirect('/signOut')

    return render_template('enterT.html', title = 'Enter Ticket Number', form = form, user=current_user)
    

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    if current_user.is_authenticated:
        flash("You are currently signed in as a manager, log out first!", category="error")
        return redirect('/index')

    form = paymentForm()
    if form.validate_on_submit():
        curID = data.getCurTID()
        curTicket = database.Tickets.query.filter_by(id = curID).first()
        curTicket.fee = data.calculatePrice()
        curTicket.paid = True
        database.db.session.commit()
        return redirect('/index')
    if data.getHappyHour():
        return render_template('enterPaymentHappy.html', title = 'Please Pay Now', form = form, price=f"{data.calculatePrice():.2f}", user=current_user)
    else:
        return render_template('enterPayment.html', title = 'Please Pay Now', form = form, price=f"{data.calculatePrice():.2f}", user=current_user)


# newUser = database.ManagerLogin(id=something, username=something, 
#   password=generate_password_hash(somepassword, method='sha256'), first_name=something, surname=something)
# database.db.session.add(newUser)
# database.db.session.commit()

# Left to do:
# * Continue bootstrap for anywhere else that needs it after merging with Zu CSS
# * New dummy_values.sql with hashed passwords
# * New dummy_values.sql with GOOD dummy values for the tickets
# Do hotfix of entryT or entryB where there is a </span. instead of </span>
