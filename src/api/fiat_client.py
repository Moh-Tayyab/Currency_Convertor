from typing import Any
import requests
from requests import Response
from typing import Tuple, Dict, Any
from datetime import datetime

# Add the FIAT_CURRENCIES set
FIAT_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD",
    "SEK", "KRW", "SGD", "NOK", "MXN", "INR", "RUB", "ZAR", "TRY", "BRL",
    "TWD", "DKK", "PLN", "THB", "IDR", "HUF", "CZK", "ILS", "CLP", "PHP",
    "AED", "SAR", "MYR" "PKR"
}

# Supported stablecoins and their CoinGecko IDs
SUPPORTED_STABLECOINS = {"USDT", "USDC", "DAI", "BUSD"}

STABLECOIN_IDS = {
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI": "dai",
    "BUSD": "binance-usd"
}

def validate_stablecoin(currency: str) -> None:
    """Validate if a currency code is a supported stablecoin."""
    if currency.upper() not in SUPPORTED_STABLECOINS:
        raise ValueError(f"Unsupported stablecoin: {currency}")

def validate_fiat(currency: str) -> None:
    """Validate if a currency code is a supported fiat currency."""
    if currency.upper() not in FIAT_CURRENCIES:
        raise ValueError(f"Unsupported fiat currency: {currency}")

def get_stablecoin_rate(source: str, target: str) -> Tuple[float, Dict[str, Any]]:
    """
    Get exchange rate between two stablecoins.
    
    Args:
        source: Source stablecoin (e.g., "USDT")
        target: Target stablecoin (e.g., "USDC")
        
    Returns:
        Tuple of (rate, metadata) where rate is the amount of target stablecoin per unit of source,
        and metadata includes timestamp, source, target, provider, and type.
    """
    # Convert to uppercase for consistency with API expectations
    source = source.upper()
    target = target.upper()
    
    # Validate inputs
    validate_stablecoin(source)
    validate_stablecoin(target)
    
    # If source and target are the same, rate is 1
    if source == target:
        return 1.0, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "self",
            "type": "stablecoin"
        }
    
    # Try primary API: CryptoCompare
    try:
        response = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={source}&tsyms={target}",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if target in data:
                rate = data[target]
                return rate, {
                    "timestamp": datetime.utcnow(),
                    "source": source,
                    "target": target,
                    "provider": "CryptoCompare",
                    "type": "stablecoin"
                }
            else:
                raise ValueError("Missing rate data from CryptoCompare")
    except Exception as e:
        print(f"Primary stablecoin API failed: {str(e)}")
    
    # Try backup API: CoinGecko
    try:
        ids = ",".join([STABLECOIN_IDS[source], STABLECOIN_IDS[target]])
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if (STABLECOIN_IDS[source] in data and "usd" in data[STABLECOIN_IDS[source]] and
                STABLECOIN_IDS[target] in data and "usd" in data[STABLECOIN_IDS[target]]):
                price_source = data[STABLECOIN_IDS[source]]["usd"]
                price_target = data[STABLECOIN_IDS[target]]["usd"]
                rate = price_source / price_target  # Rate = price of source in USD / price of target in USD
                return rate, {
                    "timestamp": datetime.utcnow(),
                    "source": source,
                    "target": target,
                    "provider": "CoinGecko",
                    "type": "stablecoin"
                }
            else:
                raise ValueError("Missing price data from CoinGecko")
    except Exception as e:
        print(f"Backup stablecoin API failed: {str(e)}")
        raise RuntimeError("All stablecoin APIs failed")
    
    # If both APIs fail
    raise RuntimeError("Failed to retrieve stablecoin exchange rate")

def get_fiat_rate(source: str, target: str) -> Tuple[float, Dict[str, Any]]:
    """
    Get exchange rate between two fiat currencies.
    
    Args:
        source: Source currency code (e.g., "USD")
        target: Target currency code (e.g., "EUR")
        
    Returns:
        Tuple of (rate, metadata) where rate is the amount of target currency per unit of source,
        and metadata includes timestamp, source, target, provider, and type.
    """
    # Convert to uppercase for consistency
    source = source.upper()
    target = target.upper()
    
    # If source and target are the same, rate is 1
    if source == target:
        return 1.0, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "self",
            "type": "fiat"
        }

    try:
        # Using ExchangeRate-API as the primary source
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{source}",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if target in data['rates']:
                rate = data['rates'][target]
                return rate, {
                    "timestamp": datetime.utcnow(),
                    "source": source,
                    "target": target,
                    "provider": "ExchangeRate-API",
                    "type": "fiat"
                }
            else:
                raise ValueError(f"Currency {target} not found in exchange rate data")
    except Exception as e:
        print(f"Fiat exchange rate API failed: {str(e)}")
        raise RuntimeError("Failed to retrieve fiat exchange rate")    
    # Return statement for the case when no exceptions are raised but no rate is found
    raise RuntimeError("Failed to retrieve fiat exchange rate")
