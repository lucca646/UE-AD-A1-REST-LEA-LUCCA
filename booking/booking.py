from flask import Flask, jsonify, request
import json
from pathlib import Path
import requests
from werkzeug.exceptions import NotFound


app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
BOOKINGS_FILE = Path(__file__).resolve().parent / 'databases' / 'bookings.json'
USERS_API_URL = 'http://localhost:3203'
SCHEDULE_API_URL = 'http://localhost:3202'
MOVIES_API_URL = 'http://localhost:3200'


with open(BOOKINGS_FILE, "r") as jsf:
   bookings = json.load(jsf)["bookings"]

def read():
    with open(BOOKINGS_FILE, 'r') as jsf:
        bookings = json.load(jsf)["bookings"]
        return bookings

def readByUserId(user_id):
    bookings_list = read()
    for booking in bookings_list:
        if booking["userid"] == user_id:
            return booking


def write(new_booking):

    with open(BOOKINGS_FILE, 'r') as jsf:
        full = json.load(jsf)


    with open(BOOKINGS_FILE, 'w') as f:
        full["bookings"].append(new_booking)

        json.dump(full, f, indent=4)
        print("ok")


@app.route("/bookings/<userId>", methods=['GET'])
def getAllBookings(user_id):
    try:
        user_response = requests.get(
            f"{USERS_API_URL}/users/{user_id}"
        ).json()
    except requests.RequestException as error:
        return "Connexion avec l'API impossible"

    if user_response.get('id') == "admin":
        return read()
    else:
        return "L'accès à cette ressource est interdit pour cet utilisateur", 403


@app.route("/bookings/<userId>", methods=['GET'])
def getBookingByUserId(userId):
    return readByUserId(userId)


@app.route("/bookings", methods=['POST'])
def createBooking():
    data = request.get_json()

    user_id = data.get('userid')
    date = data.get('date')
    movie_id = data.get('movies')
    
    try:
        schedule_response = requests.get(
            f"{SCHEDULE_API_URL}/times/{date}"
        ).json()
        user_response = requests.get(
                    f"{USERS_API_URL}/users/{user_id}"
                ).json()
        movie_response = requests.get(
                            f"{MOVIES_API_URL}/movies/{movie_id}"
                        ).json()
    except requests.RequestException as error:
        return "Connexion avec l'API impossible", 503

    #TODO verif ce que renvoie l'url quand user_id n'existe pas et renvoyer une erreur 404

    schedule_movies = schedule_response.get('movies', [])
    if movie_id not in schedule_movies:
        return f"Le film {movie_id} n'est pas disponible à la date {date}", 400
    else:
        booking_already_exists = readByUserId(user_id)
        if booking_already_exists:
            bookings_list = read()
            bookings_list.remove(booking_already_exists)
            booking_already_exists["dates"].extend(data.get('dates'))
            if date not in [d["date"] for d in booking_already_exists["dates"]]:
                booking_already_exists["dates"].append({"date": date, "movies": [movie_id]})
            else:
                for d in booking_already_exists["dates"]:
                    if d["date"] == date:
                        d["movies"].append(movie_id)
            with open(BOOKINGS_FILE, 'w') as f:
                json.dump({"bookings": bookings_list}, f, indent=3)
        else:
            new_booking = {
            "date": data.get('date'),
            "movies": data.get('movies')
            }
            write(new_booking)

    return bookings_list


@app.route("/bookings/<userId>", methods=['DELETE'])
def deleteBookingByUserId(userId):
    booking = readByUserId(userId)
    if not booking:
        raise NotFound("bookings not found")
    else:
        bookings_list = read()
        bookings_list.remove(booking)
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump({"bookings": bookings_list}, f, indent=3)
        return bookings_list

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
