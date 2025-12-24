from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Hardcoded Backend URL for Render Deployment
# Replace this with your actual Render backend URL after deployment
# Example: GATEWAY_URL = 'https://baratie-backend.onrender.com'
GATEWAY_URL = 'https://baratie-food-ordering.onrender.com'  # ⬅️ REPLACE THIS!

@app.route('/')
def home():
    if 'token' in session:
        try:
            response = requests.get(f"{GATEWAY_URL}/hotel/list")
            hotels = response.json() if response.status_code == 200 else []
        except:
            hotels = []
        return render_template('dashboard.html', hotels=hotels)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            # Updated path: /auth/login
            response = requests.post(f"{GATEWAY_URL}/auth/login", json={"username": username, "password": password})
            if response.status_code == 200:
                session['token'] = response.json().get('token')
                session['username'] = username
                return redirect(url_for('home'))
            error = "Invalid Credentials"
        except:
            error = "Service Unavailable"
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            "username": request.form['username'],
            "password": request.form['password'],
            "name": request.form['name'],
            "phone": request.form['phone'],
            "email": request.form['email'],
            "address": request.form['address'],
            "city": request.form['city']
        }
        try:
            # Updated path: /auth/register
            response = requests.post(f"{GATEWAY_URL}/auth/register", json=data)
            if response.status_code == 201:
                return redirect(url_for('login'))
            error = response.json().get('message', 'Registration Failed')
        except:
            error = "Service Unavailable"
        return render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/order/<int:hotel_id>', methods=['GET'])
def order_page(hotel_id):
    if 'token' not in session: return redirect(url_for('login'))
    try:
        response = requests.get(f"{GATEWAY_URL}/hotel/{hotel_id}")
        hotel = response.json()
        return render_template('order.html', hotel=hotel)
    except:
        return "Error loading hotel", 500

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'token' not in session: return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    hotel_name = request.form.get('hotel_name')
    hotel_id = request.form.get('hotel_id')
    
    # Simple parse
    for key, value in request.form.items():
        if key.startswith('qty_') and int(value) > 0:
            item_name = key.replace('qty_', '')
            price = float(request.form.get(f'price_{item_name}'))
            qty = int(value)
            
            # Add to cart
            cart.append({
                "hotel": hotel_name,
                "hotel_id": hotel_id,
                "name": item_name,
                "price": price,
                "quantity": qty
            })
            
    session['cart'] = cart
    return redirect(url_for('checkout'))

@app.route('/checkout')
def checkout():
    if 'token' not in session: return redirect(url_for('login'))
    cart = session.get('cart', [])
    if not cart: return "Cart is empty. <a href='/'>Go back</a>"
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    
    # Get User City for Delivery Charge
    username = session.get('username')
    try:
        user_info = requests.get(f"{GATEWAY_URL}/auth/user/{username}").json()
        user_city = user_info.get('city', 'Unknown')
    except:
        user_city = 'Unknown'
    
    # Get Delivery Charge
    hotel_id = cart[0].get('hotel_id')
    delivery_charge = 5.0 # Default
    delivery_person_name = "Standard"

    if hotel_id:
        try:
            hotel_resp = requests.get(f"{GATEWAY_URL}/hotel/{hotel_id}").json()
            if 'delivery_person' in hotel_resp:
                delivery_charge = hotel_resp['delivery_person'].get('charge', 0)
                delivery_person_name = hotel_resp['delivery_person'].get('name', 'Standard')
        except:
            pass
        
    total = subtotal + delivery_charge
    
    return render_template('checkout.html', 
                           cart_items=cart, 
                           subtotal=subtotal, 
                           delivery_charge=delivery_charge, 
                           total=total,
                           city=user_city,
                           delivery_person_name=delivery_person_name)

