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

# MongoDB Config - Use environment variable for security
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain')
client = MongoClient(MONGO_URI)
db = client.food_ordering_db
orders_collection = db.orders_service_collection
payments_collection = db.payments_service_collection

# --- PAYMENT STRATEGY ---
class PaymentStrategy(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount):
        pass

class GPayStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid ₹{amount:.2f} via Google Pay"

class PhonePeStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid ₹{amount:.2f} via PhonePe"

class CardStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid ₹{amount:.2f} via Credit/Debit Card"

class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    def execute_payment(self, amount):
        return self._strategy.pay(amount)

def process_payment_logic(amount, method):
    strategy = None
    method = method.lower()
    if method == 'gpay': strategy = GPayStrategy()
    elif method == 'phonepe': strategy = PhonePeStrategy()
    else: strategy = CardStrategy()
    
    context = PaymentContext(strategy)
    return context.execute_payment(amount)

# --- BILL BUILDER ---
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

# --- NOTIFICATION ---
# Use environment variables for email credentials (security best practice)
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'bb1.deavanathan.s@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'ipwm okbq ryso xyjc')
def send_email_logic(to_email, content):
    if not to_email: return False
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

# --- ROUTES ---

@app.route('/order/create', methods=['POST'])
def create_order():
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
    
    # 4. Notify
    send_email_logic("dnathan781@gmail.com", bill_text)
    
    return jsonify({"message": "Order Placed", "order_id": order_doc['id'], "bill": bill_text}), 201

if __name__ == '__main__':
    import sys
    # Render provides PORT environment variable, fallback to command line arg or default
    port = int(os.environ.get('PORT', 5003))
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    print(f"Transaction Service running on port {port}")
    # host='0.0.0.0' is required for Render to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False)
