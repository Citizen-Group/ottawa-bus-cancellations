
# BUS SCHEDULE

import pymongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import folium
import json
import csv
import os
import routes
import database
from flask import json

#MongoDB

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jv3iz.mongodb.net/CitizenInformation?retryWrites=true&w=majority")
db=client['CitizenInformation']


filename = 'data//route_stops.csv'
filename1 = 'data//stops.csv'
filename2 = 'data//cancel.csv'
filename3 = 'data//x.csv'
filename4 = 'data//cancelFeb.csv'
filename5 = 'data//xFeb.csv'

r3 = []
c3 = []
r2 = []
c2 = []
r1 = []
c1 = []
r =[]
c = []


rt_stop123 = db["Route_Stops"]
x = rt_stop123.find_one()
print("Data of Route_stop table :" + str(x))


stop123 = db["Stops"]
y = stop123.find_one()
print("Data of Stop table :" + str(y))

#list of all the data
# for x in col.find():
#     r1.append(x)


# BUS CANCELLATION

cancel123 = db["Cancel"]
x = cancel123.find_one()
print("Data of Cancel table :" + str(x))

x123 = db["X"]
y = x123.find_one()
print("Data of X table :" + str(y))



with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    c=next(csvreader)

    for i in  csvreader:
            r.append(i)

with open(filename1, 'r') as csvfile:
    csvreader1 = csv.reader(csvfile)
    c1=next(csvreader1)

    for j in  csvreader1:
            r1.append(j)

with open(filename2, 'r') as csvfile:
    csvreader2 = csv.reader(csvfile)
    c2=next(csvreader2)

    for m in  csvreader2:
            r2.append(m)

with open(filename3, 'r') as csvfile:
    csvreader3 = csv.reader(csvfile)
    c3=next(csvreader3)

    for n in  csvreader3:
            r3.append(n)


#January Bus Cancels

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    c=next(csvreader)

    for i in  csvreader:
            r.append(i)

with open(filename1, 'r') as csvfile:
    csvreader1 = csv.reader(csvfile)
    c1=next(csvreader1)

    for j in  csvreader1:
            r1.append(j)

with open(filename4, 'r') as csvfile:
    csvreader2 = csv.reader(csvfile)
    c2=next(csvreader2)

    for m in  csvreader2:
            r2.append(m)

with open(filename5, 'r') as csvfile:
    csvreader3 = csv.reader(csvfile)
    c3=next(csvreader3)

    for n in  csvreader3:
            r3.append(n)



#MAIN

database.onStart()

from flask import Flask, render_template
app = Flask(__name__)

# Global Vars
# I'll do the work here and we can later move it out to its on .py

class STATUSLEVELS():
    DANGER = 2,
    WARNING = 1,
    OK = 0

class transitElement():    
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount

class fakeRouteElement(transitElement):    
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount
        self.alert=(
        {
            "timestamp" : 13124675,
            "title" : "This is the title",
            "subtext" : "This is main body text",
            "location": {
                "text" : "Blah St.",
                "lat" : "45.231546",
                "lon" : "-72.254313"
            },
            "reason" : {
                "short" : "Short title Reason for problem",
                "long" : "Long reason title for problem"
            }
        })


class fakeStopElement():
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount


def populateRoutesForStopDatabase(stopID, date):
    #database call
    database.findRoutesForStop(stopID)
    
    fakeRouteList=[
        fakeRouteElement(95,1,0,0),
        fakeRouteElement(75,1,0,0),
        fakeRouteElement(85,1,0,0),
        fakeRouteElement(88,1,0,0),
        fakeRouteElement(4,1,1,2)
    ]

    return fakeRouteList


fakeRouteList=[
    fakeRouteElement(95,1,0,0),
    fakeRouteElement(75,1,0,0),
    fakeRouteElement(85,1,0,0),
    fakeRouteElement(88,1,0,0),
    fakeRouteElement(4,1,1,2)
]

fakeRouteList2=[
    { "eId": 5, "eStatus": 1,"eCanCount": 1, "eWarnCount": 2}
]

