import requests
from typing import Tuple, Dict, Any
from datetime import datetime

# API configuration
FIAT_API_BASE_URL = "https://api.frankfurter.app/latest"
BACKUP_FIAT_API_URL = "https://open.er-api.com/v6/latest"

# Supported fiat currencies (ISO 4217 codes)
FIAT_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY", "SEK", "NZD",
    "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "INR", "RUB", "BRL", "ZAR",
    "DKK", "PLN", "THB", "IDR", "HUF", "CZK", "ILS", "CLP", "PHP", "AED",
    "COP", "SAR", "MYR", "RON", "BGN", "HRK", "ISK", "PKR"
}

def validate_fiat_currency(currency: str) -> None:
    """Validate if a currency code is a supported fiat currency."""
    if currency.upper() not in FIAT_CURRENCIES:
        raise ValueError(f"Unsupported fiat currency: {currency}")

def get_fiat_rate(source: str, target: str) -> Tuple[float, Dict[str, Any]]:
    """
    Get exchange rate between two fiat currencies.
    
    Args:
        source: Source fiat currency (3-letter code)
        target: Target fiat currency (3-letter code)
        
    Returns:
        Tuple of (rate, metadata)
    """
    # Validate currencies
    validate_fiat_currency(source)
    validate_fiat_currency(target)
    
    try:
        # Primary API call
        response = requests.get(
            f"{FIAT_API_BASE_URL}",
            params={"from": source, "to": target},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'][target]
            
            return rate, {
                "timestamp": datetime.strptime(data['date'], "%Y-%m-%d"),
                "source": source,
                "target": target,
                "provider": "Frankfurter",
                "type": "fiat"
            }
            
    except Exception as e:
        print(f"Primary fiat API failed: {str(e)}")
    
    try:
        # Backup API call
        response = requests.get(
            f"{BACKUP_FIAT_API_URL}/{source}",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'][target]
            
            return rate, {
                "timestamp": datetime.utcfromtimestamp(data['time_last_update_unix']),
                "source": source,
                "target": target,
                "provider": "ExchangeRate-API",
                "type": "fiat"
            }
            
    except Exception as e:
        print(f"Backup fiat API failed: {str(e)}")
        raise RuntimeError("All fiat currency APIs failed")

    raise RuntimeError("Failed to retrieve fiat exchange rate")