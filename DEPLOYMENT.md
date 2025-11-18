# Deployment Guide for Elaani

## Deploy to Render (Recommended)

### Step 1: Prepare Your GitHub Repository
1. Make sure your code is pushed to GitHub
2. Ensure all files are committed including:
   - `requirements.txt`
   - `render.yaml`
   - `app.py`
   - All templates and static files

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select your repository
4. Render will auto-detect the `render.yaml` configuration
5. Click "Create Web Service"
6. Wait 2-3 minutes for deployment to complete
7. Your app will be live at: `https://your-app-name.onrender.com`

### Step 3: Share with Client
Copy the URL and send it to your client!

## Alternative: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects Flask and deploys
6. Get your live URL from the dashboard

## Alternative: Deploy to Fly.io

1. Install Fly CLI: `powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"`
2. Run: `fly launch` (in the elaani directory)
3. Follow the prompts
4. Deploy: `fly deploy`

## Important Notes

- The app is configured to run on port provided by the hosting platform
- Debug mode is disabled for production
- Make sure your secret key is secure (consider using environment variables)
- Free tiers may have cold starts (first load might be slow)

## Troubleshooting

If deployment fails:
1. Check the build logs on your hosting platform
2. Verify all dependencies are in `requirements.txt`
3. Make sure `gunicorn` is installed
4. Check that all template files are committed to Git
