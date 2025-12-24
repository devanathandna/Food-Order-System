# 🏗️ Architecture Overview - Baratie Food Ordering System

## 📊 System Architecture

### Simplified 2-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
│                    (Web Browser)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND SERVER                          │
│                    (Flask - Port 5001)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • User Interface (HTML/CSS/JS)                      │  │
│  │  • Session Management                                │  │
│  │  • Template Rendering                                │  │
│  │  • Request Routing                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API Calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API SERVER                       │
│                    (Flask - Port 5000)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication Module                               │  │
│  │  • User Login/Register                               │  │
│  │  • Admin Authentication                              │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Hotel Management Module                             │  │
│  │  • List Restaurants                                  │  │
│  │  • Get Restaurant Details                            │  │
│  │  • Menu Management                                   │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Admin Module                                        │  │
│  │  • Add Restaurants                                   │  │
│  │  • Add Menu Items                                    │  │
│  │  • Manage Delivery Personnel                        │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Order Processing Module                             │  │
│  │  • Create Orders                                     │  │
│  │  • Payment Processing (Strategy Pattern)            │  │
│  │  • Bill Generation (Builder Pattern)                │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Notification Module                                 │  │
│  │  • Email Notifications (SMTP)                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Database Queries
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                           │
│                    (MongoDB Atlas)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Collections:                                        │  │
│  │  • users_service_collection                          │  │
│  │  • hotels_service_collection                         │  │
│  │  • orders_service_collection                         │  │
│  │  • payments_service_collection                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow

### User Order Flow

```
1. User Login
   Browser → Frontend → Backend (/auth/login) → MongoDB
   
2. Browse Restaurants
   Browser → Frontend → Backend (/hotel/list) → MongoDB
   
3. View Menu
   Browser → Frontend → Backend (/hotel/{id}) → MongoDB
   
4. Add to Cart
   Browser → Frontend (Session Storage)
   
5. Checkout
   Browser → Frontend → Backend (/auth/user/{username}) → MongoDB
   Browser → Frontend → Backend (/hotel/{id}) → MongoDB
   
6. Place Order
   Browser → Frontend → Backend (/order/create) → 
   ├─ Payment Processing (Strategy Pattern)
   ├─ Bill Generation (Builder Pattern)
   ├─ Store in MongoDB
   └─ Send Email Notification
```

### Admin Flow

```
1. Admin Login
   Browser → Frontend → Backend (/admin/login) → Validate Credentials
   
2. Add Restaurant
   Browser → Frontend → Backend (/admin/add_hotel) → MongoDB
   
3. Add Menu Item
   Browser → Frontend → Backend (/admin/add_item) → MongoDB
   
4. Add Delivery Person
   Browser → Frontend → Backend (/admin/add_delivery_person) → MongoDB
```

## 🎨 Design Patterns

### 1. Strategy Pattern (Payment Processing)
```
PaymentContext
    ├─ GPayStrategy
    ├─ PhonePeStrategy
    └─ CardStrategy
```

**Purpose**: Allows dynamic selection of payment method at runtime

### 2. Builder Pattern (Bill Generation)
```
BillBuilder
    ├─ set_user_details()
    ├─ set_order_meta()
    ├─ set_restaurant()
    ├─ set_items()
    ├─ set_delivery()
    ├─ set_total()
    ├─ set_payment_method()
    └─ build()
```

**Purpose**: Constructs complex bill objects step-by-step

### 3. MVC Pattern (Frontend)
```
Model: Data from Backend API
View: HTML Templates
Controller: Flask Routes
```

## 📦 Component Breakdown

### Backend Server (`/backend/app.py`)
- **Lines of Code**: ~350
- **Endpoints**: 13
- **Dependencies**: Flask, PyMongo, smtplib
- **Responsibilities**:
  - API endpoint handling
  - Business logic
  - Database operations
  - Email notifications

### Frontend Server (`/frontend/app.py`)
- **Lines of Code**: ~300
- **Routes**: 15
- **Templates**: 8 HTML files
- **Responsibilities**:
  - UI rendering
  - Session management
  - API consumption
  - User interaction

## 🔐 Security Layers

```
┌─────────────────────────────────────┐
│  Environment Variables              │
│  • MongoDB credentials              │
│  • Admin credentials                │
│  • Email credentials                │
└─────────────────────────────────────┘
           ▼
┌─────────────────────────────────────┐
│  Session Management                 │
│  • User sessions                    │
│  • Admin sessions                   │
│  • Cart data                        │
└─────────────────────────────────────┘
           ▼
┌─────────────────────────────────────┐
│  Authentication                     │
│  • User login validation            │
│  • Admin authentication             │
│  • Token-based sessions             │
└─────────────────────────────────────┘
```

## 🚀 Deployment Architecture

### Local Development
```
┌─────────────────┐
│   run_app.py    │
│   (Launcher)    │
└────────┬────────┘
         │
         ├─────────────┐
         ▼             ▼
   ┌─────────┐   ┌─────────┐
   │ Backend │   │Frontend │
   │  :5000  │   │  :5001  │
   └─────────┘   └─────────┘
```

### Docker Deployment
```
┌──────────────────────────────────┐
│     docker-compose.yml           │
└────────┬─────────────────────────┘
         │
         ├─────────────┬────────────┐
         ▼             ▼            ▼
   ┌─────────┐   ┌─────────┐  ┌─────────┐
   │Container│   │Container│  │ Network │
   │ Backend │   │Frontend │  │  Bridge │
   │  :5000  │   │  :5001  │  └─────────┘
   └─────────┘   └─────────┘
```

### Production (Render.com)
```
┌─────────────────────────────────────┐
│         Render Platform             │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Web Service  │  │ Web Service  ││
│  │  (Backend)   │  │  (Frontend)  ││
│  │   HTTPS      │  │   HTTPS      ││
│  └──────────────┘  └──────────────┘│
└─────────────────────────────────────┘
           ▼
┌─────────────────────────────────────┐
│      MongoDB Atlas (Cloud)          │
└─────────────────────────────────────┘
```

## 📊 Data Flow

### Order Creation Sequence

```
1. Frontend receives order request
   ↓
2. Frontend calls Backend API (/order/create)
   ↓
3. Backend validates data
   ↓
4. Payment Strategy selected (GPay/PhonePe/Card)
   ↓
5. Payment processed
   ↓
6. Bill Builder creates formatted bill
   ↓
7. Order saved to MongoDB
   ↓
8. Email notification sent
   ↓
9. Response returned to Frontend
   ↓
10. User sees confirmation
```

## 🔧 Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Flask, Jinja2, HTML, CSS, JavaScript |
| Backend | Flask, Python 3.11 |
| Database | MongoDB Atlas |
| Email | SMTP (Gmail) |
| Deployment | Docker, Render.com |
| Web Server | Gunicorn |

## 📈 Scalability Considerations

### Current Architecture
- ✅ Simple and easy to maintain
- ✅ Fast development and deployment
- ✅ Low infrastructure cost
- ⚠️ Limited horizontal scaling

### Future Enhancements (if needed)
- Add Redis for session management
- Implement message queue (RabbitMQ/Kafka) for async tasks
- Split into microservices if traffic increases
- Add load balancer for multiple instances
- Implement caching layer

---

**This architecture prioritizes simplicity and maintainability while providing all essential features for a food ordering system.**
