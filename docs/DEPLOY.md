# 🚀 Deployment Guide

## Option 1: Streamlit Cloud (Recommended — Free + Easy)

### Prerequisites
- GitHub account
- 5 minutes

### Steps

**1. Push to GitHub**
```bash
cd portfolio_demo
git init
git add .
git commit -m "Initial portfolio demo"
git branch -M main
# Create a new repo on github.com first, then:
git remote add origin https://github.com/YOUR-USERNAME/auto-sales-pipeline.git
git push -u origin main
```

**2. Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Click "Sign in with GitHub"
- Click "New app"
- Repository: `YOUR-USERNAME/auto-sales-pipeline`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Click **Deploy**

**3. Your demo is live!**
- URL: `https://YOUR-APP-NAME.streamlit.app`
- Auto-updates on every git push
- Free forever (with reasonable usage)

**4. Add to your resume / LinkedIn**
```
🔗 Live Demo: https://YOUR-APP-NAME.streamlit.app
📂 Code: https://github.com/YOUR-USERNAME/auto-sales-pipeline
```

---

## Option 2: Run Locally

```bash
git clone <your-repo>
cd portfolio_demo
pip install -r requirements.txt
streamlit run streamlit_app.py
# Open browser → http://localhost:8501
```

---

## Customization Checklist

Before deploying, replace placeholders:

- [ ] `README.md`: Update GitHub username
- [ ] `streamlit_app.py`: Update contact email + GitHub URL
- [ ] `pages/5_👋_About.py`: Personal email, LinkedIn, GitHub
- [ ] Optional: Add your photo to `assets/profile.jpg`
- [ ] Optional: Update color theme in custom CSS

---

## Troubleshooting

**Issue: "Module not found" on Streamlit Cloud**
→ Make sure `requirements.txt` is in the project root, not inside a subfolder.

**Issue: Page shows but data missing**
→ Mock CSV at `data/mock_combined.csv` must be committed to GitHub (not in `.gitignore`).

**Issue: Custom font/CSS not showing**
→ Streamlit Cloud may sandbox some inline styles. Move to `.streamlit/config.toml` for production.
