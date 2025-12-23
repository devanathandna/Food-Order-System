# Quick Start Guide

## 🚀 Choose Your Deployment Method

### Option 1: Docker (Recommended)
```bash
# 1. Create environment file
cp .env.docker .env

# 2. Edit .env with your MongoDB URI and credentials
notepad .env  # Windows
nano .env     # Linux/Mac

# 3. Start all services
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:5001
# Admin: http://localhost:5001/admin
```

### Option 2: Python (Local Development)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run all services
python run_services.py

# 3. Access application
# Frontend: http://localhost:5001
```

### Option 3: Deploy to Render
See **RENDER_DEPLOYMENT.md** for detailed instructions.

## 📝 Environment Variables Needed

Create a `.env` file with:
```env
MONGO_URI=your-mongodb-uri
ADMIN_USER=admin
ADMIN_PASS=your-password
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

## 📚 Documentation

- **RENDER_DEPLOYMENT.md** - Deploy to Render with Docker
- **DOCKER_DEPLOYMENT.md** - Advanced Docker usage
- **README.md** - Full project documentation
- **CHANGES.md** - What changed for deployment

## 🔧 Default Ports

- Frontend: 5001
- API Gateway: 5000
- Core Service: 5002
- Transaction Service: 5003

## ⚠️ Important Notes

1. **MongoDB Required**: You need a MongoDB database (Atlas recommended)
2. **Gmail App Password**: For email notifications, use App Password not regular password
3. **Environment Variables**: Never commit `.env` to Git

## 🆘 Troubleshooting

**Services won't start?**
- Check `.env` file exists and has correct values
- Verify MongoDB URI is correct
- Ensure ports 5000-5003 are not in use

**Docker issues?**
- Run `docker-compose down -v` to clean up
- Check Docker Desktop is running
- View logs: `docker-compose logs -f`

---

**Need help?** Check the detailed guides in the documentation files above.
