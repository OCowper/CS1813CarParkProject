import json
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta


def timestampToDateString(x):
    return datetime.fromtimestamp(x).strftime("%Y-%m-%d")


def timestampToTimeString(x):
    return datetime.fromtimestamp(x).strftime("%H:%M:%S")


def timestampToDateTime(x):
    return datetime.fromtimestamp(x)


def checkSameDate(timestamp, dateString):
    return timestampToDateString(timestamp) == dateString


def checkTimePeriod(timeToCheck, startHour, endHour):
    startHourTime = datetime.strptime(f"{timestampToDateString(timeToCheck)} {startHour}", "%Y-%m-%d %H:%M:%S")
    endHourTime = datetime.strptime(f"{timestampToDateString(timeToCheck)} {endHour}", "%Y-%m-%d %H:%M:%S")
    if endHour == "00:00:00":
        endHourTime += timedelta(days=1)

    timeToCheckDateTime = timestampToDateTime(timeToCheck).replace(microsecond=0) # truncate milliseconds

    return startHourTime <= timeToCheckDateTime <= endHourTime


def countTimes(column, start, end):
    return len(column[checkTimePeriodVect(column, start, end)])


def convertToCurrency(x):
    if x != None:
        return "£{:,.2f}".format(int(x))

    return None

checkSameDateVect = np.vectorize(checkSameDate)
checkTimePeriodVect = np.vectorize(checkTimePeriod)


def getDataFrame(databaseLocation):
    """Convert sqlite table to a pandas dataframe
    :param databaseLocation (str): Location of the database file
    :return (pd.DataFrame): The pd.DataFrame version of the SQL table"""

    con = sqlite3.connect(databaseLocation)
    df = pd.read_sql_query("SELECT * from tickets", con)
    con.close()

    df = df[df['paid'] == 1] # Only gets paid tickets

    return df


def getDates(df):
    """Converts pandas series containing datetimes in timestamp format to list of dates in yyyy-mm-dd format
    :param df (pd.DataFrame): Pandas dataframe with column 'entry_time'
    :return (list): List containing strings with dates in ascending order"""
    

    dates = list(set(df['entry_time'].map(timestampToDateString).to_list()))
    return sorted(dates, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
    

def getHTMLDF(df, date, starthour, endhour):
    """Supplements other methods, NOT to be used by itself"""

    df = df.loc[checkSameDateVect(df['entry_time'], date)]
    df = df.loc[checkTimePeriodVect(df['entry_time'], starthour, endhour)]

    htmlDF = df.drop(columns=['paid'])
    htmlDF['entry_time'] = df['entry_time'].map(timestampToTimeString)
    htmlDF['exit_time'] = df['exit_time'].map(timestampToTimeString)

    htmlDF = htmlDF.rename(columns={"id": "Ticket ID", "plate": "Plate",
         "entry_time": "Entry Time", "exit_time": "Exit Time", "fee": "Fee"})
        
    htmlDF['Fee'] = htmlDF['Fee'].map(convertToCurrency)

    return htmlDF
    

def getHTML(df, date, starthour, endhour):
    """Converts pandas dataframe to a table in HTML with nice column names, formatted fee etc.
    :param df (pd.DataFame): Pandas dataframe
    :param date (str): Date in yyyy-mm-dd format to filter data for
    :param starthour (str): Earliest time to look at in hh:mm:ss form 
    :param endhour (str): Latest time to look at in hh:mm:ss form
    :return (str): HTML code for the pandas dataframe as a table"""

    """Supplements getHTML method, NOT to be used by itself"""

    htmlDF = getHTMLDF(df.copy(), date, starthour, endhour)

    htmlDF.reset_index(drop=True, inplace=True)
    headersHTML = '\n'.join([f'<th>{i}</th>' for i in htmlDF.columns.values])
    rowsHTMLlist = []
    for rowNum in range(len(htmlDF)):
        rowHTML = '\n'.join([f'<td>{htmlDF.loc[rowNum, columnName]}</td>' for columnName in htmlDF.columns.values])
        rowsHTMLlist.append(f'<tr>{rowHTML}</tr>')


    rowsHTML = '\n'.join(rowsHTMLlist)
            

    return f'''<table border="1" class="dataframe data">
<thead>
<tr style="text-align: right;">
{headersHTML}
</tr>
</thead>
<tbody>
{rowsHTML}
</tbody>
</table>'''


def lineGraphReport(df, date, starthour, endhour):
    """Creates Car Park Report Line Graph with no. cars parked, no. entries, no. exits against time for a specific date
    :param df (pd.DataFame): Pandas dataframe
    :param date (str): Date in yyyy-mm-dd format to filter data for
    :param starthour (str): Earliest time to look at in hh:mm:ss form 
    :param endhour (str): Latest time to look at in hh:mm:ss form
    :return (str): Plotly JSON text for the plotly.js script to draw the graph"""

    df = df.loc[checkSameDateVect(df['entry_time'], date)]
    df = df.loc[checkTimePeriodVect(df['entry_time'], starthour, endhour)]

    if len(df['entry_time']) > 0:
        entryTime = df['entry_time'].map(timestampToTimeString)

        numEntries = entryTime.map(lambda x: countTimes(df['entry_time'], starthour, x))
        numExits = entryTime.map(lambda x: countTimes(df['exit_time'], starthour, x))

        numParked = numEntries - numExits

        parkedCarsDF = pd.DataFrame({"Time": entryTime, "No. cars parked": numParked, "No. entries": numEntries,
                "No. exits": numExits})

        parkedCarsGraph = px.line(parkedCarsDF, x="Time", y=parkedCarsDF.columns.values[1:], title=f"Car Park Report ({date}) ({starthour[:-3]}-{endhour[:-3]})")#, template="plotly_dark")
        return json.dumps(parkedCarsGraph, cls=plotly.utils.PlotlyJSONEncoder)

    else:
        return None
        