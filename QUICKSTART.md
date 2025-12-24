# 🚀 Quick Start Guide - Baratie Food Ordering System

## ⚡ 3-Minute Setup

### Option 1: Local Development (Recommended for Testing)

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your MongoDB URI** (edit `.env` or set environment variable):
   ```bash
   # Windows PowerShell
   $env:MONGO_URI="your_mongodb_connection_string"
   
   # Linux/Mac
   export MONGO_URI="your_mongodb_connection_string"
   ```

3. **Run the application**:
   ```bash
   python run_app.py
   ```

4. **Open your browser**:
   - 🌐 Frontend: http://localhost:5001
   - 🔧 Backend API: http://localhost:5000
   - 👨‍💼 Admin Panel: http://localhost:5001/admin

### Option 2: Docker (Recommended for Production)

1. **Create `.env` file** with your MongoDB URI:
   ```env
   MONGO_URI=your_mongodb_connection_string
   ADMIN_USER=admin
   ADMIN_PASS=admin123
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:5001
   - Backend: http://localhost:5000

## 📝 Default Credentials

### Admin Login
- **URL**: http://localhost:5001/admin
- **Username**: `admin`
- **Password**: `admin123`

### User Account
- Register a new account at: http://localhost:5001/register

## 🎯 First Steps

1. **Login as Admin** → Add a restaurant
2. **Add menu items** to the restaurant
3. **Add delivery person** (optional)
4. **Logout** and register as a user
5. **Browse restaurants** → Add items to cart → Place order

## 🛑 Stopping the Application

### Local Development
- Press `Ctrl+C` in the terminal

### Docker
```bash
docker-compose down
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### MongoDB Connection Error
- Verify your `MONGO_URI` is correct
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure network connectivity

### Email Notifications Not Working
- Email is **optional** - orders will still work
- Use Gmail App Password (not regular password)
- Enable 2FA on Gmail first

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for production deployment
- See [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md) for configuration options

---

**Need help?** Open an issue on GitHub or check the documentation!
