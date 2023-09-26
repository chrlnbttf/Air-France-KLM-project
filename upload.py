'''
This document aims at requesting the api airfranceklm, selecting the content and ensuring a smooth data transfer to mongoDB without duplicates.
'''

import requests
import os
import json
import pymongo
from pymongo import MongoClient
from pprint import pprint
import pandas as pd



###### API : Import api data (+ data insight))

raw_document = requests.get('https://api.airfranceklm.com/opendata/flightstatus', headers={'API-Key': f"j8fvdtamampvx3txsttx2u99"})
data = raw_document.json()
#pprint(data) # Data insight with pretty print


###### MongoDB : Create the database, collection and index to prevent duplicates

client = pymongo.MongoClient("mongodb://host.docker.internal:27017/")

database = client["Airline_Flight_Status"]
collection = database["flightstatus"]
#collection.create_index("id", unique=True)
document = collection.find_one()


###### Data manipulation : Create usable data format compatible with database (+ data insight)

data_subset = data["operationalFlights"]

#Data insight
print(len(data_subset))
print(len(data_subset[0]))
print(data_subset[0].keys())
print(data_subset[0]["flightNumber"])
print(data_subset[1]["flightNumber"])
#print(data_subset[0])


###### Document : Enrich database with api and json file archives (+ data insight)

'''
collection.insert_many(data_subset) # Inserts documents directly from api
'''

with open("airfrance_20230926.json", "w") as write_file: # Create daily json files from api (to automatize)
    json.dump(data_subset, write_file)                 

with open('airfrance_20230926.json') as f: # Inserts json file data into MongoDB
    file_data = json.load(f)
collection.insert_many(file_data)


# Data insight
print("The number of flights is : ", collection.count_documents({}))
print("The database name is : ", client.list_database_names())
print("The collection name is :", database.list_collection_names())
print("The index of the collection is : ", collection.index_information())
#print("An example of flight data is :", document)
print("The number of flights is : ", collection.count_documents({}))



#Database maintenance commands :
#collection.drop_indexes()
#collection.delete_many({})



