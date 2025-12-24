# Visual Deployment Guide for Render

## 🎯 Overview: What You're Building

```
┌─────────────────────────────────────────────────────────┐
│                    RENDER CLOUD                          │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Frontend   │  │  API Gateway │  │ Core Service │  │
│  │              │  │              │  │              │  │
│  │ SERVICE_NAME │  │ SERVICE_NAME │  │ SERVICE_NAME │  │
│  │  = frontend  │  │  = gateway   │  │  = core      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐                                       │
│  │ Transaction  │                                       │
│  │   Service    │                                       │
│  │ SERVICE_NAME │                                       │
│  │= transaction │                                       │
│  └──────────────┘                                       │
│                                                          │
│  All 4 services use the SAME Dockerfile!                │
│  Different SERVICE_NAME = Different service runs        │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Visual Guide

### Step 1: Create Service on Render

```
┌─────────────────────────────────────────┐
│  Render Dashboard                        │
├─────────────────────────────────────────┤
│                                          │
│  [+ New]  ▼                              │
│    │                                     │
│    ├─ Web Service  ← Click this         │
│    ├─ Static Site                       │
│    ├─ Private Service                   │
│    └─ Cron Job                          │
│                                          │
└─────────────────────────────────────────┘
```

### Step 2: Connect Repository

```
┌─────────────────────────────────────────┐
│  Connect a repository                    │
├─────────────────────────────────────────┤
│                                          │
│  GitHub                                  │
│  ┌────────────────────────────────────┐ │
│  │ your-username/Food_Ordering        │ │
│  │ [Connect]                          │ │
│  └────────────────────────────────────┘ │
│                                          │
└─────────────────────────────────────────┘
```

### Step 3: Configure Service (Example: Core Service)

```
┌─────────────────────────────────────────┐
│  Create Web Service                      │
├─────────────────────────────────────────┤
│                                          │
│  Name: baratie-core                     │
│                                          │
│  Region: [Oregon (US West)]  ▼          │
│                                          │
│  Branch: main                           │
│                                          │
│  Root Directory: [leave blank]          │
│                                          │
│  Environment: Docker  ◉                 │
│                                          │
│  Dockerfile Path: Dockerfile            │
│                                          │
│  Docker Command: [leave blank]          │
│                                          │
│  Instance Type: Free  ◉                 │
│                                          │
└─────────────────────────────────────────┘
```

### Step 4: Add Environment Variables

```
┌─────────────────────────────────────────┐
│  Environment Variables                   │
├─────────────────────────────────────────┤
│                                          │
│  [+ Add Environment Variable]            │
│                                          │
│  ┌──────────────┬────────────────────┐  │
│  │ Key          │ Value              │  │
│  ├──────────────┼────────────────────┤  │
│  │ SERVICE_NAME │ core               │  │
│  ├──────────────┼────────────────────┤  │
│  │ MONGO_URI    │ mongodb+srv://...  │  │
│  ├──────────────┼────────────────────┤  │
│  │ ADMIN_USER   │ admin              │  │
│  ├──────────────┼────────────────────┤  │
│  │ ADMIN_PASS   │ admin123           │  │
│  └──────────────┴────────────────────┘  │
│                                          │
│  [Create Web Service]                    │
│                                          │
└─────────────────────────────────────────┘
```

### Step 5: Wait for Deployment

```
┌─────────────────────────────────────────┐
│  baratie-core                            │
├─────────────────────────────────────────┤
│                                          │
│  Status: ⚙️ Building...                  │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Building Docker image...           │ │
│  │ Installing dependencies...         │ │
│  │ Starting service...                │ │
│  └────────────────────────────────────┘ │
│                                          │
│  Wait 2-5 minutes...                    │
│                                          │
└─────────────────────────────────────────┘
```

### Step 6: Service is Live!

```
┌─────────────────────────────────────────┐
│  baratie-core                            │
├─────────────────────────────────────────┤
│                                          │
│  Status: ✅ Live                         │
│                                          │
│  URL: https://baratie-core.onrender.com │
│       ↑ COPY THIS URL!                  │
│                                          │
│  [Logs] [Environment] [Settings]        │
│                                          │
└─────────────────────────────────────────┘
```

---

## 🔄 Deployment Order (IMPORTANT!)

```
Step 1: Deploy Core Service
   ↓
   Copy URL: https://baratie-core.onrender.com
   ↓
Step 2: Deploy Transaction Service
   ↓
   Copy URL: https://baratie-transaction.onrender.com
   ↓
