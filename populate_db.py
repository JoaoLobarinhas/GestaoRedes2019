# /usr/bin/env python3

import urllib.request, json
from pymongo import MongoClient
import time
import subprocess

print("Server running...")

client = MongoClient('mongodb://localhost/')
db = client.snmpData
print("Connected to db...")

configs = db.configs
datas = db.datas
getSystemInfo = {}

def reset_commands():
    getSystemInfo['UpTime'] = "snmpstatus -c public -v 2c localhost | awk -F 'Up:' '{print $2}'"
    getSystemInfo['ComputerName'] = "snmpstatus -c public -v 2c localhost | awk -F 'UDP:' '{print $2}' | awk '{print $2}'"
    getSystemInfo['NetworkIP'] = "snmpstatus -c public -v 2c localhost | awk -F '[' '{print $3}' | awk -F ']' '{print $1}'"


def execute_insert(collection):
    # with urllib.request.urlopen(url_json) as url:
    #     data = json.loads(url.read().decode())
    reset_commands()

    for i in getSystemInfo:
        # get output from command executed
        process = subprocess.run(getSystemInfo[i], shell=True, stdout=subprocess.PIPE)
        getSystemInfo[i] = process.stdout.decode('utf-8')
        print(getSystemInfo[i])

    # collection.insert_one(data)
    # client.close()


#KEEP THE SERVER RUNNING ON A LOOP
while True:

    execute_insert(configs)

    print("Row was inserted!")
    # WAIT BEFORE RERUNNING
    time.sleep(30 - time.time() % 30)
