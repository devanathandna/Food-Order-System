# Complete Render Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas database created and accessible
- [ ] Gmail App Password generated (for email notifications)
- [ ] Render account created

---

## 📦 Service 1: Core Service

### Basic Settings
- **Service Name**: `baratie-core`
- **Environment**: `Docker`
- **Region**: Choose closest to you
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave blank
- **Dockerfile Path**: `Dockerfile`

### Environment Variables (Click "Add Environment Variable" for each)
```
SERVICE_NAME = core
MONGO_URI = mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain
ADMIN_USER = admin
ADMIN_PASS = admin123
```

### After Deployment
- [ ] Service deployed successfully
- [ ] Copy the service URL: `https://baratie-core.onrender.com`
- [ ] Save this URL - you'll need it for API Gateway

---

## 📦 Service 2: Transaction Service

### Basic Settings
- **Service Name**: `baratie-transaction`
- **Environment**: `Docker`
- **Region**: Same as Core Service
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Dockerfile Path**: `Dockerfile`

### Environment Variables
```
SERVICE_NAME = transaction
MONGO_URI = mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain
SENDER_EMAIL = bb1.deavanathan.s@gmail.com
SENDER_PASSWORD = ipwm okbq ryso xyjc
```

⚠️ **IMPORTANT**: Replace with YOUR email credentials!

### After Deployment
- [ ] Service deployed successfully
- [ ] Copy the service URL: `https://baratie-transaction.onrender.com`
- [ ] Save this URL - you'll need it for API Gateway

---

## 📦 Service 3: API Gateway

⚠️ **Deploy this AFTER Core and Transaction services are running!**

### Basic Settings
- **Service Name**: `baratie-gateway`
- **Environment**: `Docker`
- **Region**: Same as other services
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Dockerfile Path**: `Dockerfile`

### Environment Variables
```
SERVICE_NAME = gateway
CORE_SERVICE_URL = https://baratie-core.onrender.com
TRANS_SERVICE_URLS = https://baratie-transaction.onrender.com
```

⚠️ **Replace the URLs above with YOUR actual Render URLs from Step 1 & 2!**

### After Deployment
- [ ] Service deployed successfully
- [ ] Copy the service URL: `https://baratie-gateway.onrender.com`
- [ ] Save this URL - you'll need it for Frontend

---

## 📦 Service 4: Frontend

⚠️ **Deploy this LAST, after API Gateway is running!**

### Basic Settings
- **Service Name**: `baratie-frontend`
- **Environment**: `Docker`
- **Region**: Same as other services
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Dockerfile Path**: `Dockerfile`

### Environment Variables
```
SERVICE_NAME = frontend
GATEWAY_URL = https://baratie-gateway.onrender.com
```

⚠️ **Replace the URL above with YOUR actual Gateway URL from Step 3!**

### After Deployment
- [ ] Service deployed successfully
- [ ] Copy the service URL: `https://baratie-frontend.onrender.com`
- [ ] This is your main application URL!

---

## 🎯 Final Steps

### Test Your Application

1. **Access Frontend**
   - Visit: `https://baratie-frontend.onrender.com`
   - You should see the login/register page

2. **Test User Flow**
   - [ ] Register a new user
   - [ ] Login
   - [ ] Browse restaurants
   - [ ] Add items to cart
   - [ ] Place an order

3. **Test Admin Panel**
   - Visit: `https://baratie-frontend.onrender.com/admin`
   - [ ] Login with admin credentials
   - [ ] Add a restaurant
   - [ ] Add menu items
   - [ ] Add delivery person

### Troubleshooting

If something doesn't work:

1. **Check Service Status**
   - All 4 services should show "Live" status
   - If any show "Failed", check the logs

2. **Check Logs**
   - Go to each service → Logs tab
   - Look for error messages

3. **Common Issues**:

   **"SERVICE_NAME not set"**
   - Go to Environment tab
   - Verify `SERVICE_NAME` is set correctly
   - Check spelling (lowercase!)

   **"Service Unavailable" / 502 errors**
   - Backend services might not be running
   - Check Core and Transaction services are "Live"
   - Verify URLs in environment variables are correct

   **Database connection errors**
   - Check `MONGO_URI` is correct
   - Verify MongoDB Atlas allows connections from `0.0.0.0/0`
   - Check database user has read/write permissions

   **Email not sending**
   - Verify `SENDER_EMAIL` and `SENDER_PASSWORD`
   - Use Gmail App Password (not regular password)
   - Check Gmail account has 2FA enabled

---

## 📊 Your Service URLs Summary

After deployment, you'll have:

```
Frontend:     https://baratie-frontend.onrender.com
API Gateway:  https://baratie-gateway.onrender.com
Core Service: https://baratie-core.onrender.com
Transaction:  https://baratie-transaction.onrender.com
```

**Main URL to share**: `https://baratie-frontend.onrender.com`

---

## 🔒 Security Recommendations

Before going live:

- [ ] Change `ADMIN_PASS` from default `admin123`
- [ ] Use your own MongoDB database (not the example one)
- [ ] Use your own email credentials
- [ ] Enable MongoDB IP whitelist (if needed)
- [ ] Review all environment variables

---

## 💰 Cost Information

**Free Tier**:
- 4 services × 750 hours/month = 3000 hours total
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds

**Paid Tier** ($7/service/month):
- No cold starts
- Always-on
- Better performance
- Total: $28/month for all 4 services

---

## 🎉 Deployment Complete!

Once all 4 services show "Live" status and you can access the frontend, you're done!

**Share your app**: `https://baratie-frontend.onrender.com`

---

## 📞 Need Help?

1. Check service logs in Render dashboard
2. Verify all environment variables are set
3. Ensure all services are "Live"
4. Review this checklist again

**Common mistake**: Forgetting to update URLs in environment variables after deployment!
