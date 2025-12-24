# 🍽️ Baratie Food Ordering System

A simplified, monolithic food ordering system with a single backend API and frontend interface.

## 📋 Architecture

This application uses a **simple 2-tier architecture**:

```
┌─────────────────┐
│    Frontend     │  (Port 5001)
│   Flask + HTML  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend API    │  (Port 5000)
│  Flask + MongoDB│
└─────────────────┘
```

### Components

1. **Backend (`/backend`)**: Single Flask API server handling:
   - User authentication & registration
   - Admin operations
   - Hotel/restaurant management
   - Order processing
   - Payment handling
   - Email notifications

2. **Frontend (`/frontend`)**: Flask web application serving HTML templates

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- Gmail account for email notifications (optional)

### Local Development

1. **Clone and navigate to the project**:
   ```bash
   cd Food_Ordering
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file (or use `.env.example` as template):
   ```env
   MONGO_URI=your_mongodb_connection_string
   ADMIN_USER=admin
   ADMIN_PASS=admin123
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```

4. **Run the application**:
   ```bash
   python run_app.py
   ```

5. **Access the application**:
   - Frontend: http://localhost:5001
   - Backend API: http://localhost:5000
   - Admin Panel: http://localhost:5001/admin

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access**:
   - Frontend: http://localhost:5001
   - Backend: http://localhost:5000

## 📁 Project Structure

```
Food_Ordering/
├── backend/
│   └── app.py              # Single backend API server
├── frontend/
│   ├── app.py              # Frontend Flask app
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── Dockerfile              # Multi-service Docker image
├── docker-compose.yml      # Docker orchestration
├── run_app.py              # Local development launcher
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | (required) |
| `ADMIN_USER` | Admin username | `admin` |
| `ADMIN_PASS` | Admin password | `admin123` |
| `SENDER_EMAIL` | Gmail for notifications | (optional) |
| `SENDER_PASSWORD` | Gmail app password | (optional) |
| `PORT` | Server port | `5000` (backend), `5001` (frontend) |

### MongoDB Collections

The application uses the following collections:
- `users_service_collection` - User accounts
- `hotels_service_collection` - Restaurants and menus
- `orders_service_collection` - Order history
- `payments_service_collection` - Payment records

## 🎯 Features

### User Features
- ✅ User registration and login
- ✅ Browse restaurants and menus
- ✅ Add items to cart
- ✅ Multiple payment methods (GPay, PhonePe, Card)
- ✅ Email order confirmation
- ✅ Delivery tracking

### Admin Features
- ✅ Admin authentication
- ✅ Add new restaurants
- ✅ Manage menu items
- ✅ Assign delivery personnel
- ✅ View all restaurants

## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/user/<username>` - Get user details

### Admin
- `POST /admin/login` - Admin login
- `POST /admin/add_hotel` - Add restaurant
- `POST /admin/add_item` - Add menu item
- `POST /admin/add_delivery_person` - Add delivery person

### Hotels
- `GET /hotel/list` - List all hotels
- `GET /hotel/<id>` - Get hotel details

### Orders
- `POST /order/create` - Create new order

### Health
- `GET /health` - Health check endpoint

## 🐳 Deployment

### Render.com

1. Create two Web Services:
   - **Backend**: 
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app`
   - **Frontend**:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT frontend.app:app`
     - Environment: `GATEWAY_URL=<backend-url>`

2. Set environment variables in Render dashboard

### Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Stop
docker-compose down
```

## 🛠️ Development

### Running Individual Services

**Backend only**:
```bash
cd backend
python app.py
```

**Frontend only**:
```bash
cd frontend
python app.py
```

### Testing

Test the backend API:
```bash
curl http://localhost:5000/health
```

## 📝 Design Patterns Used

1. **Strategy Pattern** - Payment processing (GPay, PhonePe, Card)
2. **Builder Pattern** - Bill generation
3. **MVC Pattern** - Frontend structure

## 🔒 Security Notes

- Change default admin credentials in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Use strong MongoDB passwords
- Use Gmail App Passwords (not account password)

## 📧 Email Configuration

To enable email notifications:
1. Enable 2-Factor Authentication on Gmail
2. Generate an App Password
3. Set `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 👥 Authors

- Deavanathan S

## 🆘 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for food lovers**
