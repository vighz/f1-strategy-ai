# 🚀 Deployment Guide

This guide walks through deploying F1 Strategy Room to Render (backend) and Vercel (frontend).

---

## Prerequisites

- [ ] GitHub repository with all code pushed
- [ ] Render account (free tier): https://render.com
- [ ] Vercel account (free tier): https://vercel.com
- [ ] App working locally (test at http://localhost:3000)

---

## Part 1: Deploy Backend to Render

### Step 1: Create Render Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Connect your GitHub account and select your repository

### Step 2: Configure Web Service

**Basic Settings:**
- **Name:** `f1-strategy-room-api` (or your choice)
- **Region:** `Oregon (US West)` (or closest to you)
- **Branch:** `master` (or `main`)
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build & Start Commands:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- **Free** (for portfolio/demo purposes)

### Step 3: Set Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:
| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11` |
| `CORS_ORIGINS` | `https://your-frontend-url.vercel.app` (update after frontend deployment) |

**Note:** You'll update `CORS_ORIGINS` after deploying the frontend in Part 2.

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build and deployment
3. Once deployed, you'll get a URL like: `https://f1-strategy-room-api.onrender.com`

### Step 5: Test Backend

Visit these endpoints to verify:
- **Health check:** `https://your-backend-url.onrender.com/health`
- **API docs:** `https://your-backend-url.onrender.com/docs`
- **Races endpoint:** `https://your-backend-url.onrender.com/api/races/2023`

Expected responses:
- `/health` → `{"status":"healthy","service":"f1-strategy-room-api"}`
- `/api/races/2023` → JSON array of 22 races

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Import Project

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select your GitHub repository
4. Vercel will auto-detect Next.js

### Step 2: Configure Project

**Framework Preset:** `Next.js` (auto-detected)

**Root Directory:** `frontend`

**Build Settings:** (auto-detected from package.json)
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

### Step 3: Set Environment Variables

Click **"Environment Variables"** → **"Add"**

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend-url.onrender.com` (from Part 1, Step 4) |

**Example:**
```
NEXT_PUBLIC_API_URL=https://f1-strategy-room-api.onrender.com
```

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Once deployed, you'll get a URL like: `https://f1-strategy-room.vercel.app`

### Step 5: Update Backend CORS

Now that you have the frontend URL, go back to Render:

1. Go to your Render dashboard → Your web service
2. Click **"Environment"** tab
3. Update `CORS_ORIGINS` to your Vercel URL:
   ```
   https://f1-strategy-room.vercel.app
   ```
4. Click **"Save Changes"**
5. Render will automatically redeploy with new CORS settings

---

## Part 3: Test Deployed App

### Step 1: Open Frontend

Visit your Vercel URL: `https://f1-strategy-room.vercel.app`

### Step 2: Test Full Flow

1. **Load races:** Should see 22 races from 2023 season in grid
2. **Select "Italian Grand Prix"**
3. **Wait 30-60 seconds:** First load will be slow (FastF1 fetching data)
4. **Verify charts load:**
   - Degradation curves (red/yellow/white lines)
   - Top 5 strategies with stint breakdowns
   - Model caveats at bottom

### Step 3: Check for Errors

Open browser Developer Tools (F12) → Console tab

**Common issues:**

| Error | Solution |
|-------|----------|
| CORS error | Update `CORS_ORIGINS` in Render to match Vercel URL exactly |
| 404 on API calls | Verify `NEXT_PUBLIC_API_URL` in Vercel matches Render URL |
| 500 errors | Check Render logs: Dashboard → Your service → Logs |
| Slow loading | Normal on first load (FastF1 downloads telemetry), subsequent loads use cache |

---

## Part 4: Custom Domain (Optional)

### Vercel

1. Go to Vercel dashboard → Your project → Settings → Domains
2. Add your custom domain (e.g., `f1strategy.yourdomain.com`)
3. Follow DNS configuration instructions
4. Update Render `CORS_ORIGINS` to include new domain

### Render

1. Go to Render dashboard → Your service → Settings
2. Scroll to **"Custom Domain"**
3. Add your custom domain (e.g., `api.yourdomain.com`)
4. Follow DNS configuration instructions
5. Update Vercel `NEXT_PUBLIC_API_URL` to new domain

---

## Monitoring & Logs

### Render Logs

View backend logs:
- Dashboard → Your service → **"Logs"** tab
- Shows FastF1 data loading, API requests, errors

### Vercel Logs

View frontend logs:
- Dashboard → Your project → **"Deployments"** → Click deployment → **"Logs"**
- Shows build output, runtime errors

---

## Performance Notes

### Backend (Render Free Tier)

- **Spin-down:** Free tier spins down after 15 minutes of inactivity
- **First request:** May take 30-60 seconds to spin up + FastF1 data load
- **Subsequent requests:** Fast (uses cached data)
- **Upgrade option:** Paid tier ($7/month) for always-on service

### Frontend (Vercel Free Tier)

- **Always-on:** No spin-down delays
- **Fast global CDN:** Sub-second response times
- **Build time:** ~2-3 minutes per deployment

### Caching Strategy

- **FastF1 cache:** Stored on Render's ephemeral disk (lost on redeploy)
- **First race load:** 30-60 seconds
- **Subsequent loads:** <5 seconds
- **Production improvement:** Could add persistent volume or Redis cache

---

## Troubleshooting

### Backend won't start

Check Render logs for:
- Missing dependencies: Verify `requirements.txt` is complete
- Port binding: Ensure `--host 0.0.0.0 --port $PORT`
- Python version: Confirm `PYTHON_VERSION=3.11` is set

### Frontend can't reach backend

1. Test backend directly: `curl https://your-backend-url.onrender.com/health`
2. Check CORS headers: Should include your Vercel URL
3. Verify `NEXT_PUBLIC_API_URL` in Vercel environment variables
4. Check browser console for exact error message

### Data loading takes too long

- **Expected:** 30-60 seconds on first load (FastF1 downloads telemetry)
- **Subsequent loads:** Should be <5 seconds (cached)
- **If always slow:** Check Render logs for errors during FastF1 data fetch

---

## Next Steps

After successful deployment:

1. **Update README.md:**
   - Add live demo link
   - Add deployment status badges
   - Update "Coming Soon" placeholders

2. **Take Screenshots:**
   - Homepage with race selector
   - Degradation chart view
   - Strategy ranking view
   - Add to README.md

3. **Share:**
   - LinkedIn post with demo link
   - Portfolio website
   - GitHub repository description

---

## Cost Summary

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| Render | Free | $0/month | 750 hours/month, spins down after 15min |
| Vercel | Hobby | $0/month | 100GB bandwidth, unlimited deployments |
| **Total** | | **$0/month** | Perfect for portfolio/demo |

---

## Upgrade Path (If Needed)

If you need better performance:

1. **Render Pro:** $7/month
   - Always-on (no spin-down)
   - More RAM (512MB → 2GB)
   - Persistent storage option

2. **Vercel Pro:** $20/month
   - More bandwidth (100GB → 1TB)
   - Better analytics
   - Password protection

**For portfolio demo: Free tier is sufficient!**
