# Render Deployment Guide (Docker)

## 🐳 Single Dockerfile Deployment

This project uses a **single Dockerfile** that can run any of the 4 services based on the `SERVICE_NAME` environment variable.

## 📋 Render Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Docker support"
git push origin main
```

### Step 2: Create Web Services on Render

Create **4 separate Web Services** on Render, one for each microservice:

#### Service 1: API Gateway
- **Name**: `baratie-gateway`
- **Environment**: `Docker`
- **Dockerfile Path**: `Dockerfile`
- **Docker Command**: (leave blank, uses Dockerfile CMD)

**Environment Variables**:
```
SERVICE_NAME=gateway
CORE_SERVICE_URL=https://baratie-core.onrender.com
TRANS_SERVICE_URLS=https://baratie-transaction.onrender.com
```

#### Service 2: Frontend
- **Name**: `baratie-frontend`
- **Environment**: `Docker`
- **Dockerfile Path**: `Dockerfile`

**Environment Variables**:
```
SERVICE_NAME=frontend
GATEWAY_URL=https://baratie-gateway.onrender.com
```

#### Service 3: Core Service
- **Name**: `baratie-core`
- **Environment**: `Docker`
- **Dockerfile Path**: `Dockerfile`

**Environment Variables**:
```
SERVICE_NAME=core
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=ClusterMain
ADMIN_USER=admin
ADMIN_PASS=your-secure-password
```

#### Service 4: Transaction Service
- **Name**: `baratie-transaction`
- **Environment**: `Docker`
- **Dockerfile Path**: `Dockerfile`

**Environment Variables**:
```
SERVICE_NAME=transaction
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=ClusterMain
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

### Step 3: Update Service URLs

After all services are deployed, **update the environment variables** with actual Render URLs:

1. In **API Gateway**:
   - `CORE_SERVICE_URL` → `https://baratie-core.onrender.com`
   - `TRANS_SERVICE_URLS` → `https://baratie-transaction.onrender.com`

2. In **Frontend**:
   - `GATEWAY_URL` → `https://baratie-gateway.onrender.com`

### Step 4: Access Your Application

- **Frontend**: `https://baratie-frontend.onrender.com`
- **Admin Panel**: `https://baratie-frontend.onrender.com/admin`

## 🏠 Local Development with Docker

### Using Docker Compose (Recommended)
```bash
# Create .env file
cp .env.docker .env
# Edit .env with your credentials

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker CLI
```bash
# Build image
docker build -t baratie .

# Run Gateway
docker run -d -p 5000:5000 \
  -e SERVICE_NAME=gateway \
  -e CORE_SERVICE_URL=http://localhost:5002 \
  -e TRANS_SERVICE_URLS=http://localhost:5003 \
  baratie

# Run Frontend
docker run -d -p 5001:5001 \
  -e SERVICE_NAME=frontend \
  -e GATEWAY_URL=http://localhost:5000 \
  baratie

# Run Core Service
docker run -d -p 5002:5002 \
  -e SERVICE_NAME=core \
  -e MONGO_URI="your-mongo-uri" \
  baratie

# Run Transaction Service
docker run -d -p 5003:5003 \
  -e SERVICE_NAME=transaction \
  -e MONGO_URI="your-mongo-uri" \
  -e SENDER_EMAIL="your-email" \
  -e SENDER_PASSWORD="your-password" \
  baratie
```

## 🔑 Environment Variables Reference

### All Services
- `SERVICE_NAME` - **Required**: `gateway`, `frontend`, `core`, or `transaction`
- `PORT` - Auto-set by Render (default: varies by service)

### Gateway Service
- `CORE_SERVICE_URL` - Core service URL
- `TRANS_SERVICE_URLS` - Transaction service URL(s)

### Frontend Service
- `GATEWAY_URL` - API Gateway URL

### Core Service
- `MONGO_URI` - MongoDB connection string
- `ADMIN_USER` - Admin username
- `ADMIN_PASS` - Admin password

### Transaction Service
- `MONGO_URI` - MongoDB connection string
- `SENDER_EMAIL` - Gmail for notifications
- `SENDER_PASSWORD` - Gmail app password

## 🛠️ Dockerfile Explanation

The single Dockerfile uses a conditional CMD:

```dockerfile
CMD if [ "$SERVICE_NAME" = "gateway" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} api_gateway.app:app; \
    elif [ "$SERVICE_NAME" = "frontend" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} frontend.app:app; \
    # ... etc
```

This allows one Dockerfile to serve all microservices!

## 🐛 Troubleshooting

### Service Won't Start
- Check `SERVICE_NAME` is set correctly
- Verify all required environment variables are set
- Check Render logs for errors

### Wrong Service Running
- Ensure `SERVICE_NAME` matches: `gateway`, `frontend`, `core`, or `transaction`
- Case-sensitive!

### Services Can't Communicate
- Use full Render URLs (not localhost)
- Ensure all services are deployed and running
- Check environment variable URLs are correct

## 💡 Advantages of Single Dockerfile

✅ **Simpler maintenance** - One file to update  
✅ **Consistent builds** - All services use same base  
✅ **Smaller repo** - Less duplication  
✅ **Easier CI/CD** - Single build process  
✅ **Render-friendly** - Easy to configure  

## 📞 Support

- Check Render logs: Dashboard → Service → Logs
- Verify environment variables: Dashboard → Service → Environment
- Review [Render Docker Docs](https://render.com/docs/docker)

---

**Ready to deploy!** 🚀
