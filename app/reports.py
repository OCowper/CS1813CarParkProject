import json
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta

def mean(l):
    if len(l) == 0:
        return 0

    else:
        return sum(l) / len(l)

def timestampToDateString(x):
    return datetime.fromtimestamp(x).strftime("%Y-%m-%d")


def timestampToTimeString(x):
    return datetime.fromtimestamp(x).strftime("%H:%M:%S")


def timestampToDateTimeString(x):
    return datetime.fromtimestamp(x).strftime("%Y-%m-%d (%H:%M:%S)")


def timestampToDateTime(x):
    return datetime.fromtimestamp(x)


def checkSameDate(timestamp, dateString):
    return timestampToDateString(timestamp) == dateString


def checkTimePeriod(timeToCheck, startTime, endTime):
    startTimeObj = datetime.strptime(f"{timestampToDateString(timeToCheck)} {startTime}", "%Y-%m-%d %H:%M:%S")
    endTimeObj = datetime.strptime(f"{timestampToDateString(timeToCheck)} {endTime}", "%Y-%m-%d %H:%M:%S")
    
    timeToCheckDateTime = timestampToDateTime(timeToCheck).replace(microsecond=0) # truncate milliseconds

    return startTimeObj <= timeToCheckDateTime <= endTimeObj


def countTimes(column, start, end):
    return len(column[checkTimePeriodVect(column, start, end)])


def convertToCurrency(x):
    if x != None:
        return "£{:,.2f}".format(float(x))

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
    

def getHTMLDF(df, date, startTime, endTime, includeDate=False):
    """Supplements other methods, NOT to be used by itself"""

    htmlDF = None

    try:
        df = getTimePeriod(df, date, startTime, endTime)
        htmlDF = df.drop(columns=['paid'])
        includeDict = {True: timestampToDateTimeString, False: timestampToTimeString}
        htmlDF['entry_time'] = df['entry_time'].map(includeDict[includeDate])
        htmlDF['exit_time'] = df['exit_time'].map(includeDict[includeDate])
        htmlDF['fee'] = htmlDF['fee'].map(convertToCurrency)

    except ValueError: # if there's no results for the date range / time range
        htmlDF = pd.DataFrame({i: [] for i in df.columns.values if i != 'paid'})

    finally:
        htmlDF = htmlDF.rename(columns={"id": "Ticket ID", "plate": "Plate",
            "entry_time": "Entry Time", "exit_time": "Exit Time", "fee": "Fee"})
            
        
    return htmlDF
    

def getHTML(df, startDate, endDate, startTime, endTime):
    """Converts pandas dataframe to a table in HTML with nice column names, formatted fee etc.
    :param df (pd.DataFame): Pandas dataframe
    :param date (str): Date in yyyy-mm-dd format to filter data for
    :param startTime (str): Earliest time to look at in hh:mm:ss form 
    :param endTime (str): Latest time to look at in hh:mm:ss form
    :return (str): HTML code for the pandas dataframe as a table"""

    htmlDF = None
    htmlDFList = []
    x = datetime.strptime(startDate, "%Y-%m-%d")
    endDateObj = datetime.strptime(endDate, "%Y-%m-%d")

    if x <= endDateObj:
        includeDate = not (x == endDateObj)

        while (x <= endDateObj):
            htmlDFList.append(getHTMLDF(df, x.strftime("%Y-%m-%d"), startTime, endTime, includeDate=includeDate))
            x += timedelta(days=1)

        if not all([len(i) == 0 for i in htmlDFList]):
            htmlDFList = [i for i in htmlDFList if len(i) > 0]

        htmlDF = pd.concat(htmlDFList, ignore_index=True)
        htmlDF.reset_index(drop=True, inplace=True)

    else:
        htmlDF = pd.DataFrame({i: [] for i in df.columns.values if i != 'paid'})
        htmlDF = htmlDF.rename(columns={"id": "Ticket ID", "plate": "Plate",
            "entry_time": "Entry Time", "exit_time": "Exit Time", "fee": "Fee"})


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


def getTimePeriod(df, date, startTime, endTime):
    df = df.loc[checkSameDateVect(df['entry_time'], date)]
    return df.loc[checkTimePeriodVect(df['entry_time'], startTime, endTime)]


def getNumEntries(df, startTime):
    entryTime = df['entry_time'].map(timestampToTimeString)
    return entryTime.map(lambda x: countTimes(df['entry_time'], startTime, x))


def getNumExits(df, startTime):
    entryTime = df['entry_time'].map(timestampToTimeString)
    return entryTime.map(lambda x: countTimes(df['exit_time'], startTime, x))


