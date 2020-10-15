#OC Transpo API

import requests
from flask import json

# Globals
OCAPI_URL = 'https://api.octranspo1.com/v1.3/'
OCAPI_APPID = ''
OCAPI_APIKEY = ''

#Grabs API responce and returns working class code

def getStopInfo(stopID, routeID):
    TYPE = 'GetRouteSummaryForStop'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    routeNo=' + routeID + '&\
    format=json')

    return json.loads(x.text, None)

def getNextTripsForStop(stopID, routeID):
    TYPE = 'GetNextTripsForStop'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    routeNo=' + routeID + '&\
    format=json')

    return json.loads(x.text, None)

def getNextTripsForStopAllRoutes(stopID):
    TYPE = 'GetNextTripsForStopAllRoutes'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    format=json')

    return json.loads(x.text, None)
    

if __name__=="__main__":
    print(getNextTripsForStopAllRoutes('7659'))
