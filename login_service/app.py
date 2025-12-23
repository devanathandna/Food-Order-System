from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Config
MONGO_URI = "mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain"
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
users_collection = db.users_service_collection

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users_collection.find_one({"username": username})
    
    if user and user['password'] == password:
        return jsonify({"token": f"fake-jwt-token-{username}", "message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # New Fields
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')
    city = data.get('city')
    
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400
        
    user_doc = {
        "username": username,
        "password": password,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "city": city
    }
    users_collection.insert_one(user_doc)
    return jsonify({"message": "User registered"}), 201

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = users_collection.find_one({"username": username}, {'_id': 0, 'password': 0})
    if user: return jsonify(user)
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    print("Login Service running on port 5002")
    app.run(port=5002, debug=True)
