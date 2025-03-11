# Implementing API Keys with Streamlit Secrets

This guide explains how to modify your Currency Converter code to use Streamlit Secrets for API keys instead of hardcoded values.

## Step 1: Identify API Services Used

Based on the codebase analysis, your Currency Converter uses the following external APIs:

1. **ExchangeRate-API** - For fiat currency conversion
2. **CoinGecko** - For cryptocurrency data
3. **CryptoCompare** - For stablecoin and cryptocurrency data
4. **CoinCap** - As a backup for cryptocurrency data

## Step 2: Create Local Secrets File for Development

Before deploying to Streamlit Cloud, create a local `.streamlit/secrets.toml` file for testing:

```toml
# .streamlit/secrets.toml
[api_keys]
exchangerate_api = "your_exchangerate_api_key"
coingecko_api = "your_coingecko_api_key"
cryptocompare_api = "your_cryptocompare_api_key"
coincap_api = "your_coincap_api_key"
```

**Note:** Add this file to your `.gitignore` to prevent committing sensitive information.

## Step 3: Modify API Client Files

### Update fiat_client.py

Modify the ExchangeRate-API request in `fiat_client.py`:

```python
# Add at the top of the file
import streamlit as st

# Then modify the ExchangeRate-API request
try:
    apis_tried.append("ExchangeRate-API")
    
    # Get API key from Streamlit secrets if available
    api_key_param = {}
    if "api_keys" in st.secrets and "exchangerate_api" in st.secrets["api_keys"]:
        api_key_param = {"apikey": st.secrets["api_keys"]["exchangerate_api"]}
    
    response = requests.get(
        f"https://open.er-api.com/v6/latest/{source}",
        params=api_key_param,
        timeout=5
    )
```

### Update crypto_client.py

Modify the CoinGecko and CoinCap API requests in `crypto_client.py`:

```python
# Add at the top of the file
import streamlit as st

# For CoinGecko API
try:
    apis_tried.append("CoinGecko")
    
    # Get API key from Streamlit secrets if available
    params = {
        "ids": CRYPTO_MAPPING[crypto]["coingecko"],
        "vs_currencies": fiat,
        "include_last_updated_at": "true"
    }
    
    if "api_keys" in st.secrets and "coingecko_api" in st.secrets["api_keys"]:
        params["x_cg_pro_api_key"] = st.secrets["api_keys"]["coingecko_api"]
    
    response = requests.get(
        f"{COINGECKO_API_URL}/simple/price",
        params=params,
        timeout=5
    )

# For CoinCap API
try:
    apis_tried.append("CoinCap")
    
    headers = {}
    if "api_keys" in st.secrets and "coincap_api" in st.secrets["api_keys"]:
        headers = {"Authorization": f"Bearer {st.secrets['api_keys']['coincap_api']}"}
    
    response = requests.get(
        f"{BACKUP_CRYPTO_API_URL}/assets/{CRYPTO_MAPPING[crypto]['coincap']}",
        headers=headers,
        timeout=5
    )
```

### Update CryptoCompare API calls

Modify any CryptoCompare API calls in your code:

```python
# For CryptoCompare API
api_url = "https://min-api.cryptocompare.com/data/price"
params = {"fsym": source, "tsyms": target}

if "api_keys" in st.secrets and "cryptocompare_api" in st.secrets["api_keys"]:
    params["api_key"] = st.secrets["api_keys"]["cryptocompare_api"]

response = requests.get(api_url, params=params, timeout=5)
```

## Step 4: Test Locally

Before deploying to Streamlit Cloud:

1. Create the `.streamlit/secrets.toml` file with your actual API keys
2. Run your app locally with `streamlit run src/main.py`
3. Verify that API calls work correctly with the secrets

## Step 5: Deploy to Streamlit Cloud

Follow the deployment guide to deploy your app to Streamlit Cloud and configure the secrets in the Streamlit Cloud dashboard.

## Additional Tips

### Fallback for Missing API Keys

Implement fallbacks for when API keys are not available:

```python
def get_api_key(service_name):
    """Get API key from Streamlit secrets with fallback"""
    try:
        return st.secrets["api_keys"][service_name]
    except (KeyError, FileNotFoundError):
        # Log warning but don't expose in UI
        print(f"Warning: {service_name} API key not found in secrets")
        return None
```

### Rate Limiting Considerations

Some APIs have different rate limits for authenticated vs. unauthenticated requests. Adjust your caching strategy accordingly when using API keys.