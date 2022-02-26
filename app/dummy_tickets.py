from datetime import date, datetime, timedelta
from sqlite3 import Timestamp
import time, random
import sqlite3

start_year = 2022
start_month = 2
start_day = 17

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
used_plates = []

def generate_exit_time(x, day):
    while(True):
        y = datetime(x.year, x.month, x.day, random.randint(0,23), random.randint(0+day, 59), random.randint(0, 59), random.randrange(0, 999999))
        if(y.minute - x.minute >= 30):
            return y

def generate_plate():
    curr_plate = ""

    while(True):
        for i in range(0,2):
            curr_plate += random.choice(letters)

        for i in range(0,2):
            curr_plate += random.choice(numbers)

        curr_plate += " "

        for i in range(0,3):
            curr_plate += random.choice(letters)
        
        if (curr_plate not in used_plates) or used_plates == "":
            used_plates.append(curr_plate)
            return curr_plate
        else:
            curr_plate = ""


def to_time_stamp(x):
    return time.mktime(x.timetuple())

try:
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()
    print("Connected to database")

    for day in range(0,8):
        print("1")
        for tickets_per_day in range(0,20):
            print("2")
            x = datetime(2022, 2, start_day+day, random.randint(0,23), random.randint(0, 59), random.randint(0, 59), random.randrange(0, 999999))
            print("inbetween")

            y = generate_exit_time(x, day) # more than or equal to 30 mins apart from x
            print("3")

            x_stamp = to_time_stamp(x)
            y_stamp = to_time_stamp(y)

            print("4")
            
            sqlite_insert_query = "INSERT INTO tickets (plate, entry_time, exit_time, fee, paid) VALUES ('" + generate_plate() + "','" + str(x_stamp) + "','" + str(y_stamp) + "'," + str(random.randint(0,20)) + "," + str(1) + ")"
            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted: ", cursor.rowcount)

    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")







    
    
    