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
    try:
        requests.get(
            f"{USERS_API_URL}/users/{user_id}"
        ).json()
    except requests.RequestException:
        return "Cet utilisateur.rice n'existe pas"
    for booking in bookings_list:
        if booking["userid"] == user_id:
            return booking
    return "Cet utilisateur.rice n'a aucune réservation"


def write(new_booking):

    with open(BOOKINGS_FILE, 'r') as jsf:
        full = json.load(jsf)

    with open(BOOKINGS_FILE, 'w') as f:
        full["bookings"].append(new_booking)

        json.dump(full, f, indent=4)
        print("ok")


@app.route("/bookings/all/<userId>", methods=['GET'])
def getAllBookings(userId):
    try:
        user_response = requests.get(
            f"{USERS_API_URL}/users/{userId}"
        ).json()
    except requests.RequestException:
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
    date = data.get('dates')[0]["date"]
    movie_id = data.get('dates')[0]["movies"][0]

    does_user_exist = readByUserId(user_id)
    if isinstance(does_user_exist, str):
        return does_user_exist

    try:
        schedule_response = requests.get(
            f"{SCHEDULE_API_URL}/times/{date}"
        ).json()
        requests.get(
            f"{MOVIES_API_URL}/movies/{movie_id}"
        ).json()
    except requests.RequestException:
        return "Connexion avec l'API impossible", 503

    schedule_movies = schedule_response.get('movies', [])
    if movie_id not in schedule_movies:
        return f"Le film {movie_id} n'est pas disponible à la date {date}", 400
    else:
        booking_already_exists = readByUserId(user_id)
        if not isinstance(booking_already_exists, str):
            bookings_list = read()
            bookings_list.remove(booking_already_exists)
            # vérifie si la date est déjà présente dans les réservations sinon renvoie none
            booking_date = next(
                (date_entry for date_entry in booking_already_exists["dates"]
                 if date_entry["date"] == date),
                None
            )
            # si la date n'existe pas on la rajoute
            if booking_date is None:
                booking_already_exists["dates"].append({
                    "date": date,
                    "movies": [movie_id]
                })
            # si la date existe mais que le film n'est pas encore réservé on l'ajoute
            elif movie_id not in booking_date["movies"]:
                booking_date["movies"].append(movie_id)

            bookings_list.append(booking_already_exists)
            with open(BOOKINGS_FILE, 'w') as f:
                json.dump({"bookings": bookings_list}, f, indent=3)
        else:
            new_booking = {
            "userid": user_id,
            "dates": [{"date": date, "movies": [movie_id]}]
            }
            write(new_booking)

    bookings_list = read()
    return bookings_list


@app.route("/bookings/<userId>", methods=['DELETE'])
def deleteBookingByUserId(userId):
    bookings_list = read()
    if userId not in [booking["userid"] for booking in bookings_list]:
        return "Cet utilisateur.rice n'a aucune réservation"
    for booking in bookings_list:
        if booking["userid"] == userId:
            bookings_list.remove(booking)
            break
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump({"bookings": bookings_list}, f, indent=3)
    return bookings_list

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
