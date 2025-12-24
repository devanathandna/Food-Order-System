# 🚀 Render Deployment Guide - Step by Step

## 📋 Prerequisites
- GitHub account
- Render.com account (free tier works!)
- MongoDB Atlas account with connection string

---

## 🎯 Deployment Steps

### Step 1: Deploy Backend First

1. **Go to Render Dashboard**: https://dashboard.render.com/

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Backend Service**:
   ```
   Name: baratie-backend (or any name you prefer)
   Region: Choose closest to you
   Branch: main (or your branch name)
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
   ```

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"
   
   ```
   MONGO_URI = mongodb+srv://username:password@cluster.mongodb.net/...
   ADMIN_USER = admin
   ADMIN_PASS = admin123
   SENDER_EMAIL = your_email@gmail.com
   SENDER_PASSWORD = your_gmail_app_password
   ```

5. **Create Web Service** (Click the button)

6. **Wait for Deployment** (2-5 minutes)

7. **Copy Your Backend URL**:
   - Once deployed, you'll see a URL like: `https://baratie-backend-xyz.onrender.com`
   - **COPY THIS URL** - you'll need it for the frontend!

8. **Test Backend**:
   - Visit: `https://your-backend-url.onrender.com/health`
   - You should see: `{"status": "healthy", "service": "Baratie Backend"}`

---

### Step 2: Update Frontend with Backend URL

1. **Open `frontend/app.py`** in your code editor

2. **Find line 11** (the one with the arrow ⬅️):
   ```python
   GATEWAY_URL = 'https://YOUR-BACKEND-APP-NAME.onrender.com'  # ⬅️ REPLACE THIS!
   ```

3. **Replace with your actual backend URL**:
   ```python
   GATEWAY_URL = 'https://baratie-backend-xyz.onrender.com'
   ```
   *(Use the URL you copied from Step 1.7)*

4. **Save the file**

5. **Commit and push to GitHub**:
   ```bash
   git add frontend/app.py
   git commit -m "Updated backend URL for Render deployment"
   git push
   ```

---

### Step 3: Deploy Frontend

1. **Go to Render Dashboard**: https://dashboard.render.com/

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (same repo)

3. **Configure Frontend Service**:
   ```
   Name: baratie-frontend (or any name you prefer)
   Region: Same as backend
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT frontend.app:app
   ```

4. **No Environment Variables Needed** (since you hardcoded the URL!)

5. **Create Web Service**

6. **Wait for Deployment** (2-5 minutes)

7. **Get Your Frontend URL**:
   - You'll see a URL like: `https://baratie-frontend-xyz.onrender.com`

---

### Step 4: Test Your Application

1. **Visit your frontend URL**: `https://baratie-frontend-xyz.onrender.com`

2. **Test User Flow**:
   - Register a new account
   - Login
   - Browse restaurants (if any exist)

3. **Test Admin Flow**:
   - Go to: `https://baratie-frontend-xyz.onrender.com/admin`
   - Login with: `admin` / `admin123`
   - Add a restaurant
   - Add menu items
   - Add delivery person

4. **Test Order Flow**:
   - Logout from admin
   - Login as user
   - Browse restaurants
   - Add items to cart
   - Place order

---

## 🎨 Visual Deployment Flow

```
┌─────────────────────────────────────────────────┐
│  Step 1: Deploy Backend to Render              │
│  ✅ Get Backend URL                             │
│  Example: https://baratie-backend.onrender.com │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Step 2: Update frontend/app.py                │
│  ✅ Hardcode GATEWAY_URL with backend URL       │
│  ✅ Commit and push to GitHub                   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Step 3: Deploy Frontend to Render             │
│  ✅ Frontend will use hardcoded backend URL     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Step 4: Test Everything                       │
│  ✅ User registration/login                     │
│  ✅ Admin operations                            │
│  ✅ Order placement                             │
└─────────────────────────────────────────────────┘
```

---

## 📝 Quick Reference

### Backend Configuration
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

### Frontend Configuration
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT frontend.app:app
```

### Where to Hardcode Backend URL
**File**: `frontend/app.py`  
**Line**: ~11  
**Change**: 
```python
GATEWAY_URL = 'https://your-actual-backend-url.onrender.com'
```

---

## ⚠️ Important Notes

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - Upgrade to paid plan for always-on services

2. **MongoDB Atlas**:
   - Make sure your IP is whitelisted (or allow all: `0.0.0.0/0`)
   - Use the connection string with your actual credentials

3. **Email Notifications**:
   - Use Gmail App Password (not regular password)
   - Enable 2FA on Gmail first

4. **HTTPS**:
   - Render automatically provides HTTPS
   - No additional configuration needed

---

## 🔧 Troubleshooting

### Backend Not Starting
- Check logs in Render dashboard
- Verify `MONGO_URI` is correct
- Ensure `requirements.txt` includes all dependencies

### Frontend Can't Connect to Backend
- Verify you hardcoded the correct backend URL in `frontend/app.py`
- Check backend is running (visit `/health` endpoint)
- Ensure backend URL uses `https://` not `http://`

### 502 Bad Gateway
- Backend service is spinning up (wait 30-60 seconds)
- Check backend logs for errors

### MongoDB Connection Error
- Verify MongoDB Atlas IP whitelist
- Check connection string format
- Ensure database user has correct permissions

---

## 🎉 Success Checklist

- [ ] Backend deployed and accessible
- [ ] Backend `/health` endpoint returns healthy status
- [ ] Frontend `app.py` updated with backend URL
- [ ] Changes committed and pushed to GitHub
- [ ] Frontend deployed and accessible
- [ ] User registration works
- [ ] User login works
- [ ] Admin login works
- [ ] Can add restaurants
- [ ] Can place orders

---

## 📞 Need Help?

If you encounter issues:
1. Check Render logs (click on your service → "Logs" tab)
2. Test backend endpoints directly with browser or Postman
3. Verify environment variables are set correctly
4. Check MongoDB Atlas connection

---

**Your Render URLs will look like**:
- Backend: `https://baratie-backend-xyz.onrender.com`
- Frontend: `https://baratie-frontend-xyz.onrender.com`

**Remember**: Replace `YOUR-BACKEND-APP-NAME.onrender.com` in `frontend/app.py` with your actual backend URL!

Good luck! 🚀
