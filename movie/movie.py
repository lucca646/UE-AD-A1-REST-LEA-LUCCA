from uuid import uuid4

from flask import Flask, request, jsonify, make_response
import json
import sys
from pathlib import Path
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
MOVIES_FILE = Path(__file__).resolve().parent / 'databases' / 'movies.json'

def read():
    with open(MOVIES_FILE, 'r') as jsf:
        movies = json.load(jsf)["movies"]
        print(movies)
        return movies

def readById(movieId):
    movies_list = read()
    for movie in movies_list:
        if movie["id"] == movieId:
            return movie



def write(new_movie):
    
    with open(MOVIES_FILE, 'r') as jsf:
        full = json.load(jsf)


    with open(MOVIES_FILE, 'w') as f:
        full["movies"].append(new_movie)
        print(full)

        json.dump(full, f, indent=4)
        print("ok")
 
 
print(read())


@app.route("/movies", methods=['GET'])
def getAllMovies():

    return read()
    
    
@app.route("/movies/<movieId>", methods=['GET'])
def getMovieById(movieId):
    return readById(movieId)


@app.route("/movies", methods=['POST'])
def createMovie():
    data = request.get_json()

    new_movie = {
      "title": data.get('title'),
      "rating": data.get('rating'),
      "director": data.get('director'),
      "id": str(uuid4())
    }

    write(new_movie)
    return make_response(jsonify({"message": "Movie created successfully"}), 201)


@app.route("/movies/<movieId>", methods=['PUT'])
def updateMovie(movieId):
    movie = readById(movieId)
    if not movie:
        raise NotFound("Movie with id {} not found".format(movieId))
    else:
        data = request.get_json()
        movie["title"] = data.get('title', movie["title"])
        movie["rating"] = data.get('rating', movie["rating"])
        movie["director"] = data.get('director', movie["director"])
        return make_response(jsonify({"message": "Movie updated successfully"}), 200)


@app.route("/movies/<movieId>", methods=['DELETE'])
def deleteMovieById(movieId):
    movie = readById(movieId)
    if not movie:
        raise NotFound("Movie with id {} not found".format(movieId))
    else:
        movies_list = read()
        movies_list.remove(movie)
        with open(MOVIES_FILE, 'w') as f:
            json.dump({"movies": movies_list}, f, indent=4)
        return make_response(jsonify({"message": "Movie deleted successfully"}), 200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
