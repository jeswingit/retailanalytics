# ✅ Deployment Checklist

Use this checklist to deploy your dashboard step-by-step.

---

## 🚨 CRITICAL SECURITY STEPS (DO FIRST!)

- [ ] **Go to https://platform.openai.com/api-keys**
- [ ] **Revoke the old exposed API key** (starts with `sk-proj-Wbv...`)
- [ ] **Create a new API key** and save it securely
- [ ] **Close any chat windows** where the old key was visible

---

## 📝 PREPARATION

- [ ] Read `SECURITY_NOTICE.md`
- [ ] Read `DEPLOYMENT_GUIDE.md` or `QUICK_DEPLOY.md`
- [ ] Have your new OpenAI API key ready
- [ ] Ensure `customer_shopping_data.csv` exists in your project folder

---

## 🔧 CODE IS READY

- [x] API key removed from code (now uses secrets)
- [x] `.gitignore` created (prevents committing secrets)
- [x] `requirements.txt` includes all dependencies
- [x] Code updated to use Streamlit secrets

---

## 📦 GITHUB SETUP

- [ ] **Create GitHub account** (if you don't have one)
  - Sign up at: https://github.com
  
- [ ] **Push your code to GitHub**:
  
  **Option A: GitHub Desktop (Recommended for beginners)**
  - [ ] Download from: https://desktop.github.com/
  - [ ] Open GitHub Desktop
  - [ ] File → Add Local Repository
  - [ ] Browse to: `D:\Cursor\Sales Data`
  - [ ] Click "Publish repository"
  - [ ] **Uncheck "Keep this code private"** ⚠️ (must be public)
  - [ ] Click "Publish Repository"
  
  **Option B: Command Line**
  - [ ] Open PowerShell in `D:\Cursor\Sales Data`
  - [ ] Run: `git init`
  - [ ] Run: `git add .`
  - [ ] Run: `git commit -m "Initial commit"`
  - [ ] Create repo at: https://github.com/new
  - [ ] Name it: `jj-analytics-dashboard`
  - [ ] Make it **PUBLIC** ⚠️
  - [ ] Run: `git remote add origin https://github.com/YOUR_USERNAME/jj-analytics-dashboard.git`
  - [ ] Run: `git branch -M main`
  - [ ] Run: `git push -u origin main`

---

## 🌐 STREAMLIT CLOUD DEPLOYMENT

- [ ] **Sign up for Streamlit Cloud**:
  - [ ] Go to: https://share.streamlit.io/
  - [ ] Click "Sign up"
  - [ ] Choose "Continue with GitHub"
  - [ ] Authorize Streamlit Cloud

- [ ] **Create New App**:
  - [ ] Click "New app"
  - [ ] Select repository: `YOUR_USERNAME/jj-analytics-dashboard`
  - [ ] Branch: `main`
  - [ ] Main file: `dashboard_with_gpt.py`
  - [ ] (Optional) Customize app URL

- [ ] **Add API Key Secret** ⚠️ CRITICAL:
  - [ ] Click "Advanced settings..."
  - [ ] In "Secrets" box, add:
    ```toml
    OPENAI_API_KEY = "your-new-api-key-here"
    ```
  - [ ] Replace with your NEW API key
  - [ ] Click "Deploy!"

- [ ] **Wait for deployment** (2-5 minutes)

---

## 🎉 POST-DEPLOYMENT

- [ ] **Test your dashboard**:
  - [ ] Visit your app URL
  - [ ] Check all visualizations load
  - [ ] Open AI Chatbot
  - [ ] Ask a test question
  - [ ] Verify filters work

- [ ] **Set up monitoring**:
  - [ ] Bookmark Streamlit Cloud dashboard: https://share.streamlit.io/
  - [ ] Bookmark OpenAI usage: https://platform.openai.com/usage
  - [ ] Set spending limits: https://platform.openai.com/settings/organization/limits

- [ ] **Share your dashboard**:
  - [ ] Copy your app URL
  - [ ] Share with stakeholders
  - [ ] Add to portfolio/LinkedIn
  - [ ] Celebrate! 🎊

---

## 💻 LOCAL DEVELOPMENT SETUP (Optional)

- [ ] Create `.streamlit/secrets.toml`:
  ```bash
  # Windows PowerShell
  New-Item -Path ".streamlit" -ItemType Directory -Force
  Set-Content -Path ".streamlit\secrets.toml" -Value 'OPENAI_API_KEY = "your-new-api-key-here"'
  ```

- [ ] Add your new API key to `.streamlit/secrets.toml`

- [ ] Test locally:
  ```bash
  python -m streamlit run dashboard_with_gpt.py
  ```

---

## 🔒 SECURITY VERIFICATION

- [ ] **Old API key is revoked** ✅
- [ ] **New API key is NOT in any code files** ✅
- [ ] **`.streamlit/secrets.toml` is in `.gitignore`** ✅
- [ ] **No secrets committed to GitHub** ✅
- [ ] **Spending limits set on OpenAI** ✅

---

## 📊 SUCCESS METRICS

Once deployed, you should have:
- ✅ Live dashboard accessible via public URL
- ✅ AI chatbot working with new secure API key
- ✅ All visualizations rendering correctly
- ✅ Filters functioning properly
- ✅ No security warnings or errors
- ✅ Monitoring set up for usage and costs

---

## 🆘 HELP & SUPPORT

If you get stuck:
- Read: `DEPLOYMENT_GUIDE.md` (detailed instructions)
- Read: `QUICK_DEPLOY.md` (simplified guide)
- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Forum: https://discuss.streamlit.io/

---

**Estimated Total Time: 10-15 minutes**

**Current Status**: Ready to deploy! 🚀

