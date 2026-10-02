from uuid import uuid4

from flask import Flask, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

def read():
    with open('{}/databases/users.json'.format("."), 'r') as jsf:
        users = json.load(jsf)["users"]
        print(users)
        return users

def readById(userId):
    users_list = read()
    for user in users_list:
        if user["id"] == userId:
            return user



def write(new_user):
    
    with open('{}/databases/users.json'.format("."), 'r') as jsf:
        full = json.load(jsf)


    with open('{}/databases/users.json'.format("."), 'w') as f:
        full["users"].append(new_user)
        print(full)

        json.dump(full, f, indent=4)
        print("ok")
 
 
print(read())


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
    return make_response(jsonify({"message": "User created successfully"}), 201)


@app.route("/users/<userId>", methods=['PUT'])
def updateUser(userId):
    user = readById(userId)
    if not user:
        raise NotFound("User with id {} not found".format(userId))
    else:
        data = request.get_json()
        user["name"] = data.get('name', user["name"])
        user["last_active"] = data.get('last_active', user["last_active"])
        user["id"] = data.get('name', user["name"])
        return make_response(jsonify({"message": "User updated successfully"}), 200)


@app.route("/users/<userId>", methods=['DELETE'])
def deleteUserById(userId):
    user = readById(userId)
    if not user:
        raise NotFound("User with id {} not found".format(userId))
    else:
        users_list = read()
        users_list.remove(user)
        with open('{}/databases/users.json'.format("."), 'w') as f:
            json.dump({"users": users_list}, f, indent=4)
        return make_response(jsonify({"message": "User deleted successfully"}), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
