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
    "AED", "SAR", "MYR", "PKR"
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
    
    # Validate currencies before proceeding
    try:
        validate_fiat(source)
        validate_fiat(target)
    except ValueError as e:
        raise ValueError(f"Invalid currency code: {str(e)}")
    
    # If source and target are the same, rate is 1
    if source == target:
        return 1.0, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "self",
            "type": "fiat"
        }

    # Try multiple APIs in sequence with proper error handling
    apis_tried = []
    error_messages = []
    
    # 1. Try ExchangeRate-API (Primary)
    try:
        apis_tried.append("ExchangeRate-API")
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{source}",
            timeout=5
        )
        
        # Check HTTP status code first
        if response.status_code != 200:
            error_messages.append(f"ExchangeRate-API returned status code {response.status_code}")
            raise ValueError(f"API returned status code {response.status_code}")
            
        data = response.json()
        
        # Check for error response
        if 'result' in data and data['result'] == 'error':
            error_type = data.get('error-type', 'unknown error')
            error_messages.append(f"ExchangeRate-API error: {error_type}")
            raise ValueError(f"API returned error: {error_type}")
            
        # Check if 'rates' key exists
        if 'rates' not in data:
            error_messages.append("ExchangeRate-API response missing 'rates' key")
            raise ValueError(f"'rates' key not found in API response: {data}")
            
        # Check if target currency exists in rates
        if target not in data['rates']:
            error_messages.append(f"ExchangeRate-API: Target currency {target} not found in rates")
            raise ValueError(f"Currency {target} not found in exchange rate data")
            
        # Success case
        rate = data['rates'][target]
        return rate, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "ExchangeRate-API",
            "type": "fiat"
        }
    except Exception as e:
        print(f"Primary fiat API (ExchangeRate-API) failed: {str(e)}")
        # Continue to backup API
    
    # 2. Try Frankfurter API (First Backup)
    try:
        apis_tried.append("Frankfurter")
        backup_response = requests.get(
            f"https://api.frankfurter.app/latest?from={source}&to={target}",
            timeout=5
        )
        
        if backup_response.status_code != 200:
            error_messages.append(f"Frankfurter API returned status code {backup_response.status_code}")
            raise ValueError(f"Backup API returned status code {backup_response.status_code}")
            
        backup_data = backup_response.json()
        
        # Check for error response
        if 'error' in backup_data:
            error_messages.append(f"Frankfurter API error: {backup_data['error']}")
            raise ValueError(f"Backup API returned error: {backup_data['error']}")
            
        # Check if rates exist
        if 'rates' not in backup_data:
            error_messages.append("Frankfurter API response missing 'rates' key")
            raise ValueError("'rates' key not found in backup API response")
            
        # Check if target currency exists
        if target not in backup_data['rates']:
            error_messages.append(f"Frankfurter API: Target currency {target} not found in rates")
            raise ValueError(f"Currency {target} not found in backup exchange rate data")
            
        # Success case
        rate = backup_data['rates'][target]
        return rate, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "Frankfurter API (Backup)",
            "type": "fiat"
        }
    except Exception as backup_error:
        print(f"First backup fiat API (Frankfurter) failed: {str(backup_error)}")
        # Continue to second backup API
    
    # 3. Try CurrencyAPI (Second Backup)
    try:
        apis_tried.append("CurrencyAPI")
        second_backup_response = requests.get(
            f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{source.lower()}/{target.lower()}.json",
            timeout=5
        )
        
        if second_backup_response.status_code != 200:
            error_messages.append(f"CurrencyAPI returned status code {second_backup_response.status_code}")
            raise ValueError(f"Second backup API returned status code {second_backup_response.status_code}")
            
        second_backup_data = second_backup_response.json()
        
        # Check if target currency exists
        if target.lower() not in second_backup_data:
            error_messages.append(f"CurrencyAPI: Target currency {target} not found in response")
            raise ValueError(f"Currency {target} not found in second backup API response")
            
        # Success case
        rate = second_backup_data[target.lower()]
        return rate, {
            "timestamp": datetime.utcnow(),
            "source": source,
            "target": target,
            "provider": "CurrencyAPI (Second Backup)",
            "type": "fiat"
        }
    except Exception as second_backup_error:
        print(f"Second backup fiat API (CurrencyAPI) failed: {str(second_backup_error)}")
    
    # All APIs failed
    apis_tried_str = ", ".join(apis_tried)
    error_details = " | ".join(error_messages)
    raise RuntimeError(f"Failed to retrieve fiat exchange rate after trying {apis_tried_str}. Errors: {error_details}")
