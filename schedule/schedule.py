from flask import Flask, request, jsonify, make_response
import json
from pathlib import Path
from werkzeug.exceptions import NotFound
import time

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'
TIMES_FILE = Path(__file__).resolve().parent / 'databases' / 'times.json'

with open(TIMES_FILE, "r") as jsf:
   schedule = json.load(jsf)["schedule"]

def read():
    with open(TIMES_FILE, 'r') as jsf:
        times = json.load(jsf)["schedule"]
        return times

def readByDate(date):
    times_list = read()
    for time in times_list:
        if time["date"] == date:
            return time


def write(new_time):
    
    with open(TIMES_FILE, 'r') as jsf:
        full = json.load(jsf)


    with open(TIMES_FILE, 'w') as f:
        full["schedule"].append(new_time)

        json.dump(full, f, indent=4)
        print("ok")
 
 
@app.route("/times", methods=['GET'])
def getAllTimes():

    return read()
    
    
@app.route("/times/<timeDate>", methods=['GET'])
def getTimeByDate(timeDate):
    return readByDate(timeDate)


@app.route("/times", methods=['POST'])
def createTime():
    data = request.get_json()

    time_already_exists = readByDate(data.get('date'))
    if time_already_exists:
        times_list = read()
        times_list.remove(time_already_exists)
        time_already_exists["movies"].extend(data.get('movies'))
        times_list.append(time_already_exists)
        with open(TIMES_FILE, 'w') as f:
            json.dump({"schedule": times_list}, f, indent=3)
    else:
        new_time = {
        "date": data.get('date'),
        "movies": data.get('movies')
        }
        write(new_time)

    return new_time


@app.route("/times/<timeDate>", methods=['DELETE'])
def deleteTimeByDate(timeDate):
    time = readByDate(timeDate)
    if not time:
        raise NotFound("schedule not found")
    else:
        times_list = read()
        times_list.remove(time)
        with open(TIMES_FILE, 'w') as f:
            json.dump({"schedule": times_list}, f, indent=3)
        return times_list

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
