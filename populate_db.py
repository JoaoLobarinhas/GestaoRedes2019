# /usr/bin/env python3

import urllib.request, json
from pymongo import MongoClient
import time
import subprocess
from bson.objectid import ObjectId
from subprocess import Popen, PIPE, call
from bson.json_util import dumps

print("Server running...")

client = MongoClient('mongodb://localhost/')
db = client.snmpData
print("Connected to db...")

configs = db.configs      

def execute_insert():
    current_data=list()
    try:
        while True:
            aux = list(configs.find({},{"ip":1,"port":1,"repTime":1,"active":1}))
            if len(current_data) == 0:
                for x in aux:
                    print(x)
                    if x["active"] == "true":
                        print(x)
                        cmd = "gnome-terminal -x sh -c 'python3 /home/lobarinhas/Desktop/GestaoRedes2019/execute.py "+x["ip"]+" "+x["port"]+" "+x["repTime"]+" "+ str(x['_id'])+";bash'"
                        Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                        current_data.append(x)
                        print(current_data)
            elif( len(current_data) != len(aux)):
                for x in aux:
                    if not current_data.__contains__(x):
                        print(True)
                        if x["active"] == "true":
                            cmd = "gnome-terminal -x sh -c 'python3 /home/lobarinhas/Desktop/GestaoRedes2019/execute.py "+x["ip"]+" "+x["port"]+" "+x["repTime"]+" "+ str(x['_id'])+";bash'"
                            Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                            current_data.append(x)
            time.sleep(30 - time.time() % 30)
    except KeyboardInterrupt:
        pass

## Fazer com que ele consiga criar mais terminais caso seja necessario
execute_insert()
