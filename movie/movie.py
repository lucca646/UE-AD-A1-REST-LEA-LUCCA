from flask import Flask, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

def read():
    with open('{}/databases/movies.json'.format("."), 'r') as jsf:
        movies = json.load(jsf)["movies"]
        print(movies)
        return movies

def readById(movieId):
    movies_list = read()
    for movie in movies_list:
        if movie["id"] == movieId:
            return movie



def write(new_movie):
    
    with open('{}/databases/movies.json'.format("."), 'r') as jsf:
        full = json.load(jsf)


    with open('{}/databases/movies.json'.format("."), 'w') as f:
        full["movies"].append(new_movie)
        print(full)

        json.dump(full, f, indent=4)
        print("ok")
 
print(read())

new_movie = {
      "title": "TTest",
      "rating": 2.4,
      "director": "Lea",
      "id": "840d006c-3a57-5-b18f-9b713b073f3c"
    }

write(new_movie)


@app.route("/movies", methods=['GET'])
def getAllMovies():

    return read()
    
    
@app.route("/movies/<movieId>", methods=['GET'])
def getMovieById(movieId):
    print("ici")
    return readById(movieId)


@app.route("/movies/<movieId>", methods=['POST'])
def createMovie(movieId):
    data = request.get_json()

    director = data.get('director')
    title = data.get('title')
    rating = data.get('rating')
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/movies/<movieId>", methods=['PUT'])
def updateMovie(movieId):
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/movies/<movieId>", methods=['DELETE'])
def deleteMovieById(movieId):
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
