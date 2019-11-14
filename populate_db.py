# /usr/bin/env python3

import urllib.request, json
from pymongo import MongoClient
import time


print("Server running...")

client = MongoClient('mongodb://localhost/')
db = client.sensors
print("Connected to db...")
    #print(db.sensors.find_one({'borough':'Bronx'}))

cardiac = db.cardiac
blood = db.blood

def execute_insert(collection, id_collection):
    url_json = 'http://nosql.hpeixoto.me/api/sensor/' + id_collection + '00' + str(url_end)
    print("Inserting from " + url_json)

    with urllib.request.urlopen(url_json) as url:
        data = json.loads(url.read().decode())

    url_total = data['number_of_sensors']

    collection.insert_one(data)
    client.close()

    return url_total


#KEEP THE SERVER RUNNING ON A LOOP
while True:
    url_total = 1
    url_end = 1

    # LOOP THROUGH ALL SENSORS
    while True:
        url_total = execute_insert(cardiac, "3")
        execute_insert(blood, "4")

        # CHANGE URL TO FETCH
        url_end += 1
        if(url_end > url_total-1):
            break;


    print("Row was inserted!")
    # WAIT BEFORE RERUNNING
    time.sleep(30 - time.time() % 30)
