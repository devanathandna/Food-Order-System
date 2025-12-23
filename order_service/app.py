from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
import time
import datetime

app = Flask(__name__)

# MongoDB Config
MONGO_URI = "mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain"
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
orders_collection = db.orders_service_collection

GATEWAY_URL = "http://localhost:5000"

# --- Builder Pattern for Bill ---
class BillBuilder:
    def __init__(self):
        self.bill_data = {}
        self.output = ""

    def set_user_details(self, username, email, phone):
        self.bill_data['username'] = username
        self.bill_data['email'] = email
        self.bill_data['phone'] = phone
        self.output += f"Customer: {username}\nEmail: {email}\nPhone: {phone}\n"
        return self

    def set_order_meta(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bill_data['timestamp'] = now
        self.output += f"Date: {now}\n"
        return self

    def set_restaurant(self, name):
        self.bill_data['restaurant'] = name
        self.output += f"Restaurant: {name}\n"
        self.output += "-" * 30 + "\n"
        return self

    def set_items(self, items):
        self.bill_data['items'] = items
        self.output += "Items:\n"
        for item in items:
            # item structure: {name, quantity, price}
            line_total = item['price'] * item['quantity']
            self.output += f"- {item['name']} x{item['quantity']} (${item['price']}) = ${line_total:.2f}\n"
        return self
    
    def set_delivery(self, charge):
        self.bill_data['delivery_charge'] = charge
        self.output += f"Delivery Charge: ${charge:.2f}\n"
        return self

    def set_total(self, total):
        self.bill_data['total_amount'] = total
        self.output += "-" * 30 + "\n"
        self.output += f"TOTAL: ${total:.2f}\n"
        return self

    def set_payment_method(self, method):
        self.bill_data['payment_method'] = method
        self.output += f"Payment Method: {method}\n"
        return self

    def build(self):
        return self.output

@app.route('/create', methods=['POST'])
def create_order():
    data = request.json
    
    # Context Data
    user_data = data.get('user_details', {}) # {username, email, phone}
    items = data.get('items', []) # List of {name, price, quantity}
    rest_name = data.get('restaurant_name')
    delivery_charge = float(data.get('delivery_charge', 0))
    payment_method = data.get('payment_method', 'card')
    
    # Calculate Total
    items_total = sum(item['price'] * item['quantity'] for item in items)
    final_total = items_total + delivery_charge
    
    # 1. Process Payment (Strategy via Payment Service)
    try:
        pay_resp = requests.post(f"{GATEWAY_URL}/payment/process", 
                                 json={"amount": final_total, "method": payment_method})
        if pay_resp.status_code != 200:
            return jsonify({"message": "Payment Failed"}), 400
    except:
        return jsonify({"message": "Payment Service Unavailable"}), 503

    # 2. Build Bill (Builder Pattern)
    builder = BillBuilder()
    bill_text = (builder
        .set_user_details(user_data.get('username'), user_data.get('email'), user_data.get('phone'))
        .set_order_meta()
        .set_restaurant(rest_name)
        .set_items(items)
        .set_delivery(delivery_charge)
        .set_total(final_total)
        .set_payment_method(payment_method)
        .build())
    
    # 3. Store Order
    order_doc = builder.bill_data
    order_doc['bill_text'] = bill_text
    order_id = int(time.time())
    order_doc['id'] = order_id
    orders_collection.insert_one(order_doc)
    
    # 4. Send Notification
    # Hardcoded recipient as per request "toaddr = "dnathan781@gmail.com"
    # But usually would be user's email.
    target_email = "dnathan781@gmail.com" 
    
    try:
        requests.post(f"{GATEWAY_URL}/notification/send_bill", 
                      json={"to_email": target_email, "bill_content": bill_text})
    except:
        print("Failed to send email")

    return jsonify({"message": "Order Placed", "order_id": order_id, "bill": bill_text}), 201

if __name__ == '__main__':
    print("Order Service running on port 5004")
    app.run(port=5004, debug=True)