@app.route('/place_order_final', methods=['POST'])
def place_order_final():
    if 'token' not in session: return redirect(url_for('login'))
    
    payment_method = request.form['payment_method']
    delivery_charge = float(request.form['delivery_charge'])
    cart = session.get('cart', [])
    username = session.get('username')
    
    # Get user full details
    try:
        user_info = requests.get(f"{GATEWAY_URL}/auth/user/{username}").json()
    except:
        user_info = {}
    
    payload = {
        "user_details": {
            "username": username,
            "email": user_info.get('email'),
            "phone": user_info.get('phone')
        },
        "items": cart,
        "restaurant_name": cart[0]['hotel'] if cart else "Multiple",
        "delivery_charge": delivery_charge,
        "payment_method": payment_method
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/order/create", json=payload)
        if response.status_code == 201:
            session.pop('cart', None) # Clear cart
            return f"<h1>Order Successful!</h1><pre>{response.json().get('bill')}</pre><a href='/'>Home</a>"
        return f"Order Failed: {response.text}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Admin Routes ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f"{GATEWAY_URL}/admin/login", json={"username": username, "password": password})
            if response.status_code == 200:
                session['admin_token'] = response.json().get('token')
                return redirect(url_for('admin_dashboard'))
            error = "Invalid Admin Credentials"
        except:
            error = "Admin Service Unavailable"
        return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    # Fetch Data to show
    try:
        hotels = requests.get(f"{GATEWAY_URL}/hotel/list").json()
    except:
        hotels = []
    return render_template('admin_dashboard.html', hotels=hotels)

# --- New Portal Routes ---
@app.route('/admin/portal/add_hotel')
def view_add_hotel():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    return render_template('admin_add_hotel.html')

@app.route('/admin/portal/add_food')
def view_add_food():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    try: hotels = requests.get(f"{GATEWAY_URL}/hotel/list").json()
    except: hotels = []
    return render_template('admin_add_food.html', hotels=hotels)

@app.route('/admin/portal/add_delivery')
def view_add_delivery():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    try: hotels = requests.get(f"{GATEWAY_URL}/hotel/list").json()
    except: hotels = []
    return render_template('admin_add_delivery.html', hotels=hotels)

@app.route('/admin/add_hotel', methods=['POST'])
def admin_add_hotel():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    menu = []
    food_name = request.form.get('food_name')
    if food_name:
        try:
            food_price = float(request.form.get('food_price', 0))
        except ValueError:
            food_price = 0.0
        menu.append({
            "id": 101, "name": food_name, "price": food_price
        })
        
    data = {
        "name": request.form['name'],
        "address": request.form['address'],
        "city": request.form['city'],
        "menu": menu
    }
    
    try:
        resp = requests.post(f"{GATEWAY_URL}/admin/add_hotel", json=data)
        if resp.status_code != 200 and resp.status_code != 201:
            print(f"Error creating hotel: {resp.text}")
    except Exception as e:
        print(f"Exception connecting to Admin Service: {e}")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_item', methods=['POST'])
def admin_add_item():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    try:
        data = {
            "hotel_id": int(request.form['hotel_id']),
            "name": request.form['name'],
            "price": float(request.form['price'])
        }
        requests.post(f"{GATEWAY_URL}/admin/add_item", json=data)
    except: pass
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_price', methods=['POST'])
def admin_update_price():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    try:
        data = {
            "hotel_id": int(request.form['hotel_id']),
            "item_id": int(request.form['item_id']),
            "price": float(request.form['price'])
        }
        requests.put(f"{GATEWAY_URL}/admin/update_price", json=data)
    except: pass
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_delivery_person', methods=['POST'])
def admin_add_delivery_person():
    if 'admin_token' not in session: return redirect(url_for('admin_login'))
    data = {
        "hotel_id": int(request.form['hotel_id']),
        "name": request.form['name'],
        "phone": request.form['phone'],
        "city": request.form['city'],
        "charge": float(request.form['charge'])
    }
    requests.post(f"{GATEWAY_URL}/admin/add_delivery_person", json=data)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Render provides PORT environment variable
    port = int(os.environ.get('PORT', 5001))
    print(f"Frontend running on port {port}")
    # host='0.0.0.0' is required for Render to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False)
