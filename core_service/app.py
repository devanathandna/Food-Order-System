from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)

# MongoDB Config - Use environment variable for security
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain')
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
users_collection = db.users_service_collection
hotels_collection = db.hotels_service_collection

# Admin Credentials - Use environment variables for security
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')

# --- LOGIN / AUTH ROUTES ---

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users_collection.find_one({"username": username})
    if user and user['password'] == password:
        return jsonify({"token": f"fake-jwt-token-{username}", "message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400
        
    user_doc = {
        "username": username,
        "password": data.get('password'),
        "name": data.get('name'),
        "phone": data.get('phone'),
        "email": data.get('email'),
        "address": data.get('address'),
        "city": data.get('city')
    }
    users_collection.insert_one(user_doc)
    return jsonify({"message": "User registered"}), 201

@app.route('/auth/user/<username>', methods=['GET'])
def get_user(username):
    user = users_collection.find_one({"username": username}, {'_id': 0, 'password': 0})
    if user: return jsonify(user)
    return jsonify({"message": "User not found"}), 404

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('username') == ADMIN_USER and data.get('password') == ADMIN_PASS:
        return jsonify({"token": "admin-secret-token", "message": "Admin logged in"}), 200
    return jsonify({"message": "Invalid Admin Credentials"}), 401

@app.route('/admin/add_hotel', methods=['POST'])
def add_hotel():
    # Direct DB insertion (Merged from hotel_service)
    data = request.json
    if not data.get('name'): return jsonify({"message": "Name required"}), 400
    
    last_hotel = hotels_collection.find_one(sort=[("id", -1)])
    new_id = (last_hotel['id'] + 1) if last_hotel else 1
    
    new_hotel = {
        "id": new_id,
        "name": data.get('name'),
        "address": data.get('address'),
        "city": data.get('city'),
        "menu": data.get('menu', [])
    }
    hotels_collection.insert_one(new_hotel)
    return jsonify({"message": "Hotel created", "id": new_id}), 201

@app.route('/admin/add_item', methods=['POST'])
def add_item():
    data = request.json
    hotel_id = data.get('hotel_id')
    
    # Generate Item ID
    import time
    item_id = int(time.time() * 1000) % 100000 
    
    new_item = {"id": item_id, "name": data.get('name'), "price": float(data.get('price'))}
    
    result = hotels_collection.update_one(
        {"id": int(hotel_id)},
        {"$push": {"menu": new_item}}
    )
    if result.modified_count:
        return jsonify({"message": "Item added", "item_id": item_id}), 200
    return jsonify({"message": "Hotel not found"}), 404

@app.route('/admin/add_delivery_person', methods=['POST'])
def add_delivery_person():
    data = request.json
    hotel_id = data.get('hotel_id')
    if not hotel_id: return jsonify({"message": "Hotel ID required"}), 400
        
    person = {
        "name": data.get('name'),
        "phone": data.get('phone'),
        "city": data.get('city'),
        "charge": float(data.get('charge', 0))
    }
    result = hotels_collection.update_one(
        {"id": int(hotel_id)},
        {"$set": {"delivery_person": person}}
    )
    if result.modified_count:
        return jsonify({"message": "Delivery Person Added to Hotel"}), 201
    return jsonify({"message": "Hotel not found"}), 404

# --- HOTEL PUBLIC ROUTES ---

@app.route('/hotel/list', methods=['GET'])
def list_hotels():
    hotels = list(hotels_collection.find({}, {'_id': 0}))
    return jsonify(hotels)

@app.route('/hotel/<int:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = hotels_collection.find_one({"id": hotel_id}, {'_id': 0})
    if hotel: return jsonify(hotel)
    return jsonify({"message": "Hotel not found"}), 404


if __name__ == '__main__':
    # Render provides PORT environment variable
    port = int(os.environ.get('PORT', 5002))
    print(f"Core Service running on port {port}")
    # host='0.0.0.0' is required for Render to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False)
