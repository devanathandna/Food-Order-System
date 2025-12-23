from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GATEWAY_URL = "http://localhost:5000"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@app.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == ADMIN_USER and password == ADMIN_PASS:
        return jsonify({"token": "admin-secret-token", "message": "Admin logged in"}), 200
    return jsonify({"message": "Invalid Admin Credentials"}), 401

@app.route('/add_hotel', methods=['POST'])
def add_hotel():
    # Proxy to Hotel Service
    data = request.json
    # data should contain name, address, city, menu
    resp = requests.post(f"{GATEWAY_URL}/hotel/create", json=data)
    return jsonify(resp.json()), resp.status_code

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    hotel_id = data.get('hotel_id')
    resp = requests.post(f"{GATEWAY_URL}/hotel/{hotel_id}/add_item", json=data)
    return jsonify(resp.json()), resp.status_code

@app.route('/add_delivery_person', methods=['POST'])
def add_delivery_person():
    data = request.json
    resp = requests.post(f"{GATEWAY_URL}/hotel/add_delivery_person", json=data)
    return jsonify(resp.json()), resp.status_code

@app.route('/update_price', methods=['PUT'])
def update_price():
    data = request.json
    hotel_id = data.get('hotel_id')
    resp = requests.put(f"{GATEWAY_URL}/hotel/{hotel_id}/update_price", json=data)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    print("Admin Service running on port 5006")
    app.run(port=5006, debug=True)
