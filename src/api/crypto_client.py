import requests
from typing import Tuple, Dict, Any
from datetime import datetime

from api.fiat_client import FIAT_CURRENCIES, get_fiat_rate

# API configuration
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
BACKUP_CRYPTO_API_URL = "https://api.coincap.io/v2"

# Supported cryptocurrencies and their IDs
CRYPTO_MAPPING = {
    "BTC": {"coingecko": "bitcoin", "coincap": "bitcoin"},
    "ETH": {"coingecko": "ethereum", "coincap": "ethereum"},
    "USDT": {"coingecko": "tether", "coincap": "tether"},
    "BNB": {"coingecko": "binancecoin", "coincap": "binance-coin"},
    "USDC": {"coingecko": "usd-coin", "coincap": "usd-coin"},
    "XRP": {"coingecko": "ripple", "coincap": "xrp"},
    "SOL": {"coingecko": "solana", "coincap": "solana"},
    "ADA": {"coingecko": "cardano", "coincap": "cardano"},
    "DOGE": {"coingecko": "dogecoin", "coincap": "dogecoin"},
    "DOT": {"coingecko": "polkadot", "coincap": "polkadot"}
}

def validate_crypto_currency(currency: str) -> None:
    """Validate if a currency code is a supported cryptocurrency."""
    if currency.upper() not in CRYPTO_MAPPING:
        raise ValueError(f"Unsupported cryptocurrency: {currency}")

def get_crypto_rate(crypto: str, fiat: str = "USD") -> Tuple[float, Dict[str, Any]]:
    """
    Get exchange rate between cryptocurrency and fiat currency.
    
    Args:
        crypto: Cryptocurrency code (e.g. BTC)
        fiat: Fiat currency code (e.g. USD)
        
    Returns:
        Tuple of (rate, metadata)
    """
    # Validate inputs
    validate_crypto_currency(crypto)
    if fiat.upper() not in FIAT_CURRENCIES:  # Reuse fiat validation from fiat_client
        raise ValueError(f"Unsupported fiat currency: {fiat}")
    
    crypto = crypto.upper()
    fiat = fiat.lower()
    
    try:
        # Primary API call (CoinGecko)
        response = requests.get(
            f"{COINGECKO_API_URL}/simple/price",
            params={
                "ids": CRYPTO_MAPPING[crypto]["coingecko"],
                "vs_currencies": fiat,
                "include_last_updated_at": True
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            coin_data = data.get(CRYPTO_MAPPING[crypto]["coingecko"], {})
            
            return coin_data[fiat], {
                "timestamp": datetime.utcfromtimestamp(coin_data.get("last_updated_at", datetime.utcnow().timestamp())),
                "source": crypto,
                "target": fiat,
                "provider": "CoinGecko",
                "type": "crypto"
            }
            
    except Exception as e:
        print(f"Primary crypto API failed: {str(e)}")
    
    try:
        # Backup API call (CoinCap)
        response = requests.get(
            f"{BACKUP_CRYPTO_API_URL}/assets/{CRYPTO_MAPPING[crypto]['coincap']}",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()['data']
            usd_rate = float(data['priceUsd'])
            
            # Convert to requested fiat if needed
            if fiat != "usd":
                _, fiat_data = get_fiat_rate("USD", fiat.upper())
                conversion_rate = fiat_data['rate']
                final_rate = usd_rate * conversion_rate
            else:
                final_rate = usd_rate
                
            return final_rate, {
                "timestamp": datetime.utcfromtimestamp(int(data['time'])/1000),
                "source": crypto,
                "target": fiat,
                "provider": "CoinCap",
                "type": "crypto"
            }
            
    except Exception as e:
        print(f"Backup crypto API failed: {str(e)}")
        raise RuntimeError("All cryptocurrency APIs failed")

    raise RuntimeError("Failed to retrieve cryptocurrency rate")