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
    "DOT": {"coingecko": "polkadot", "coincap": "polkadot"},
    "LTC": {"coingecko": "litecoin", "coincap": "litecoin"},
    "XLM": {"coingecko": "stellar", "coincap": "stellar"},
    "LINK": {"coingecko": "chainlink", "coincap": "chainlink"},
    "BCH": {"coingecko": "bitcoin-cash", "coincap": "bitcoin-cash"},
    "ZEC": {"coingecko": "zcash", "coincap": "zcash"},
    "BSV": {"coingecko": "bitcoin-sv", "coincap": "bitcoin-sv"},
    "TRX": {"coingecko": "tron", "coincap": "tron"},
    "ONT": {"coingecko": "ontology", "coincap": "ontology"},
    "ETC": {"coingecko": "ethereum-classic", "coincap": "ethereum-classic"},
    "NEO": {"coingecko": "neo", "coincap": "neo"},
    "IOTA": {"coingecko": "iota", "coincap": "iota"},
    "RED": {"coingecko": "red", "coincap": "red"},
    "AAVE": {"coingecko": "aave", "coincap": "aave"},
    "UNI": {"coingecko": "uniswap", "coincap": "uniswap"},
    "SOLANA": {"coingecko": "solana", "coincap": "solana"},
    "SUSHI": {"coingecko": "sushi", "coincap": "sushi"},
    "YFI": {"coingecko": "yearn-finance", "coincap": "yearn-finance"},
    "CRV": {"coingecko": "curve-dao-token", "coincap": "curve-dao-token"},
    "UNISWAP": {"coingecko": "uniswap", "coincap": "uniswap"},  
    "BELT": {"coingecko": "belt", "coincap": "belt"},
    "KSM": {"coingecko": "kusama", "coincap": "kusama"},
    "SOLANA-SOLV": {"coingecko": "solana-solv", "coincap": "solana-solv"},
    "AAVE-SOLV": {"coingecko": "aave-solv", "coincap": "aave-solv"},
    "UNISWAP-V2": {"coingecko": "uniswap-v2", "coincap": "uniswap-v2"},
    "DAPP": {"coingecko": "dapp", "coincap": "dapp"},
    "BTS": {"coingecko": "bitshares", "coincap": "bitshares"},
    "SKY": {"coingecko": "skycoin", "coincap": "skycoin"},
    "ALGO": {"coingecko": "algorand", "coincap": "algorand"}, 
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
    
    # Track APIs tried and error messages for better error reporting
    apis_tried = []
    error_messages = []
    
    # 1. Try CoinGecko (Primary API)
    try:
        apis_tried.append("CoinGecko")
        response = requests.get(
            f"{COINGECKO_API_URL}/simple/price",
            params={
                "ids": CRYPTO_MAPPING[crypto]["coingecko"],
                "vs_currencies": fiat,
                "include_last_updated_at": "true"
            },
            timeout=5
        )
        
        # Check HTTP status code
        if response.status_code != 200:
            error_messages.append(f"CoinGecko returned status code {response.status_code}")
            raise ValueError(f"CoinGecko API returned status code {response.status_code}")
        
        data = response.json()
        
        # Check if coin data exists
        if CRYPTO_MAPPING[crypto]["coingecko"] not in data:
            error_messages.append(f"CoinGecko: No data found for {crypto}")
            raise ValueError(f"No data found for {crypto} in CoinGecko response")
            
        coin_data = data.get(CRYPTO_MAPPING[crypto]["coingecko"], {})
        
        # Check if fiat currency exists in response
        if fiat not in coin_data:
            error_messages.append(f"CoinGecko: No {fiat} price found for {crypto}")
            raise ValueError(f"No {fiat} price found for {crypto} in CoinGecko response")
        
        # Success case
        last_updated = coin_data.get("last_updated_at", datetime.utcnow().timestamp())
        return coin_data[fiat], {
            "timestamp": datetime.utcfromtimestamp(last_updated),
            "source": crypto,
            "target": fiat,
            "provider": "CoinGecko",
            "type": "crypto"
        }
            
    except Exception as e:
        print(f"Primary crypto API (CoinGecko) failed: {str(e)}")
        # Continue to backup API
    
    # 2. Try CoinCap (Backup API)
    try:
        apis_tried.append("CoinCap")
        response = requests.get(
            f"{BACKUP_CRYPTO_API_URL}/assets/{CRYPTO_MAPPING[crypto]['coincap']}",
            timeout=5
        )
        
        # Check HTTP status code
        if response.status_code != 200:
            error_messages.append(f"CoinCap returned status code {response.status_code}")
            raise ValueError(f"CoinCap API returned status code {response.status_code}")
        
        # Check if response has expected structure
        if 'data' not in response.json():
            error_messages.append("CoinCap: Response missing 'data' field")
            raise ValueError("CoinCap response missing 'data' field")
            
        data = response.json()['data']
        
        # Check if price data exists
        if 'priceUsd' not in data:
            error_messages.append(f"CoinCap: No price data for {crypto}")
            raise ValueError(f"No price data found for {crypto} in CoinCap response")
            
        usd_rate = float(data['priceUsd'])
        
        # Convert to requested fiat if needed
        if fiat != "usd":
            try:
                fiat_rate, fiat_data = get_fiat_rate("USD", fiat.upper())
                final_rate = usd_rate * fiat_rate
            except Exception as fiat_error:
                error_messages.append(f"Failed to convert USD to {fiat.upper()}: {str(fiat_error)}")
                raise ValueError(f"CoinCap provided USD rate but conversion to {fiat.upper()} failed: {str(fiat_error)}")
        else:
            final_rate = usd_rate
        
        # Ensure timestamp is a datetime object
        timestamp = int(data.get('time', datetime.utcnow().timestamp() * 1000)) / 1000
        return final_rate, {
            "timestamp": datetime.utcfromtimestamp(timestamp),
            "source": crypto,
            "target": fiat,
            "provider": "CoinCap",
            "type": "crypto"
        }
            
    except Exception as e:
        print(f"Backup crypto API (CoinCap) failed: {str(e)}")
    
    # 3. Try CryptoCompare (Second Backup API)
    try:
        apis_tried.append("CryptoCompare")
        second_backup_response = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms={fiat.upper()}",
            timeout=5
        )
        
        if second_backup_response.status_code != 200:
            error_messages.append(f"CryptoCompare returned status code {second_backup_response.status_code}")
            raise ValueError(f"CryptoCompare API returned status code {second_backup_response.status_code}")
            
        second_backup_data = second_backup_response.json()
        
        # Check if target currency exists
        if fiat.upper() not in second_backup_data:
            error_messages.append(f"CryptoCompare: No {fiat.upper()} price found for {crypto}")
            raise ValueError(f"No {fiat.upper()} price found for {crypto} in CryptoCompare response")
            
        # Success case
        rate = second_backup_data[fiat.upper()]
        return rate, {
            "timestamp": datetime.utcnow(),
            "source": crypto,
            "target": fiat,
            "provider": "CryptoCompare (Second Backup)",
            "type": "crypto"
        }
    except Exception as second_backup_error:
        print(f"Second backup crypto API (CryptoCompare) failed: {str(second_backup_error)}")
    
    # All APIs failed
    apis_tried_str = ", ".join(apis_tried)
    error_details = " | ".join(error_messages)
    
    # Instead of raising an exception, return a default value with error metadata
    # This allows the application to continue running even when APIs fail
    default_rate = 0.0
    error_metadata = {
        "timestamp": datetime.utcnow(),
        "source": crypto,
        "target": fiat,
        "provider": "Error",
        "type": "crypto",
        "error": f"Failed to retrieve cryptocurrency rate after trying {apis_tried_str}. Errors: {error_details}",
        "rate": default_rate
    }
    
    # Log the error but don't crash the application
    print(f"Error getting exchange rate for {crypto} to {fiat}: {error_metadata['error']}")
    
    # Return a default value with error metadata
    return default_rate, error_metadata