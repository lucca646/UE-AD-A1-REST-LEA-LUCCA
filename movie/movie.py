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
    for k in read():
        if k == movieId:
            return k


def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        full = {}
        full['movies']=movies
        json.dump(full, f)



@app.route("/movies", methods=['GET'])
def getAllMovies():
    return read()
    
    
@app.route("/movies/<movieId>", methods=['GET'])
def getMovieById(movieId):
    return readById(movieId)
    # return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/movies/<movie-id>", methods=['POST'])
def createMovie():
    data = request.get_json()

    director = data.get('director')
    title = data.get('title')
    rating = data.get('rating')
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/movies/<movie-id>", methods=['PUT'])
def updateMovie():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/movies/<movie-id>", methods=['DELETE'])
def deleteMovieById():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
