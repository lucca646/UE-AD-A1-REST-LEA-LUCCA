from flask import Flask, request, jsonify, make_response
import json
from movie import movie
from user.user import readById
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

def read():
    with open('{}/databases/times.json'.format("."), 'r') as jsf:
        times = json.load(jsf)["times"]
        print(times)
        return times

def readByDate(date):
    times_list = read()
    for time in times_list:
        if time["date"] == date:
            return time


def write(new_time):
    
    with open('{}/databases/times.json'.format("."), 'r') as jsf:
        full = json.load(jsf)


    with open('{}/databases/times.json'.format("."), 'w') as f:
        full["times"].append(new_time)
        print(full)

        json.dump(full, f, indent=4)
        print("ok")
 
 
print(read())


@app.route("/times", methods=['GET'])
def getAllTimes():

    return read()
    
    
@app.route("/times/<timeDate>", methods=['GET'])
def getTimeByDate(timeDate):
    return readByDate(timeDate)


@app.route("/times", methods=['POST'])
def createTime():
    data = request.get_json()

    new_time = {
      "date": data.get('date'),
      "movies": data.get('movies')
    }

    write(new_time)
    return make_response(jsonify({"message": "Schedule created successfully"}), 201)


@app.route("/times/<timeDate>", methods=['DELETE'])
def deleteTimeByDate(timeDate):
    time = readByDate(timeDate)
    if not time:
        raise NotFound("Time with date {} not found".format(timeDate))
    else:
        times_list = read()
        times_list.remove(time)
        with open('{}/databases/times.json'.format("."), 'w') as f:
            json.dump({"times": times_list}, f, indent=4)
        return make_response(jsonify({"message": "Time deleted successfully"}), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
