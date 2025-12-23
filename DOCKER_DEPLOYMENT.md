# Docker Deployment Guide

This guide covers deploying the Baratie Food Ordering System using Docker and Docker Compose.

## 🐳 Prerequisites

1. **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
2. **Docker Compose** (included with Docker Desktop)
3. **MongoDB Atlas** account (or local MongoDB)

## 🚀 Quick Start (Local Development)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Food_Ordering
```

### 2. Create Environment File
```bash
# Copy the template
cp .env.docker .env

# Edit .env with your actual credentials
# Use your favorite text editor
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 3. Build and Run
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Application
- **Frontend**: http://localhost:5001
- **Admin Panel**: http://localhost:5001/admin
- **API Gateway**: http://localhost:5000

### 5. Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📦 Individual Service Commands

### Build Individual Services
```bash
docker build -f Dockerfile.gateway -t baratie-gateway .
docker build -f Dockerfile.frontend -t baratie-frontend .
docker build -f Dockerfile.core -t baratie-core .
docker build -f Dockerfile.transaction -t baratie-transaction .
```

### Run Individual Services
```bash
# Core Service
docker run -d -p 5002:5002 \
  -e MONGO_URI="your-mongo-uri" \
  baratie-core

# Transaction Service
docker run -d -p 5003:5003 \
  -e MONGO_URI="your-mongo-uri" \
  -e SENDER_EMAIL="your-email" \
  -e SENDER_PASSWORD="your-password" \
  baratie-transaction

# API Gateway
docker run -d -p 5000:5000 \
  -e CORE_SERVICE_URL="http://core-service:5002" \
  -e TRANS_SERVICE_URLS="http://transaction-service:5003" \
  baratie-gateway

# Frontend
docker run -d -p 5001:5001 \
  -e GATEWAY_URL="http://api-gateway:5000" \
  baratie-frontend
```

## ☁️ Deploying to Render with Docker

### Option 1: Using Render's Native Docker Support

1. **Create a Web Service** on Render for each microservice

2. **Configure each service**:
   - **Environment**: Docker
   - **Dockerfile Path**: 
     - Gateway: `Dockerfile.gateway`
     - Frontend: `Dockerfile.frontend`
     - Core: `Dockerfile.core`
     - Transaction: `Dockerfile.transaction`

3. **Set Environment Variables** in Render dashboard (same as before)

4. **Deploy**: Render will automatically build and deploy from Dockerfile

### Option 2: Using Docker Hub

1. **Build and tag images**:
```bash
docker build -f Dockerfile.gateway -t yourusername/baratie-gateway:latest .
docker build -f Dockerfile.frontend -t yourusername/baratie-frontend:latest .
docker build -f Dockerfile.core -t yourusername/baratie-core:latest .
docker build -f Dockerfile.transaction -t yourusername/baratie-transaction:latest .
```

2. **Push to Docker Hub**:
```bash
docker login
docker push yourusername/baratie-gateway:latest
docker push yourusername/baratie-frontend:latest
docker push yourusername/baratie-core:latest
docker push yourusername/baratie-transaction:latest
```

3. **Deploy on Render**:
   - Select "Deploy an existing image from a registry"
   - Enter your Docker Hub image URL
   - Configure environment variables

## 🔧 Docker Compose Configuration

The `docker-compose.yml` file orchestrates all services:

```yaml
services:
  core-service:      # Port 5002
  transaction-service: # Port 5003
  api-gateway:       # Port 5000
  frontend:          # Port 5001
```

### Service Dependencies
```
Frontend → API Gateway → Core Service
                      → Transaction Service
```

### Networking
All services communicate via `baratie-network` bridge network.

## 🛠️ Useful Docker Commands

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f api-gateway
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart frontend
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build frontend
```

### Execute Commands in Container
```bash
# Open shell in container
docker-compose exec frontend /bin/bash

# Run Python command
docker-compose exec core-service python -c "print('Hello')"
```

### Clean Up
```bash
# Remove stopped containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a
```

## 📊 Environment Variables Reference

### Required for All Services
- `PORT` - Service port (auto-set by Render)

### Core Service
- `MONGO_URI` - MongoDB connection string
- `ADMIN_USER` - Admin username
- `ADMIN_PASS` - Admin password

### Transaction Service
- `MONGO_URI` - MongoDB connection string
- `SENDER_EMAIL` - Gmail address for notifications
- `SENDER_PASSWORD` - Gmail app password

### API Gateway
- `CORE_SERVICE_URL` - Core service URL
- `TRANS_SERVICE_URLS` - Transaction service URL(s)

### Frontend
- `GATEWAY_URL` - API Gateway URL

## 🔍 Troubleshooting

### Services Can't Connect
```bash
# Check network
docker network ls
docker network inspect food_ordering_baratie-network

# Check if services are running
docker-compose ps
```

### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Change port in docker-compose.yml
ports:
  - "5010:5001"  # Map to different host port
```

### Container Keeps Restarting
```bash
# Check logs
docker-compose logs frontend

# Check container status
docker-compose ps
```

### Database Connection Failed
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas network access (allow 0.0.0.0/0)
- Ensure database user has proper permissions

### Image Build Fails
```bash
# Clear Docker cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -f Dockerfile.gateway .
```

## 🎯 Production Best Practices

### 1. Use Multi-Stage Builds (Optional Optimization)
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "..."]
```

### 2. Health Checks
Add to docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 3. Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

### 4. Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 📈 Scaling with Docker

### Scale Transaction Service
```bash
# Run 3 instances
docker-compose up -d --scale transaction-service=3
```

### Load Balancing
For production, use:
- **Nginx** as reverse proxy
- **Traefik** for automatic service discovery
- **Kubernetes** for advanced orchestration

## 🔐 Security Checklist

- [ ] Use `.env` file (never commit to Git)
- [ ] Use Docker secrets for sensitive data
- [ ] Run containers as non-root user
- [ ] Keep base images updated
- [ ] Scan images for vulnerabilities (`docker scan`)
- [ ] Use specific image tags (not `latest`)

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Render Docker Deployment](https://render.com/docs/docker)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Your application is now containerized and ready for deployment!** 🐳🚀
