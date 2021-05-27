import json
import os
from pathlib import Path

def getServerConfig(path):
  filepath = 'config/server.json'
  with open((path/filepath).resolve(), 'r') as server:
    jsonServerData = json.load(server)
    return jsonServerData

def getSystemConfig(path):
  filepath = 'config/system.json'
  with open((path/filepath).resolve(), 'r') as system:
    jsonSystemData = json.load(system)
    return jsonSystemData

def getBrokerAppConfig(path):
  filepath = 'config/brokerapp.json'
  with open((path/filepath).resolve(), 'r') as brokerapp:
    jsonUserData = json.load(brokerapp)
    return jsonUserData

def getHolidays(path):
  filepath = 'config/holidays.json'
  with open((path/filepath).resolve(), 'r') as holidays:
    holidaysData = json.load(holidays)
    return holidaysData

def getTimestampsData():
  serverConfig = getServerConfig(Path(__file__).parent.parent)
  timestampsFilePath = os.path.join(serverConfig['deployDir'], 'timestamps.json')
  if os.path.exists(timestampsFilePath) == False:
    return {}
  timestampsFile = open(timestampsFilePath, 'r')
  timestamps = json.loads(timestampsFile.read())
  return timestamps

def saveTimestampsData(timestamps = {}):
  serverConfig = getServerConfig(Path(__file__).parent.parent)
  timestampsFilePath = os.path.join(serverConfig['deployDir'], 'timestamps.json')
  with open(timestampsFilePath, 'w') as timestampsFile:
    json.dump(timestamps, timestampsFile, indent=2)
  print("saved timestamps data to file " + timestampsFilePath)
