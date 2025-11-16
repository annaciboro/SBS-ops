# SBS Dashboard - Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Google Cloud Service Account with Sheets API access

---

## Step-by-Step Deployment

### 1. Push to GitHub

First, initialize a git repository and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SBS Dashboard"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/sbs-dashboard.git
git branch -M main
git push -u origin main
```

**IMPORTANT:** Make sure your `.gitignore` is working properly. The following should NOT be in your repo:
- `.streamlit/secrets.toml`
- `config.yaml`
- Any `.json` credential files

---

### 2. Deploy on Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the deployment settings:**
   - **Repository:** `YOUR-USERNAME/sbs-dashboard`
   - **Branch:** `main`
   - **Main file path:** `dashboard.py`
   - **App URL:** Choose your custom URL (e.g., `sbs-dashboard`)

5. **Click "Advanced settings"** (very important!)

---

### 3. Configure Secrets

In the Advanced settings, you need to add your secrets. Click on **"Secrets"** and paste your configuration:

```toml
# Copy the ENTIRE contents of your local .streamlit/secrets.toml file here
# It should look like this:

[gcp_service_account]
type = "service_account"
project_id = "YOUR-PROJECT-ID"
private_key_id = "YOUR-PRIVATE-KEY-ID"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR-PRIVATE-KEY-HERE
-----END PRIVATE KEY-----"""
client_email = "YOUR-SERVICE-ACCOUNT-EMAIL"
client_id = "YOUR-CLIENT-ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR-CERT-URL"
universe_domain = "googleapis.com"

google_sheet_id = "YOUR-GOOGLE-SHEET-ID"

[google_sheets]
SHEET_URL = "YOUR-GOOGLE-SHEETS-URL"
```

**ALSO** add your authentication config:

Create a file called `config.yaml` in the Streamlit Cloud secrets (paste this at the bottom of the secrets):

```toml
# Add this section for authentication
[auth]
credentials = """
credentials:
  usernames:
    sbs.anna.ciboro@gmail.com:
      email: sbs.anna.ciboro@gmail.com
      name: Anna Ciboro
      password: "$2b$12$/e117bp3xq3bi80h/4Y4w.X.pCmfBOaVMeQpxmonw08GaMF4yOwp6"
      admin: true

cookie:
  expiry_days: 0
  key: "7eb707cb9ec9120e9f9ef0edb40dbb3b"
  name: "sbs_auth"

preauthorized:
  emails:
    - sbs.anna.ciboro@gmail.com
"""
```

---

### 4. Update Code for Streamlit Cloud

Your `dashboard.py` needs to load the config from secrets instead of from a file.

The code already handles this, but double-check around line 17-35 in `dashboard.py`:

```python
# Load authentication config
if os.path.exists("config.yaml"):
    # Local development
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
else:
    # Streamlit Cloud deployment - load from secrets
    if hasattr(st, 'secrets') and 'auth' in st.secrets:
        config = yaml.safe_load(st.secrets["auth"]["credentials"])
    else:
        st.error("Authentication configuration not found")
        st.stop()
```

---

### 5. Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes for Streamlit to install dependencies
3. Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

---

## Troubleshooting

### Common Issues:

**1. "ModuleNotFoundError"**
- Check that all packages are in `requirements.txt`
- Make sure versions are compatible

**2. "Google Sheets API Error"**
- Verify your service account has access to the sheet
- Check that `google_sheet_id` is correct in secrets
- Ensure the sheet is shared with your service account email

**3. "Authentication Failed"**
- Make sure you added the `[auth]` section to secrets
- Verify the password hash is correct
- Check that `config.yaml` is NOT in your GitHub repo

**4. "App is slow or timing out"**
- Check your Google Sheets quota
- Consider adding `@st.cache_data` to more functions
- Increase TTL in cache decorators if needed

---

## Managing the Live App

### Updating the App:
Just push to GitHub:
```bash
git add .
git commit -m "Update dashboard"
git push
```

Streamlit Cloud will automatically redeploy!

### Viewing Logs:
- Click on your app in Streamlit Cloud dashboard
- Click "Manage app" → "Logs" to see real-time logs

### Restarting the App:
- Go to Streamlit Cloud dashboard
- Click "Manage app" → "Reboot app"

---

## Security Checklist

Before deploying, verify:

- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] `config.yaml` is in `.gitignore`
- [ ] No `.json` credential files in repo
- [ ] Secrets are properly configured in Streamlit Cloud
- [ ] Google Sheet is only shared with your service account
- [ ] Authentication is enabled and working

---

## Next Steps

After deployment:

1. **Test the live app** thoroughly
2. **Share the URL** with your team
3. **Set up monitoring** (Streamlit Cloud provides basic analytics)
4. **Consider adding a custom domain** (available in Streamlit Cloud)

---

## Support

- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/
- Google Sheets API: https://developers.google.com/sheets/api
