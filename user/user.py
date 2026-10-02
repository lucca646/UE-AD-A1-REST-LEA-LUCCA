from uuid import uuid4
import time
from flask import Flask, request
import requests
import json
from pathlib import Path

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
USERS_FILE = Path(__file__).resolve().parent / 'databases' / 'users.json'


with open(USERS_FILE, "r") as jsf:
   users = json.load(jsf)["users"]

def read():
    with open(USERS_FILE, 'r') as jsf:
        users = json.load(jsf)["users"]
        return users

def readById(userId):
    users_list = read()
    for user in users_list:
        if user["id"] == userId:
            return user



def write(new_user):
    
    with open(USERS_FILE, 'r') as jsf:
        full = json.load(jsf)


    with open(USERS_FILE, 'w') as f:
        full["users"].append(new_user)

        json.dump(full, f, indent=4)
        print("ok")
 
 

@app.route("/users", methods=['GET'])
def getAllUsers():

    return read()
    
    
@app.route("/users/<userId>", methods=['GET'])
def getUserById(userId):
    return readById(userId)


@app.route("/users", methods=['POST'])
def createUser():
    data = request.get_json()

    new_user = {
      "name": data.get('name'),
      "last_active": data.get('last_active'),
      "id": data.get('name')
    }

    write(new_user)
    return new_user


@app.route("/users/<userId>", methods=['PUT'])
def updateUser(userId):
    user = readById(userId)
    if not user:
        return "user not found"
    else:
        users_list = read()
        users_list.remove(user)
        data = request.get_json()
        user["name"] = data.get('name')
        user["last_active"] = int(time.time())

        users_list.append(user)
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": users_list}, f, indent=3)
            
        return user


@app.route("/users/<userId>", methods=['DELETE'])
def deleteUserById(userId):
    user = readById(userId)
    if not user:
        return "user not found"
    else:
        users_list = read()
        users_list.remove(user)
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": users_list}, f, indent=3)
        return users_list


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
