'''
This document constitues the code of fastAPI.
'''

import pandas as pd
import json
from pprint import pprint
from fastapi import FastAPI, Depends, Header, Query, Request, HTTPException
import pymongo
from pymongo import MongoClient


# Creation of the API and control if it works

api = FastAPI(
    title = "AirFrance-KLM route API",
    description = "API that retrieves routes from MongoDB database",
    version="1.0",
    openapi_tags=[
        {"name": "API-Health", "description": "Check if API works"},
        {"name": "Flight", "description": "Return parametered general flights data"},
        {"name": "Status", "description": "Aggregate flight status"},
        {"name": "Delay", "description": "Produce delayed flights information"},
    ],
)

@api.get("/check", name = "API shape", tags = ['API-Health'])
def check():
    """Check if the API works"""
    return {"status": "The API is active"}


# Connection to the database MongoDB

def mongo():
    client = pymongo.MongoClient("mongodb://host.docker.internal:27017/")
    database = client["Airline_Flight_Status"]
    collection = database["flightstatus"]
    return collection


# Quiery getting flight numbers limited to departure and arrival airports in Netherland, France and Australia
# (play with IATA codes):

iata = pd.read_csv("iata.csv")
netherlands = iata.loc[iata["Country"]=="Netherlands"]
france = iata.loc[iata["Country"]=="France"]
singapore = iata.loc[iata["Country"]=="Singapore"]

@api.get("/flights/{IATA: str}", name = "Sum and number of flights restricted to 3 countries", tags = ['Flight'])
def get_flights(IATA):
    """ Get flight numbers. The desired airport IATA code in Netherlands, France or Singapore shall be specified."""
    collection = mongo()
    if (any(netherlands["IATA"]==IATA)
        or any(france["IATA"] == IATA)
        or any(singapore["IATA"] == IATA)):
        flights = list(collection.find({"$or": [{"flightLegs.departureInformation.airport.code": IATA},\
        {"flightLegs.arrivalInformation.airport.code": IATA}]}, {"flightNumber": 1, "_id": 0}))
        if len(flights)==0:
            raise HTTPException(status_code=404, detail="Not found : No flight with this IATA code in the mongodb database")
        return "The number of flights and the flight numbers with this IATA code are respectively : ",\
        len(flights), flights
    else:
        raise HTTPException(status_code=400, detail="Bad Request : Invalid IATA code")


# Quiery getting all flight data for x number of flights (in order to automatize the Dash output)

@api.get("/flights/{volume: int}", name = "x flights", tags = ['Flight'])
def get_flights(volume):
    """ Get all flights data. The desired number of flights shall be specified."""
    collection = mongo()
    flights = collection.find({}, {'_id':0}).limit(int(volume)) # take off the _id which is not iterable + specification of int mandatory
    result = []
    for flight in flights:
        result.append(flight)
    return result

# Quiery getting all flight data

@api.get("/flights", name = "Flights", tags = ['Flight'])
def get_flights():
    """ Get all flights data."""
    collection = mongo()
    flights = collection.find({}, {'_id':0})
    result = []
    for flight in flights:
        result.append(flight)
    return result

# Quiery getting flight status

@api.get("/status", name = "Flight status", tags = ['Status'])
def get_status():
    """ Get the number of flights on-time, delayed, cancelled, partially cancelled and departed."""
    collection = mongo()
    return list(collection.aggregate([{"$group": {"_id": "$flightStatusPublic", "nb_status": {"$sum": 1}}},\
{   "$sort":{"nb_status":-1} }]))


# Quiery getting delays information

@api.get("/delays", name = "Flight delay reasons", tags = ['Delay'])
def get_delays():
    """ Get the number of flights delayed due to delayed incoming aircraft, delayed cabin crew, no gate available, technical issue and operational issue.\n
    NB : The first number corresponds to the non-delayed flights.\n
    NB : The following numbers corresponds to the delayed flights. The reason field can be empty if not mentioned by the airline company."""
    collection = mongo()
    delays_text = []
    delays = list(collection.aggregate([
    {"$group": {"_id": "$flightLegs.irregularity.delayInformation.delayReasonCodePublic", "nb": {"$sum":1}}},
    {"$sort":{"nb":-1}}]))
    for i in range(len(delays)):
        if delays[i]['_id']==[['FSR01']]:
            result = {"Technical issues : ", delays[i]['nb']}
        elif delays[i]['_id']==[['FSR02']]:
            result = {"Operational issues : ", delays[i]['nb']}
        elif delays[i]['_id']==[['FSR03']]:
            result = {"delayed incoming aircraft : ", delays[i]['nb']}
        elif delays[i]['_id']==[['FSR04']]:
            result = {"delayed cabin crew :" , delays[i]['nb']}
        elif delays[i]['_id']==[['FSR05']]:
            result = {"no gate available :", delays[i]['nb']}
        else:
            result = {}
        delays_text.append(result)
    return delays_text

