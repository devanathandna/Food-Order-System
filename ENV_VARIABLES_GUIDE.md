# Environment Variables Configuration Guide

## 🔧 How to Set Environment Variables on Render

### Step-by-Step:

1. Go to Render Dashboard: https://dashboard.render.com
2. Click on your service (e.g., "baratie-core")
3. Click **"Environment"** in the left sidebar
4. Click **"Add Environment Variable"**
5. Enter Key and Value
6. Click **"Save Changes"**
7. Service will automatically redeploy

---

## 📋 Complete Configuration Reference

### Service 1: baratie-core

| Key | Value | Notes |
|-----|-------|-------|
| `SERVICE_NAME` | `core` | ⚠️ Required - lowercase |
| `MONGO_URI` | `mongodb+srv://username:password@cluster.mongodb.net/?appName=ClusterMain` | Replace with your MongoDB URI |
| `ADMIN_USER` | `admin` | Change for security |
| `ADMIN_PASS` | `admin123` | ⚠️ Change this! |

**Example MongoDB URI**:
```
mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain
```

---

### Service 2: baratie-transaction

| Key | Value | Notes |
|-----|-------|-------|
| `SERVICE_NAME` | `transaction` | ⚠️ Required - lowercase |
| `MONGO_URI` | `mongodb+srv://username:password@cluster.mongodb.net/?appName=ClusterMain` | Same as core service |
| `SENDER_EMAIL` | `your-email@gmail.com` | Gmail address |
| `SENDER_PASSWORD` | `your-app-password` | Gmail App Password (not regular password) |

**How to get Gmail App Password**:
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication (if not already)
3. Create new App Password
4. Select "Mail" and "Other (Custom name)"
5. Copy the 16-character password
6. Use this as `SENDER_PASSWORD`

---

### Service 3: baratie-gateway

| Key | Value | Notes |
|-----|-------|-------|
| `SERVICE_NAME` | `gateway` | ⚠️ Required - lowercase |
| `CORE_SERVICE_URL` | `https://baratie-core.onrender.com` | Your Core service URL |
| `TRANS_SERVICE_URLS` | `https://baratie-transaction.onrender.com` | Your Transaction service URL |

⚠️ **Important**: 
- Deploy Core and Transaction services FIRST
- Copy their URLs from Render dashboard
- Then set these variables

**How to find service URLs**:
1. Go to service in Render dashboard
2. Look at the top - you'll see the URL
3. Format: `https://your-service-name.onrender.com`

---

### Service 4: baratie-frontend

| Key | Value | Notes |
|-----|-------|-------|
| `SERVICE_NAME` | `frontend` | ⚠️ Required - lowercase |
| `GATEWAY_URL` | `https://baratie-gateway.onrender.com` | Your Gateway service URL |

⚠️ **Important**: 
- Deploy Gateway service FIRST
- Copy its URL from Render dashboard
- Then set this variable

---

## 🎯 Quick Copy-Paste Templates

### For Core Service:
```
SERVICE_NAME=core
MONGO_URI=mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain
ADMIN_USER=admin
ADMIN_PASS=admin123
```

### For Transaction Service:
```
SERVICE_NAME=transaction
MONGO_URI=mongodb+srv://deava_sample:deava_0701_sample@clustermain.d1ldf.mongodb.net/?appName=ClusterMain
SENDER_EMAIL=bb1.deavanathan.s@gmail.com
SENDER_PASSWORD=ipwm okbq ryso xyjc
```

### For Gateway Service:
```
SERVICE_NAME=gateway
CORE_SERVICE_URL=https://baratie-core.onrender.com
TRANS_SERVICE_URLS=https://baratie-transaction.onrender.com
```

### For Frontend Service:
```
SERVICE_NAME=frontend
GATEWAY_URL=https://baratie-gateway.onrender.com
```

⚠️ **Remember to replace**:
- MongoDB URI with your own
- Email credentials with your own
- Service URLs with your actual Render URLs

---

## ✅ Validation Checklist

### Core Service
- [ ] `SERVICE_NAME` is exactly `core` (lowercase)
- [ ] `MONGO_URI` starts with `mongodb+srv://`
- [ ] `ADMIN_USER` is set
- [ ] `ADMIN_PASS` is set (changed from default)

### Transaction Service
- [ ] `SERVICE_NAME` is exactly `transaction` (lowercase)
- [ ] `MONGO_URI` is the same as Core Service
- [ ] `SENDER_EMAIL` is a valid Gmail address
- [ ] `SENDER_PASSWORD` is Gmail App Password (16 chars)

### Gateway Service
- [ ] `SERVICE_NAME` is exactly `gateway` (lowercase)
- [ ] `CORE_SERVICE_URL` starts with `https://`
- [ ] `TRANS_SERVICE_URLS` starts with `https://`
- [ ] URLs point to your actual Render services

### Frontend Service
- [ ] `SERVICE_NAME` is exactly `frontend` (lowercase)
- [ ] `GATEWAY_URL` starts with `https://`
- [ ] URL points to your actual Gateway service

---

## 🐛 Common Mistakes

### ❌ Wrong SERVICE_NAME
```
SERVICE_NAME=Gateway  ❌ (uppercase)
SERVICE_NAME=GATEWAY  ❌ (all caps)
SERVICE_NAME=Core     ❌ (capitalized)
```

### ✅ Correct SERVICE_NAME
```
SERVICE_NAME=gateway  ✅
SERVICE_NAME=frontend ✅
SERVICE_NAME=core     ✅
SERVICE_NAME=transaction ✅
```

### ❌ Wrong URLs
```
GATEWAY_URL=http://localhost:5000  ❌ (localhost)
GATEWAY_URL=baratie-gateway        ❌ (no https://)
```

### ✅ Correct URLs
```
GATEWAY_URL=https://baratie-gateway.onrender.com  ✅
CORE_SERVICE_URL=https://baratie-core.onrender.com ✅
```

---

## 🔄 Deployment Order

**Important**: Set environment variables in this order:

1. **Core Service** → Deploy → Get URL
2. **Transaction Service** → Deploy → Get URL
3. **Gateway Service** → Set URLs from steps 1 & 2 → Deploy → Get URL
4. **Frontend Service** → Set URL from step 3 → Deploy

---

## 📞 Troubleshooting

### "SERVICE_NAME not set" error
- Check spelling: must be lowercase
- Check it's actually saved (click "Save Changes")
- Valid values: `gateway`, `frontend`, `core`, `transaction`

### "Connection refused" / 502 errors
- Backend services might not be running
- Check all 4 services show "Live" status
- Verify URLs in environment variables are correct
- Make sure URLs use `https://` not `http://`

### Database connection errors
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas network access allows `0.0.0.0/0`
- Ensure database user has read/write permissions

### Email not sending
- Use Gmail App Password, not regular password
- Verify 2FA is enabled on Gmail account
- Check `SENDER_EMAIL` format is correct

---

## 💡 Pro Tips

1. **Copy-paste carefully**: One typo can break everything
2. **Use the same MongoDB URI**: For both Core and Transaction services
3. **Wait for deployment**: After setting variables, wait for service to redeploy
4. **Check logs**: If something fails, check the Logs tab
5. **Test incrementally**: Test each service after deployment

---

**Need the deployment checklist?** See `DEPLOYMENT_CHECKLIST.md`
