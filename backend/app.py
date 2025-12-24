from flask import Flask, request, jsonify
from pymongo import MongoClient
import abc
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ===========================
# CONFIGURATION
# ===========================

# MongoDB Config
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain')
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
users_collection = db.users_service_collection
hotels_collection = db.hotels_service_collection
orders_collection = db.orders_service_collection
payments_collection = db.payments_service_collection

# Admin Credentials
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')

# Email Configuration
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'bb1.deavanathan.s@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'ipwm okbq ryso xyjc')

# ===========================
# AUTHENTICATION ROUTES
# ===========================

@app.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users_collection.find_one({"username": username})
    if user and user['password'] == password:
        return jsonify({"token": f"fake-jwt-token-{username}", "message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
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
    """Get user details"""
    user = users_collection.find_one({"username": username}, {'_id': 0, 'password': 0})
    if user: 
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

# ===========================
# ADMIN ROUTES
# ===========================

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    data = request.json
    if data.get('username') == ADMIN_USER and data.get('password') == ADMIN_PASS:
        return jsonify({"token": "admin-secret-token", "message": "Admin logged in"}), 200
    return jsonify({"message": "Invalid Admin Credentials"}), 401

@app.route('/admin/add_hotel', methods=['POST'])
def add_hotel():
    """Add a new hotel/restaurant"""
    data = request.json
    if not data.get('name'): 
        return jsonify({"message": "Name required"}), 400
    
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
    """Add menu item to a hotel"""
    data = request.json
    hotel_id = data.get('hotel_id')
    
    # Generate Item ID
    item_id = int(time.time() * 1000) % 100000 
    
    new_item = {
        "id": item_id, 
        "name": data.get('name'), 
        "price": float(data.get('price'))
    }
    
    result = hotels_collection.update_one(
        {"id": int(hotel_id)},
        {"$push": {"menu": new_item}}
    )
    if result.modified_count:
        return jsonify({"message": "Item added", "item_id": item_id}), 200
    return jsonify({"message": "Hotel not found"}), 404

@app.route('/admin/add_delivery_person', methods=['POST'])
def add_delivery_person():
    """Add delivery person to a hotel"""
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

# ===========================
# HOTEL/RESTAURANT ROUTES
# ===========================

@app.route('/hotel/list', methods=['GET'])
def list_hotels():
    """List all hotels"""
    hotels = list(hotels_collection.find({}, {'_id': 0}))
    return jsonify(hotels)

@app.route('/hotel/<int:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    """Get specific hotel details"""
    hotel = hotels_collection.find_one({"id": hotel_id}, {'_id': 0})
    if hotel: 
        return jsonify(hotel)
    return jsonify({"message": "Hotel not found"}), 404

# ===========================
# PAYMENT STRATEGY PATTERN
# ===========================

class PaymentStrategy(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount):
        pass

class GPayStrategy(PaymentStrategy):
    def pay(self, amount): 
        return f"Paid ₹{amount:.2f} via Google Pay"

class PhonePeStrategy(PaymentStrategy):
    def pay(self, amount): 
        return f"Paid ₹{amount:.2f} via PhonePe"

class CardStrategy(PaymentStrategy):
    def pay(self, amount): 
        return f"Paid ₹{amount:.2f} via Credit/Debit Card"

class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def execute_payment(self, amount):
        return self._strategy.pay(amount)

def process_payment_logic(amount, method):
    """Process payment using strategy pattern"""
    strategy = None
    method = method.lower()
    if method == 'gpay': 
        strategy = GPayStrategy()
    elif method == 'phonepe': 
        strategy = PhonePeStrategy()
    else: 
        strategy = CardStrategy()
    
    context = PaymentContext(strategy)
    return context.execute_payment(amount)

# ===========================
# BILL BUILDER PATTERN
# ===========================

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
            line_total = item['price'] * item['quantity']
            self.output += f"- {item['name']} x{item['quantity']} (₹{item['price']}) = ₹{line_total:.2f}\n"
        return self
    
    def set_delivery(self, charge):
        self.bill_data['delivery_charge'] = charge
        self.output += f"Delivery Charge: ₹{charge:.2f}\n"
        return self

    def set_total(self, total):
        self.bill_data['total_amount'] = total
        self.output += "-" * 30 + "\n"
        self.output += f"TOTAL: ₹{total:.2f}\n"
        return self

    def set_payment_method(self, method):
        self.bill_data['payment_method'] = method
        self.output += f"Payment Method: {method}\n"
        return self

    def build(self):
        return self.output

# ===========================
# NOTIFICATION SERVICE
# ===========================

def send_email_logic(to_email, content):
    """Send email notification"""
    if not to_email: 
        return False
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = "Your Food Order Bill"
        msg.attach(MIMEText(content, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# ===========================
# ORDER ROUTES
# ===========================

@app.route('/order/create', methods=['POST'])
def create_order():
    """Create a new order with payment and notification"""
    data = request.json
    user_data = data.get('user_details', {})
    items = data.get('items', [])
    rest_name = data.get('restaurant_name')
    delivery_charge = float(data.get('delivery_charge', 0))
    payment_method = data.get('payment_method', 'card')
    
    items_total = sum(item['price'] * item['quantity'] for item in items)
    final_total = items_total + delivery_charge
    
    # 1. Process Payment
    pay_message = process_payment_logic(final_total, payment_method)
    
    # 2. Build Bill
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
    
    bill_text += f"\nValidation: {pay_message}"

    # 3. Store Order
    order_doc = builder.bill_data
    order_doc['id'] = int(time.time())
    order_doc['bill_text'] = bill_text
    orders_collection.insert_one(order_doc)
    
    # 4. Send Notification
    send_email_logic("dnathan781@gmail.com", bill_text)
    
    return jsonify({
        "message": "Order Placed", 
        "order_id": order_doc['id'], 
        "bill": bill_text
    }), 201

# ===========================
# HEALTH CHECK
# ===========================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Baratie Backend"}), 200

# ===========================
# MAIN
# ===========================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🍽️  Baratie Backend Server running on port {port}")
    print(f"📊 MongoDB: Connected")
    print(f"🔐 Admin User: {ADMIN_USER}")
    app.run(host='0.0.0.0', port=port, debug=False)
