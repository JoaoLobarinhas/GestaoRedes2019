import urllib.request, json
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import asyncio
import time
import sys
import subprocess
import json

print("Server running...")

client = MongoClient('mongodb://localhost/')
db = client.snmpData
print("Connected to db...")

configs = db.configs
getSystemInfo = {}

ip = sys.argv[1]
port = sys.argv[2]
reptime = sys.argv[3]
_id = ObjectId(sys.argv[4])

aux_cmd = ip+":"+port
print("Worker id: "+str(_id))
print("IP: "+ip)
print("Port: "+port)

class Proces:

    def __init__(self, oid, name):
        self.oid = oid
        self.name = name

class Disk:

    def __init__(self,diskSpace,diskSpacePerc,diskSpaceUsed):
        self.space = diskSpace
        self.usedPerc = diskSpacePerc
        self.spaceused = diskSpaceUsed

class Ram:

    def __init__(self,ramSpace,ramSpaceFree,ramSpaceUsed,ramMemShared,ramMemBuffer,ramMemCached):
        self.size = ramSpace
        self.freeSpace = ramSpaceFree
        self.usedSpace = ramSpaceUsed
        self.shared = ramMemShared
        self.buffer = ramMemBuffer
        self.cache = ramMemCached

class CPU:

    def __init__(self,cpuUsage,cpuSystem,cpuIdle):
        self.usage = cpuUsage
        self.system = cpuSystem
        self.idle = cpuIdle

class Packets:

    def __init__(self, recvPackets, transPackets, recvPacketsIp, transPacketsIp):
        self.recvPackets = recvPackets
        self.transPackets = transPackets
        self.recvPacketsIp = recvPacketsIp
        self.transPacketsIp = transPacketsIp 

class Data:

    def __init__(self,upTime, computerName, networkIp, interfaces, packets, disk, ram, cpu, process):
        self.updateTime = getTimeNow()
        self.upTime = upTime
        self.computerName = computerName
        self.networkIp = networkIp
        self.interfaces = interfaces
        self.packets = packets
        self.disk = disk
        self.ram = ram
        self.cpu = cpu
        self.process = process       

class Configs:

    def __init__(self, ip, port, lastUpdate, repTime):
        self.ip=ip
        self.port=port
        self.lastupdate=lastUpdate
        self.repTime = repTime
        self.data =  []


def getConfig(aux):

    getSystemInfo['UpTime'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'Up: ' '{print $2}'"
    getSystemInfo['ComputerName'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'UDP: ' '{print $2}' | awk '{print $2}'"
    getSystemInfo['NetworkIP'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F '[' '{print $3}' | awk -F ']' '{print $1}'"
    getSystemInfo['Interfaces'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'Interfaces: ' '{print $2}' | awk -F ',' '{print $1}'"
    getSystemInfo['RecvPackets'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'Recv/Trans packets: ' '{print $2}' | awk -F '/' '{print $1}'"
    getSystemInfo['TransPackets'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'Recv/Trans packets: ' '{print $2}' | awk -F '/' '{print $2}' | awk -F '|' '{print $1}'"
    getSystemInfo['RecvPacketsIP'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'IP: ' '{print $2}' | awk -F '/' '{print $1}'"
    getSystemInfo['TransPacketsIP'] = "snmpstatus -c public -v 2c "+ aux + " | awk -F 'IP: ' '{print $2}' | awk -F '/' '{print $2}'"
    getSystemInfo['DiskSpace'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.9.1.7.1 | awk -F 'INTEGER: ' '{print $2}'"
    getSystemInfo['DiskSpacePerc'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.9.1.9.1 | awk -F 'INTEGER: ' '{print $2}'"
    getSystemInfo['DiskSpaceUsed'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.9.1.7.1 | awk -F 'INTEGER: ' '{print $2}'"
    getSystemInfo['RAMspace'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.5.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['RAMspaceFree'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.11.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['RAMspaceUsed'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.6.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['RAMmemShared'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.13.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['RAMmemBuffer'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.14.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['RAMmemCached'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.4.15.0 | awk -F 'INTEGER: ' '{print $2}' | awk -F 'kB' '{print $1}'"
    getSystemInfo['CpuUsage'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.11.ssCpuRawUser.0 | awk -F 'Counter32: ' '{print $2}'"
    getSystemInfo['CpuSystem'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.11.ssCpuRawSystem.0 | awk -F 'Counter32: ' '{print $2}'"
    getSystemInfo['CpuIdle'] = "snmpget -v2c -c public "+ aux + "  .1.3.6.1.4.1.2021.11.ssCpuRawIdle.0 | awk -F 'Counter32: ' '{print $2}'"
    getProces = "snmpwalk -CI -v2c -c public "+aux+ " hrSWRunPath"

    for i in getSystemInfo:
        # get output from command executed
        process = subprocess.run(getSystemInfo[i], shell=True, stdout=subprocess.PIPE)
        getSystemInfo[i] = process.stdout.decode('utf-8').strip()
    
    process = subprocess.run(getProces, shell=True, stdout=subprocess.PIPE)
    getProces = (process.stdout.decode('utf-8').strip()).split('\n')
    processL = list()
    for x in getProces:
        if(" = STRING: " in x):
            i = x.split(" = STRING: ")
            i[1] = i[1].translate({ord('"'): None})
            processL.append(Proces(i[0],i[1]).__dict__)

    
    data = Data(getSystemInfo["UpTime"],getSystemInfo["ComputerName"],getSystemInfo["NetworkIP"], getSystemInfo["Interfaces"], Packets(getSystemInfo["RecvPackets"],getSystemInfo["TransPackets"],getSystemInfo["RecvPacketsIP"],getSystemInfo["TransPacketsIP"]).__dict__,
    Disk(getSystemInfo["DiskSpace"],getSystemInfo["DiskSpacePerc"],getSystemInfo["DiskSpaceUsed"]).__dict__, Ram(getSystemInfo["RAMspace"],getSystemInfo["RAMspaceFree"],getSystemInfo["RAMspaceUsed"],getSystemInfo["RAMmemShared"],getSystemInfo["RAMmemBuffer"],getSystemInfo["RAMmemCached"]).__dict__,
    CPU(getSystemInfo["CpuUsage"],getSystemInfo["CpuSystem"],getSystemInfo["CpuIdle"]).__dict__,processL)

    return data.__dict__


def checkIfDataChanged(date):

    aux = configs.find_one({"_id":_id})
    
    if aux["lastupdate"] != date:
        ip = aux["ip"]
        port = aux["port"]
        aux_cmd = ip+":"+port
        return True
    else:
        return False


def getTimeNow():
    now = datetime.now()
    dt_string = str(now.strftime("%d-%m-%Y %H:%M:%S"))
    return dt_string

def getData():
    cont=0
    data_aux=None
    try:
        while True:
            aux = configs.find_one({"_id":_id})
            if(aux["active"] == "true"):
                checkIfDataChanged(data_aux)
                print("Inseriu dados")
                configs.update_one({"_id":_id},{"$push":  {"data": getConfig(aux_cmd)}})
            else:
                break
            cont=cont+1
            #Aplicar o tempo de repetições
            time.sleep(30 - time.time() % 30)
    except KeyboardInterrupt:
        pass

getData()