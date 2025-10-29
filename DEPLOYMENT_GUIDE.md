# 🚀 Deployment Guide - JJ Analytics Dashboard

Deploy your Retail Sales Dashboard to **Streamlit Community Cloud** (100% FREE!)

---

## 🚨 CRITICAL FIRST STEP - Secure Your API Key

### ⚠️ Your API Key is Compromised!

**IMMEDIATELY do the following:**

1. **Revoke your current OpenAI API key** (the one that was hardcoded)
   - Go to: https://platform.openai.com/api-keys
   - Find the key and click **"Revoke"**
   
2. **Generate a new API key**
   - Click **"Create new secret key"**
   - Give it a name (e.g., "JJ Analytics Dashboard")
   - **Copy it immediately** - you won't see it again!
   - Keep it somewhere safe (like a password manager)

---

## 📋 Prerequisites

1. **GitHub Account** (free)
   - Sign up at: https://github.com
   
2. **Streamlit Community Cloud Account** (free)
   - Sign up at: https://share.streamlit.io/
   - Link it to your GitHub account

3. **OpenAI API Key** (paid, but cheap for low usage)
   - Get from: https://platform.openai.com/api-keys

---

## 🎯 Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - JJ Analytics Dashboard"
   ```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it: `jj-analytics-dashboard`
   - Make it **PUBLIC** (required for free Streamlit hosting)
   - **DO NOT** add README, .gitignore, or license (we already have them)
   - Click **"Create repository"**

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/jj-analytics-dashboard.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Community Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io/
   - Click **"New app"**

2. **Configure your app**:
   - **Repository**: Select your `jj-analytics-dashboard` repo
   - **Branch**: `main`
   - **Main file path**: `dashboard_with_gpt.py`
   - Click **"Advanced settings"** (optional but recommended)

3. **Add your API Key as a Secret** (CRITICAL STEP):
   - In the **"Secrets"** section, add:
   ```toml
   OPENAI_API_KEY = "your-new-openai-api-key-here"
   ```
   - Replace with your **NEW** API key (not the old compromised one!)

4. **Deploy**:
   - Click **"Deploy!"**
   - Wait 2-5 minutes for deployment
   - Your dashboard will be live at: `https://YOUR_APP_NAME.streamlit.app/`

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use Streamlit secrets for API keys
- ✅ Keep `.gitignore` to prevent committing secrets
- ✅ Revoke compromised keys immediately
- ✅ Use environment variables for local development
- ✅ Regularly rotate API keys

### ❌ DON'T:
- ❌ **NEVER** hardcode API keys in your code
- ❌ **NEVER** commit secrets.toml to Git
- ❌ **NEVER** share API keys in chat/email
- ❌ **NEVER** commit .env files

---

## 🛠️ Local Development Setup (After Securing API Key)

1. **Create `.streamlit/secrets.toml`**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Add your NEW API key** to `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-new-openai-api-key-here"
   ```

3. **Run locally**:
   ```bash
   python -m streamlit run dashboard_with_gpt.py
   ```

---

## 🌐 Alternative: Set Environment Variable (Local Only)

Instead of using secrets.toml locally, you can set an environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-new-api-key-here"
python -m streamlit run dashboard_with_gpt.py
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="your-new-api-key-here"
python -m streamlit run dashboard_with_gpt.py
```

---

## 📊 Monitoring Your Deployed App

### Streamlit Cloud Dashboard:
- View app status, logs, and metrics
- Manage secrets
- Reboot or redeploy the app
- Access at: https://share.streamlit.io/

### OpenAI Usage:
- Monitor API usage and costs
- View at: https://platform.openai.com/usage

---

## 🔄 Updating Your Deployed App

1. **Make changes locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. **Auto-deploy**: Streamlit Cloud will automatically redeploy!

---

## 💰 Cost Estimate

### Streamlit Community Cloud:
- ✅ **100% FREE**
- Includes: 1 GB RAM, unlimited public apps

### OpenAI API:
- 💵 **Pay-as-you-go**
- GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Estimated: **$5-20/month** for moderate usage
- Set usage limits at: https://platform.openai.com/settings/organization/limits

---

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"
**Solution**: Add `OPENAI_API_KEY` to Streamlit Cloud secrets or local `.streamlit/secrets.toml`

### Issue: App won't start
**Solution**: Check logs in Streamlit Cloud dashboard for errors

### Issue: API rate limit exceeded
**Solution**: 
- Wait a few minutes
- Upgrade OpenAI plan
- Implement rate limiting in your app

### Issue: Data file not found
**Solution**: 
- Ensure `customer_shopping_data.csv` is committed to GitHub
- Check file path is correct in code

---

## 📝 Sharing Your Dashboard

Once deployed, share your dashboard URL:
```
https://YOUR_APP_NAME.streamlit.app/
```

**Tips for sharing:**
- 🔗 Add to your LinkedIn profile
- 📧 Send to stakeholders
- 📱 Works on mobile devices!
- 🌍 Accessible worldwide

---

## 🎉 You're Live!

Your professional retail analytics dashboard is now deployed and accessible to anyone with the link!

**Next Steps:**
- Monitor usage and costs
- Gather feedback from users
- Iterate and improve
- Add more features!

---

## 🆘 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/
- **OpenAI Support**: https://help.openai.com/

---

**Built with ❤️ by JJ Analytics**