def getNumParked(df, startTime):
    return getNumEntries(df, startTime) - getNumExits(df, startTime)


def getCarNumbers(df, date, startTime, endTime):
    df = getTimePeriod(df, date, startTime, endTime)

    numParked = getNumParked(df, startTime)
    ids = pd.Series(numParked.index)
    ids += 1 # indexes get messed up and is 1 behind the ticket id
    
    timeParkedDF = pd.DataFrame({"id": ids, "num_parked": numParked.values})

    timeParkedDF['times'] = df.loc[df['id'].isin(timeParkedDF['id'])]['entry_time'].to_list()

    hours = []
    dateTimeList = [datetime.fromtimestamp(i) for i in timeParkedDF['times'].to_list()]
    
    for timeObj in dateTimeList:
        if timeObj.hour not in hours:
            hours.append(timeObj.hour)


    carNumbersDict = {"Hour": [], "Car Numbers": []}

    for i in range(len(hours)):
        hour1 = hours[i]
        hour2 = hours[i]+1
        timeRange = [x.timestamp() for x in dateTimeList if datetime(1,1,1, hour1).time() <= 
        x.time() <= datetime(1,1,1, hour2).time()]

        carNumbersDict["Car Numbers"].append(timeParkedDF.loc[timeParkedDF["times"].isin(timeRange)]['num_parked'].to_list())
        carNumbersDict["Hour"].append(f"{hour1:02}:00 - {hour2:02}:00")

    return carNumbersDict


def lineGraphReport(df, date, startTime, endTime):
    """Creates Car Park Report Line Graph with no. cars parked, no. entries, no. exits against time for a specific date range
    :param df (pd.DataFame): Pandas dataframe
    :param date (str): Date in yyyy-mm-dd format to filter data for
    :param startTime (str): Earliest time to look at in hh:mm:ss form 
    :param endTime (str): Latest time to look at in hh:mm:ss form
    :return (str): Plotly JSON text for the plotly.js script to draw the graph"""

    try:
        df = getTimePeriod(df, date, startTime, endTime)
        
        entryTime = df['entry_time'].map(timestampToTimeString)

        numEntries = getNumEntries(df, startTime)
        numExits = getNumExits(df, startTime)

        numParked = numEntries - numExits

        parkedCarsDF = pd.DataFrame({"Time": entryTime, "No. cars parked": numParked, "No. entries": numEntries,
                "No. exits": numExits})

        if len(parkedCarsDF) == 0:
            return None

        parkedCarsGraph = px.line(parkedCarsDF, x="Time", y=parkedCarsDF.columns.values[1:], title=f"Car Park Report ({date}) ({startTime[:-3]}-{endTime[:-3]})")
        return json.dumps(parkedCarsGraph, cls=plotly.utils.PlotlyJSONEncoder)

    except ValueError: # if there's no results for the date range / time range
        return None


def barCharts(df, date, startTime, endTime, charts=[]):
    """Creates Car Park Report Bar Charts for average no. cars parked, minimum and maximum against hour time periods for a specific date range
    :param df (pd.DataFame): Pandas dataframe
    :param date (str): Date in yyyy-mm-dd format to filter data for
    :param startTime (str): Earliest time to look at in hh:mm:ss form 
    :param endTime (str): Latest time to look at in hh:mm:ss form
    :param charts (list): Which charts to plot (average, min, max)
    :return (str): Plotly JSON text for the plotly.js script to draw the graph"""

    chartDict = {"Average Cars Parked Per Hour": (lambda x: int(mean(x)), "blue"), 
    "Minimum Cars Parked Per Hour": (min, "green"), 
    "Maximum Cars Parked Per Hour": (max, "red")}

    chartJSONs = []
    try:
        barDict = {}
        carNumbersDict = getCarNumbers(df, date, startTime, endTime)
        
        barDict["Hour"] = carNumbersDict["Hour"]
        for chartName in charts:
            barDict[chartName] = [chartDict[chartName][0](x) for x in carNumbersDict["Car Numbers"]]
            
            barDF = pd.DataFrame(barDict)
            
            if len(barDF) == 0:
                chartJSONs.append(None)

            else:
                barGraph = px.bar(barDF, x="Hour", y=chartName, title=f"{chartName} ({date}) ({startTime[:-3]}-{endTime[:-3]})",
                color_discrete_sequence=[chartDict[chartName][1]]*len(barDict["Hour"]))

                chartJSONs.append(json.dumps(barGraph, cls=plotly.utils.PlotlyJSONEncoder))

    except ValueError: # if there's no results for the date range / time range
        chartJSONs += [None] * len(charts)

    return chartJSONs