Step 3: Deploy API Gateway
   ↓
   Use URLs from Step 1 & 2 in environment variables:
   - CORE_SERVICE_URL = https://baratie-core.onrender.com
   - TRANS_SERVICE_URLS = https://baratie-transaction.onrender.com
   ↓
   Copy URL: https://baratie-gateway.onrender.com
   ↓
Step 4: Deploy Frontend
   ↓
   Use URL from Step 3 in environment variables:
   - GATEWAY_URL = https://baratie-gateway.onrender.com
   ↓
   ✅ DONE! Access: https://baratie-frontend.onrender.com
```

---

## 📊 Environment Variables Cheat Sheet

### Core Service
```
┌──────────────┬────────────────────────────────────┐
│ Key          │ Value                              │
├──────────────┼────────────────────────────────────┤
│ SERVICE_NAME │ core                               │
│ MONGO_URI    │ mongodb+srv://user:pass@cluster... │
│ ADMIN_USER   │ admin                              │
│ ADMIN_PASS   │ your-password                      │
└──────────────┴────────────────────────────────────┘
```

### Transaction Service
```
┌──────────────────┬────────────────────────────────┐
│ Key              │ Value                          │
├──────────────────┼────────────────────────────────┤
│ SERVICE_NAME     │ transaction                    │
│ MONGO_URI        │ mongodb+srv://user:pass@...    │
│ SENDER_EMAIL     │ your-email@gmail.com           │
│ SENDER_PASSWORD  │ your-app-password              │
└──────────────────┴────────────────────────────────┘
```

### API Gateway
```
┌──────────────────┬────────────────────────────────────┐
│ Key              │ Value                              │
├──────────────────┼────────────────────────────────────┤
│ SERVICE_NAME     │ gateway                            │
│ CORE_SERVICE_URL │ https://baratie-core.onrender.com  │
│ TRANS_SERVICE... │ https://baratie-trans.onrender.com │
└──────────────────┴────────────────────────────────────┘
```

### Frontend
```
┌──────────────┬────────────────────────────────────────┐
│ Key          │ Value                                  │
├──────────────┼────────────────────────────────────────┤
│ SERVICE_NAME │ frontend                               │
│ GATEWAY_URL  │ https://baratie-gateway.onrender.com   │
└──────────────┴────────────────────────────────────────┘
```

---

## ✅ Verification Checklist

After deployment, verify each service:

### Core Service
```
Visit: https://baratie-core.onrender.com/hotel/list
Expected: JSON response with hotels list (might be empty)
```

### Transaction Service
```
Check Logs: Should see "Transaction Service running on port..."
No direct URL to test (internal service)
```

### API Gateway
```
Visit: https://baratie-gateway.onrender.com/hotel/list
Expected: Same JSON as Core Service (proxied)
```

### Frontend
```
Visit: https://baratie-frontend.onrender.com
Expected: Login/Register page
```

---

## 🐛 Common Errors & Solutions

### Error: "SERVICE_NAME not set"
```
❌ Problem: SERVICE_NAME environment variable missing
✅ Solution: 
   1. Go to service → Environment tab
   2. Add: SERVICE_NAME = core (or gateway/frontend/transaction)
   3. Save Changes
```

### Error: "502 Bad Gateway"
```
❌ Problem: Backend service not running or wrong URL
✅ Solution:
   1. Check all 4 services show "Live" status
   2. Verify URLs in environment variables
   3. Make sure URLs use https:// not http://
```

### Error: "Connection to MongoDB failed"
```
❌ Problem: MongoDB URI incorrect or network access blocked
✅ Solution:
   1. Check MONGO_URI is correct
   2. In MongoDB Atlas: Network Access → Allow 0.0.0.0/0
   3. Verify database user has read/write permissions
```

---

## 🎉 Success Indicators

You know it's working when:

1. ✅ All 4 services show "Live" status in Render
2. ✅ Frontend loads at https://baratie-frontend.onrender.com
3. ✅ You can register a new user
4. ✅ You can login
5. ✅ You can see restaurants (if any added)
6. ✅ Admin panel works at /admin

---

## 📞 Still Stuck?

1. **Check Logs**: Each service → Logs tab → Look for errors
2. **Verify Variables**: Each service → Environment tab → Check all values
3. **Review Checklist**: See DEPLOYMENT_CHECKLIST.md
4. **Check Order**: Did you deploy in the correct order?

---

**Remember**: The key is the `SERVICE_NAME` environment variable!
- Same Dockerfile
- Different SERVICE_NAME
- Different service runs

**Good luck! 🚀**
