from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Config
MONGO_URI = "mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain"
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
hotels_collection = db.hotels_service_collection
delivery_collection = db.delivery_service_collection

@app.route('/create', methods=['POST'])
def create_hotel():
    data = request.json
    if not data.get('name'): return jsonify({"message": "Name required"}), 400
    
    last_hotel = hotels_collection.find_one(sort=[("id", -1)])
    new_id = (last_hotel['id'] + 1) if last_hotel else 1
    
    new_hotel = {
        "id": new_id,
        "name": data.get('name'),
        "address": data.get('address'),
        "city": data.get('city'),
        "menu": data.get('menu', []) # Expecting array of {name, quantity, price}
    }
    hotels_collection.insert_one(new_hotel)
    return jsonify({"message": "Hotel created", "id": new_id}), 201

@app.route('/add_delivery_person', methods=['POST'])
def add_delivery_person():
    data = request.json
    hotel_id = data.get('hotel_id')
    
    if not hotel_id:
        return jsonify({"message": "Hotel ID required"}), 400
        
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

@app.route('/<int:hotel_id>/add_item', methods=['POST'])
def add_item(hotel_id):
    data = request.json
    item_name = data.get('name')
    price = data.get('price')
    
    # Generate Item ID
    # Use a simple timestamp-ish or random for simplicity, or find max in menu
    import time
    item_id = int(time.time() * 1000) % 100000 
    
    new_item = {"id": item_id, "name": item_name, "price": float(price)}
    
    result = hotels_collection.update_one(
        {"id": hotel_id},
        {"$push": {"menu": new_item}}
    )
    
    if result.modified_count:
        return jsonify({"message": "Item added", "item_id": item_id}), 200
    return jsonify({"message": "Hotel not found"}), 404

@app.route('/<int:hotel_id>/update_price', methods=['PUT'])
def update_price(hotel_id):
    data = request.json
    item_id = data.get('item_id')
    new_price = data.get('price')
    
    result = hotels_collection.update_one(
        {"id": hotel_id, "menu.id": int(item_id)},
        {"$set": {"menu.$.price": float(new_price)}}
    )
    
    if result.modified_count:
        return jsonify({"message": "Price updated"}), 200
    return jsonify({"message": "Item not found"}), 404

@app.route('/list', methods=['GET'])
def list_hotels():
    hotels = list(hotels_collection.find({}, {'_id': 0}))
    return jsonify(hotels)

@app.route('/<int:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = hotels_collection.find_one({"id": hotel_id}, {'_id': 0})
    if hotel:
        return jsonify(hotel)
    return jsonify({"message": "Hotel not found"}), 404

if __name__ == '__main__':
    print("Hotel Service running on port 5003")
    app.run(port=5003, debug=True)
