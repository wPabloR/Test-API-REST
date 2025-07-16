"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Airport, Flight, Book
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():

    all_users = db.session.query(User).all()
    result = [user.serialize() for user in all_users]

    response_body = {
        "users": result
    }

    return jsonify(response_body), 200

@app.route('/flights', methods=['GET'])
def get_flight():

    all_flights = db.session.query(Flight).all()
    result = [flight.serialize() for flight in all_flights]

    response_body = {
        "flights": result
    }

    return jsonify(response_body), 200

@app.route('/airports', methods=['GET'])
def get_airports():

    all_airports = db.session.query(Airport).all()
    result = [airport.serialize() for airport in all_airports]

    response_body = {
        "airports": result
    }

    return jsonify(response_body), 200

@app.route('/bookings', methods=['GET'])
def get_books():

    all_bookings = db.session.query(Book).all()
    result = [book.serialize() for book in all_bookings]

    response_body = {
        "bookings": result
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    response_body = {
        "user": user.serialize()
    }

    return jsonify(response_body), 200


@app.route('/users/<int:user_id>/flights-detailed', methods=['GET'])
def get_user_flights(user_id):

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    detailed = [{
        "booking": booking.serialize(),
        "flight": booking.flight.serialize() 
    } for booking in user.books]

    response_body = {
        "flights": detailed
    }

    return jsonify(response_body), 200

@app.route('/airports/<int:airport_id>/flights', methods=['GET'])
def get_airport_flights(airport_id):

    airport = db.session.get(Airport, airport_id)
    if airport is None:
        return jsonify({"error": "Airport not found"}), 404
    
    flights = [flight.serialize() for flight in airport.flights]

    response_body = {
        "flights": flights
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
