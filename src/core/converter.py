# core/converter.py
import datetime
from typing import Dict, Tuple, List, Any, Optional
import streamlit as st
from api.fiat_client import get_fiat_rate
from api.crypto_client import get_crypto_rate
from core.cache import get_cached_rate, cache_rate

def is_crypto(currency_code: str) -> bool:
    """
    Determine if a currency code is a cryptocurrency.
    
    Args:
        currency_code: The currency code to check
        
    Returns:
        bool: True if cryptocurrency, False if fiat
    """
    crypto_currencies = ["BTC", "ETH", "USDT", "BNB", "USDC", "XRP", "SOL", "ADA", "DOGE", "DOT"]
    return currency_code.upper() in crypto_currencies

def get_exchange_rate(source: str, target: str) -> Tuple[float, Dict[str, Any]]:
    """
    Get the current exchange rate between two currencies.
    
    Args:
        source: Source currency code
        target: Target currency code
        
    Returns:
        Tuple containing:
            - float: The exchange rate
            - Dict: Metadata about the rate (timestamp, source API, etc.)
    """
    # Check cache first
    cached_data = get_cached_rate(source, target)
    if cached_data:
        return cached_data["rate"], cached_data
    
    # Handle different currency type combinations
    source_is_crypto = is_crypto(source)
    target_is_crypto = is_crypto(target)
    
    try:
        # Case 1: Crypto to Crypto
        if source_is_crypto and target_is_crypto:
            # Get rates in USD, then calculate cross-rate
            source_usd_rate, source_metadata = get_crypto_rate(source, "USD")
            target_usd_rate, target_metadata = get_crypto_rate(target, "USD")
            rate = source_usd_rate / target_usd_rate
            
            metadata = {
                "timestamp": datetime.datetime.now().isoformat(),
                "source_api": "CoinGecko",
                "rate": rate,
                "source_usd_rate": source_usd_rate,
                "target_usd_rate": target_usd_rate
            }
            
        # Case 2: Crypto to Fiat
        elif source_is_crypto and not target_is_crypto:
            if target == "USD":
                rate, metadata = get_crypto_rate(source, "USD")
            else:
                # Get crypto-to-USD rate, then USD-to-fiat rate
                crypto_usd_rate, crypto_metadata = get_crypto_rate(source, "USD")
                usd_fiat_rate, fiat_metadata = get_fiat_rate("USD", target)
                rate = crypto_usd_rate * usd_fiat_rate
                
                metadata = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source_api": f"CoinGecko + ExchangeRate-API",
                    "rate": rate,
                    "crypto_usd_rate": crypto_usd_rate,
                    "usd_fiat_rate": usd_fiat_rate
                }
        
        # Case 3: Fiat to Crypto
        elif not source_is_crypto and target_is_crypto:
            if source == "USD":
                # Just need to invert the crypto-to-USD rate
                usd_crypto_rate, crypto_metadata = get_crypto_rate(target, "USD")
                rate = 1 / usd_crypto_rate
                metadata = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source_api": "CoinGecko",
                    "rate": rate,
                    "usd_crypto_rate": usd_crypto_rate
                }
            else:
                # Convert fiat to USD, then USD to crypto
                fiat_usd_rate, fiat_metadata = get_fiat_rate(source, "USD")
                usd_crypto_rate, crypto_metadata = get_crypto_rate(target, "USD")
                rate = fiat_usd_rate * (1 / usd_crypto_rate)
                
                metadata = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source_api": f"ExchangeRate-API + CoinGecko",
                    "rate": rate,
                    "fiat_usd_rate": fiat_usd_rate,
                    "usd_crypto_rate": usd_crypto_rate
                }
        
        # Case 4: Fiat to Fiat
        else:
            rate, metadata = get_fiat_rate(source, target)
        
        # Cache the result
        cache_rate(source, target, rate, metadata)
        
        return rate, metadata
        
    except Exception as e:
        # Log the error
        print(f"Error getting exchange rate: {str(e)}")
        
        # Try to use cached rates if available
        cached_data = get_cached_rate(source, target, allow_expired=True)
        if cached_data:
            # Add warning to metadata
            cached_data["warning"] = "Using cached rate due to API error"
            return cached_data["rate"], cached_data
        
        # No cached data available
        raise RuntimeError(f"Failed to get exchange rate and no cached data available: {str(e)}")

def convert_currency(amount: float, source_currency: str, target_currency: str = "USD") -> Tuple[float, Dict[str, Any]]:
    """
    Convert an amount from one currency to another.
    
    Args:
        amount: The amount to convert
        source_currency: Source currency code
        target_currency: Target currency code (defaults to USD)
        
    Returns:
        Tuple containing:
            - float: The converted amount
            - Dict: Metadata about the conversion
    """
    rate, metadata = get_exchange_rate(source_currency, target_currency)
    converted_amount = amount * rate
    
    # Add conversion info to metadata
    metadata["converted_amount"] = converted_amount
    metadata["original_amount"] = amount
    
    return converted_amount, metadata

def get_historical_rates(source: str, target: str, days: int = 7) -> List[Dict[str, Any]]:
    """
    Get historical exchange rates between two currencies.
    
    Args:
        source: Source currency code
        target: Target currency code
        days: Number of days of historical data to retrieve
        
    Returns:
        List of dictionaries containing date and rate information
    """
    # Note: This is a placeholder implementation
    # In a real app, you would call historical API endpoints
    
    # For demo purposes, generate some sample data
    today = datetime.datetime.now()
    rate, _ = get_exchange_rate(source, target)
    
    # Generate random-ish historical data around the current rate
    import random
    historical_data = []
    
    for i in range(days):
        date = today - datetime.timedelta(days=i)
        # Vary the rate by up to ±5%
        variance = random.uniform(-0.05, 0.05)
        historical_rate = rate * (1 + variance)
        
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "rate": historical_rate
        })
    
    # Sort by date ascending
    historical_data.sort(key=lambda x: x["date"])
    
    return historical_data