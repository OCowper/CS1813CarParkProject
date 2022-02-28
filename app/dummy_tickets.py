import time, random
import sqlite3
from os import path
from datetime import datetime, timedelta


used_plates = []


def generate_plate():    
    validLetters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    randomLetters = ''.join([random.choice(validLetters) for _ in range(5)])

    curr_plate = f"{randomLetters[:2]}{random.randint(10, 99)} {randomLetters[2:]}"

    return curr_plate

def generatePlates(howMany):
    global used_plates

    plates = []
    while len(plates) < howMany:
        plates += [generate_plate() for _ in range(howMany-len(plates))]
        plates = [i for i in plates if i not in used_plates]
        used_plates += plates
    
    return plates

def generateAfternoon(dateObj):
    """15-20 cars staying for around 1-3 hours entering between 12:00-14:30
    :param dateObj (datetime.date): The date the tickets are being generated for"""
    
    howManyCars = random.randint(15, 20)
    
    ticketsDict = {}
    ticketsDict['plates'] = generatePlates(howManyCars)
    ticketsDict['entryTimes'] = []
    ticketsDict['exitTimes'] = []
    ticketsDict['fees'] = []
    ticketsDict['paid'] = []
    
    pm12 = datetime.combine(dateObj, datetime(1, 1, 1, 12, 0, 0).time())
    pm230 = datetime.combine(dateObj, datetime(1, 1, 1, 14, 30, 0).time())

    secondsBetween = (pm230-pm12).seconds

    for _ in range(howManyCars):
        entryTime = pm12 + timedelta(seconds=random.randint(0, secondsBetween))
        ticketsDict['entryTimes'].append(entryTime)
        ticketsDict['fees'].append(random.randint(50, 1000) / 100)
        ticketsDict['paid'].append(True)
    
    ticketsDict['entryTimes'] = sorted(ticketsDict['entryTimes'])
    
    for i in range(howManyCars):
        exitTime = ticketsDict['entryTimes'][i] + timedelta(seconds=random.randint(60*60, 180*60))
        ticketsDict['entryTimes'][i] = str(ticketsDict['entryTimes'][i].timestamp()) 
        ticketsDict['exitTimes'].append(str(exitTime.timestamp()))
    

    return ticketsDict


def to_time_stamp(x):
    return time.mktime(x.timetuple())


def insertTickets():
    global used_plates
    try:
        print("Connecting to database.db")
        conn = sqlite3.connect(path.join('app', 'database.db')) # insertTickets is called from __init__.py which which thinks it's outside the app folder
        cur = conn.cursor()
        print("Connected to database")
        print()


        todayObj = datetime.now()
        todayString = todayObj.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Generating random tickets every day spanning 1 year prior to today's date & time ({todayString})")


        lastYearObj = todayObj.replace(year=todayObj.year-1)
        x = lastYearObj

        while x <= todayObj:
            used_plates = [] # since same cars can visit a car park on multiple days

            ticketsDict = generateAfternoon(x)
            

            for i in range(len(ticketsDict['plates'])):
                plate, entryTime, exitTime, fee, paid = (ticketsDict['plates'][i], ticketsDict['entryTimes'][i], 
                ticketsDict['exitTimes'][i], ticketsDict['fees'][i], ticketsDict['paid'][i])

                sqlite_insert_query = f"INSERT INTO tickets (plate, entry_time, exit_time, fee, paid) VALUES ('{plate}','{entryTime}','{exitTime}',{fee},{paid})"
                count = cur.execute(sqlite_insert_query)
                conn.commit()

            x += timedelta(days=1) # add a day

        cur.close()
        print("Done!")

    except sqlite3.Error as error:
        print("Failed to insert data into 'ticket' table", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
