# core/cache.py
import datetime
import time
from typing import Dict, Any, Optional
import streamlit as st

# Cache TTL in seconds (30 minutes for regular cache, 24 hours for emergency fallback)
CACHE_TTL = 1800  # 30 minutes
EMERGENCY_CACHE_TTL = 86400  # 24 hours

def initialize_cache():
    """Initialize the rate cache in Streamlit session state if it doesn't exist."""
    if "rate_cache" not in st.session_state:
        st.session_state.rate_cache = {}

def get_cache_key(source: str, target: str) -> str:
    """Generate a cache key for a currency pair."""
    return f"{source.upper()}_{target.upper()}"

def cache_rate(source: str, target: str, rate: float, metadata: Dict[str, Any]):
    """
    Cache an exchange rate with metadata.
    
    Args:
        source: Source currency code
        target: Target currency code
        rate: Exchange rate
        metadata: Rate metadata
    """
    cache_key = get_cache_key(source, target)
    
    # Store in cache with expiration timestamp
    cache_entry = {
        "rate": rate,
        "metadata": metadata,
        "expires_at": time.time() + CACHE_TTL,
        "created_at": time.time()
    }
    
    st.session_state.rate_cache[cache_key] = cache_entry
    
    # Also cache the inverse rate
    inverse_cache_key = get_cache_key(target, source)
    inverse_rate = 1 / rate
    
    # Create new metadata for inverse
    inverse_metadata = metadata.copy()
    inverse_metadata["rate"] = inverse_rate
    inverse_metadata["is_inverse"] = True
    
    inverse_cache_entry = {
        "rate": inverse_rate,
        "metadata": inverse_metadata,
        "expires_at": time.time() + CACHE_TTL,
        "created_at": time.time()
    }
    
    st.session_state.rate_cache[inverse_cache_key] = inverse_cache_entry

def get_cached_rate(source: str, target: str, allow_expired: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get a cached exchange rate if available and not expired.
    
    Args:
        source: Source currency code
        target: Target currency code
        allow_expired: Whether to return expired cache entries
        
    Returns:
        Dict containing rate and metadata, or None if not in cache or expired
    """
    cache_key = get_cache_key(source, target)
    
    if cache_key in st.session_state.rate_cache:
        cache_entry = st.session_state.rate_cache[cache_key]
        
        # Check if cache entry is expired
        if time.time() <= cache_entry["expires_at"] or allow_expired:
            # Copy metadata and add cache information
            result = cache_entry["metadata"].copy()
            result["rate"] = cache_entry["rate"]
            result["cached"] = True
            result["cache_age"] = time.time() - cache_entry["created_at"]
            
            if allow_expired and time.time() > cache_entry["expires_at"]:
                result["cache_expired"] = True
                result["seconds_expired"] = time.time() - cache_entry["expires_at"]
            
            return result
    
    return None

@st.cache_data(ttl=CACHE_TTL)
def cached_api_request(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make an API request with built-in caching.
    
    Args:
        url: API endpoint URL
        params: Query parameters
        
    Returns:
        API response as dictionary
    """
    import requests
    
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    
    return response.json()