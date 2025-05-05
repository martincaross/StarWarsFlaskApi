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
from models import db, User, People, Planets, Vehicles, Favorites
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
def get_all_users():

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Verificar si ya existe el favorito
    existing_fav = Favorites.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if existing_fav:
        return jsonify({"error": "Favorite already exists"}), 409

    favorite = Favorites(user_id=user_id, planets_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Verificar si ya existe el favorito
    existing_fav = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_fav:
        return jsonify({"error": "Favorite already exists"}), 409

    favorite = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Verificar si ya existe el favorito
    existing_fav = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if existing_fav:
        return jsonify({"error": "Favorite already exists"}), 409

    favorite = Favorites(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get("user_id")

    favorite = Favorites.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = request.args.get("user_id")

    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite person deleted"}), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = request.args.get("user_id")

    favorite = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite vehicle deleted"}), 200


#People

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    body = request.get_json()
    if not body or "name" not in body:
        return jsonify({"error": "Missing 'name' field"}), 400
    new_person = People(name=body["name"])
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 201

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.get(people_id)

    if person is None:
        return jsonify({"error": "Character not found"}), 404

    db.session.delete(person)
    db.session.commit()

    return jsonify({"message": f"Character with ID {people_id} has been deleted"}), 200


# Planets

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    # Buscar un registro de Planet por ID
    planet = Planets.query.get(planet_id)
    
    # Si no se encuentra el planeta, devolvemos un error 404
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    # Si lo encontramos, devolvemos la información serializada
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    if not body or "name" not in body:
        return jsonify({"error": "Missing 'name' field"}), 400
    new_planet = Planets(name=body["name"])
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": f"Planet with ID {planet_id} has been deleted"}), 200

# Vehicles

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    # Buscar un registro de Planet por ID
    vehicle = Vehicles.query.get(vehicle_id)
    
    # Si no se encuentra el planeta, devolvemos un error 404
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    
    # Si lo encontramos, devolvemos la información serializada
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = request.get_json()
    if not body or "name" not in body:
        return jsonify({"error": "Missing 'name' field"}), 400
    new_vehicle = Vehicles(name=body["name"])
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": f"Vehicle with ID {vehicle_id} has been deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