@api.get("/delays/departure_airport", name = "Flight delay reasons by airport of departure", tags = ['Delay'])
def get_delays_departure_airport():
    """ Aggregate flight delay reasons by departure airport."""
    collection = mongo()
    delays_text = []
    delays = list(collection.aggregate([
        {"$match": {"flightStatusPublic": "DELAYED_DEPARTURE"}},
        {"$group": {"_id": {
            "reason" : "$flightLegs.irregularity.delayInformation.delayReasonCodePublic",
            "airport": "$flightLegs.departureInformation.airport.code"
            }, "nb": {"$sum":1}}},
        {"$sort": {"nb": -1}}]))
    for i in range(len(delays)):
        if delays[i]['_id']['reason']==[['FSR01']]:
            result = ("Technical issues : ", delays[i]['_id']['airport'], delays[i]['nb'])
        elif delays[i]['_id']['reason']==[['FSR02']]:
            result = ("Operational issues : ", delays[i]['_id']['airport'], delays[i]['nb'])
        elif delays[i]['_id']['reason']==[['FSR03']]:
            result = ("delayed incoming aircraft : ", delays[i]['_id']['airport'], delays[i]['nb'])
        elif delays[i]['_id']['reason']==[['FSR04']]:
            result =("delayed cabin crew : ", delays[i]['_id']['airport'], delays[i]['nb'])
        elif delays[i]['_id']['reason']==[['FSR05']]:
            result = ("no gate available : ", delays[i]['_id']['airport'], delays[i]['nb'])
        else:
            result = {}
        delays_text.append(result)
    return delays_text


@api.get("/delays/{flight_number: int}", name = "Flight delay information by flight number", tags = ['Delay'])
def get_delay(flight_number):
    """ Return information for delayed flights such as the n°1957 and n°1855 versus n°161. The number of the flight shall be precised."""
    collection = mongo()
    flight = list(collection.find({"flightNumber":int(flight_number)}, {"_id":0, "flightNumber": 1}))
    flight_bis = list(collection.find({"flightStatusPublic":"DELAYED_DEPARTURE"}, {"_id":0, "flightNumber": 1}))
    if len(flight) ==0:
        raise HTTPException(status_code=404, detail="Not found : No flight with this number in the mongodb database")
    elif len(flight_bis) ==0:
        return "The flight arrived on time. No delay."
    else:
        delays_flight_number = list(collection.find({"flightNumber":int(flight_number)},\
        {"_id":0, "flightNumber": 1, "flightLegs.irregularity.delayInformation.delayReasonPublicShort":1}))
        return delays_flight_number
        

@api.get("/delays/{IATA: str}", name = "Flight delayed by airport IATA code", tags = ['Delay'])
def get_delays(IATA):
    collection = mongo()
    delays_by_airport = list(collection.aggregate([
    {"$match": {"$and": [{"flightStatusPublic":"DELAYED_DEPARTURE"}, {"flightLegs.departureInformation.airport.code":str(IATA)}]}},
    {"$group": {"_id": "$flightLegs.departureInformation.airport.code", "nb_delay": {"$sum":1}}},
    {"$sort":{"nb_delay":-1}}]))
    if IATA not in list(iata["IATA"]):
        raise HTTPException(status_code=400, detail="Bad Request : Invalid IATA code")
    elif len(delays_by_airport)==0:
        return "On-time departure"
    else:
        return delays_by_airport

'''
Note:
- Possible further studies regarding flight delays :
-- In term of lenght of time (comparison between "times.scheduled": "2023-09-21T11:50:00.000+02:00 and "estimatedArrival": "2023-09-21T12:19:00.000+02:00")
-- In term of date
-- In term of country etc
Correlation between meteo conditions from https://www.accuweather.com API for instance and "delayed incoming aircraft" 
'''