# Routes
@app.route('/<routeID>/<stopID>')
def routesAndStops(routeID, stopID):

    #Route and stop valid parsing needs to be done here
    #add "isValid" to the first if

    if routeID is not None or stopID is not None: 
        if routeID.lower() == "all":

            #Here we will need to do a quick call to get the cached health of all the routes
            #Filter out the routes we don't need and update a list of
            # RouteID's, statusLevel, HasCancellations, HasWarnings
            # WE can update the JS on the page to hardcode the images used for "bus route types"
            # So we don't need to pass extra data per cycle

            #API check also needed here as well as cancellation check

            #Switch over to class return type

            return render_template("stops.html",
            title="Occasional Transport: Ottawa Bus Edition", 
            mastHead="Stops Page",
            selectedRouteID="all",
            selectedstopID=stopID,
            statusLevel=STATUSLEVELS.OK, 
            locationText="Located between at the intersection of Two and Fern",
            locationDescrip="Lovely Stop. Great Atmosphere",
            mastDescrip="Display all Stops For " + stopID + " stop ID",
            fakeRouteListSend=fakeRouteList)
        else:
            return render_template("stops.html",
            title="Occasional Transport: Ottawa Bus Edition", 
            mastHead="Stops Page",
            selectedRouteID=routeID,
            selectedstopID=stopID,
            statusLevel=STATUSLEVELS.OK,
            locationText="Located between at the intersection of Two and Fern",
            locationDescrip="Lovely Stop. Great Atmosphere",
            mastDescrip="Display "+ routeID +" route information for " + stopID + " stop ID",
            fakeRouteListSend=fakeRouteList)
    else:
        index()

@app.route('/<routeID>/<stopID>/json')
def routesAndStopsJson(routeID, stopID):

    def make_summary():
        return fakeRouteList2

    if routeID is not None or stopID is not None: 
        if routeID.lower() == "all":
            if routeID is not None:
                data = make_summary()
                response = app.response_class(
                    response=json.dumps(data),
                    status=200,
                    mimetype='application/json'
                )
                return response

        else:
            if routeID is not None:
                data = make_summary()
                response = app.response_class(
                    response=json.dumps(data),
                    status=200,
                    mimetype='application/json'
                )
                return response

    else:
        index()


@app.route('/<routeID>')
def busRoutes(routeID):

    #Route valid parsing needs to be done here
    #add "isValid" to the first if

    if routeID is not None:
        return render_template("routes.html",
        title="Occasional Transport: Ottawa Bus Edition", 
        mastHead="Routes Page",
        selectedRouteID=routeID,
        statusLevel=STATUSLEVELS.OK, 
        mastDescrip="Display "+ routeID +" route information ")
    else:
        index()

@app.route('/<routeID>/json')
def busRoutesJson(routeID):

    #Route valid parsing needs to be done here
    #add "isValid" to the first if

    def make_summary():
        return fakeRouteList2

    if routeID is not None:
        data = make_summary()
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    else:
        index()


@app.route('/')
def index():

    return render_template("index.html",
    title="Occasional Transport: Ottawa Bus Edition", 
    mastHead="Where's my @#$@ Bus?",
    statusLevel=STATUSLEVELS.OK, 
    mastDescrip="Who knows. We don't. Move along.")

# Historical Routes

@app.route('/cancel/jan')
def jan():
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    for k in r1:
        folium.Marker(location=[k[4], k[5]], tooltip=[k[2], k[1]],
                      icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(m)

    for a in r2:
        for b in r3:
            if (a[0] == b[0]):
                if (b[1] < "2"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                  icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(m)
                elif (b[1] >= "2" and b[1] < "4"):

                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1], 'Cancellations'],
                                  icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(m)
                elif (b[1] >= "4"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

    m.save('templates//jan_stops.html')
    return render_template("jan_stops.html")



@app.route('/cancel/feb')
def feb():
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    for k in r1:
        folium.Marker(location=[k[4], k[5]], tooltip=[k[2], k[1]],
                      icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(m)

    for a in r2:
        for b in r3:
            if (a[0] == b[0]):
                if (b[1] < "2"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                  icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(m)
                elif (b[1] >= "2" and b[1] < "4"):

                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1], 'Cancellations'],
                                  icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(m)
                elif (b[1] >= "4"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

    m.save('templates//feb_stops.html')
    return render_template("feb_stops.html")


@app.route('/schedule/<route_id>')
def scheduleroute(route_id):
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    for k in r:
        if (k[1] == route_id and k[2] == "1"):
            for l in r1:
                if (k[3] == l[0]):
                    folium.Marker(location=[l[4], l[5]], tooltip=[l[2], l[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

    m.save('templates//schedule.html')
    return render_template("schedule.html")



@app.route('/cancel/<cancel_id>')
def cancel(cancel_id):
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    for k in r:
        if (k[1] == cancel_id):
            for l in r1:
                if (k[3] == l[0]):
                    folium.Marker(location=[l[4], l[5]], tooltip=[l[2], l[1]],
                                  icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(m)

    for a in r2:
        if (a[2] == cancel_id):
            for b in r3:
                if (a[0] == b[0]):
                    if (b[1] < "2"):
                        folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                      icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(m)
                    elif (b[1] >= "2" and b[1] < "4"):
                        folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1], 'Cancellations'],
                                      icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(m)
                    elif (b[1] >= "4"):
                        folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                      icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

    m.save('templates//cancel.html')
    return render_template("cancel.html")


if __name__=="__main__":
    app.run(port=8000,debug=True)
