# Currency Converter Streamlit Deployment Guide

This guide will walk you through deploying your Currency Converter application on Streamlit Cloud.

## Prerequisites

- A GitHub account
- Your Currency Converter code pushed to a GitHub repository
- API keys for the currency conversion services (if needed)

## Step 1: Prepare Your Repository

1. Make sure your project structure is organized correctly:
   ```
   Currency_Convertor/
   ├── src/
   │   ├── api/
   │   ├── core/
   │   ├── ui/
   │   ├── main.py
   │   └── requirements.txt
   └── README.md
   ```

2. Fix the requirements.txt file name (currently it's spelled "requirments.txt"):
   - Rename `src/requirments.txt` to `src/requirements.txt`
   - Make sure all dependencies are listed correctly

3. Create a `.streamlit` directory in the root of your project with a `config.toml` file for custom settings (optional):
   ```toml
   [theme]
   primaryColor = "#1E88E5"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   font = "sans serif"
   ```

## Step 2: Set Up GitHub Repository

1. Create a new GitHub repository if you haven't already
2. Push your Currency Converter code to the repository
3. Make sure your main Streamlit app file (`main.py`) is in the correct location

## Step 3: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch, and main file path (`src/main.py`)
5. Click "Deploy"

## Step 4: Configure API Keys in Streamlit Secrets

Your Currency Converter uses several external APIs for currency conversion. You need to securely store these API keys in Streamlit's secrets management:

1. In your Streamlit Cloud dashboard, find your deployed app
2. Click on the three dots (⋮) next to your app and select "Settings"
3. Navigate to the "Secrets" section
4. Add your API keys in TOML format:

```toml
# .streamlit/secrets.toml
[api_keys]
exchangerate_api = "your_exchangerate_api_key"
coingecko_api = "your_coingecko_api_key"
cryptocompare_api = "your_cryptocompare_api_key"
coincap_api = "your_coincap_api_key"
```

## Step 5: Access API Keys in Your Code

Modify your code to use the secrets instead of hardcoded API keys. For example:

```python
# In your API client files
import streamlit as st

# Access the API keys securely
exchangerate_api_key = st.secrets["api_keys"]["exchangerate_api"]
coingecko_api_key = st.secrets["api_keys"]["coingecko_api"]
```

## Step 6: Advanced Streamlit Settings

You can configure additional settings for your Streamlit app:

1. **Memory Management**: If your app requires more memory, you can adjust this in the app settings
2. **Custom Domain**: Set up a custom domain for your app in the Streamlit Cloud settings
3. **Authentication**: Enable authentication to restrict access to your app
4. **Environment Variables**: Configure additional environment variables if needed

## Troubleshooting

- If your app fails to deploy, check the logs in the Streamlit Cloud dashboard
- Ensure all dependencies are correctly listed in `requirements.txt`
- Verify that your API keys are correctly configured in the secrets
- Check that your main file path is correctly specified during deployment

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Secrets Management](https://docs.streamlit.io/library/advanced-features/secrets-management)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)