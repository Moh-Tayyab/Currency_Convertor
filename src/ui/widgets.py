import streamlit as st
from typing import Tuple

def create_currency_inputs() -> Tuple[str, str]:
    """
    Create currency selection dropdowns.
    
    Returns:
        Tuple of (source_currency, target_currency)
    """
    # Define available currencies
    fiat_currencies = [
        "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", 
        "SEK", "NZD", "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", 
        "INR", "BRL", "ZAR"
    ]
    
    crypto_currencies = [
        "BTC", "ETH", "USDT", "BNB", "USDC", "XRP", "SOL", "ADA", "DOGE", "DOT"
    ]
    
    # Combine all currencies and sort
    all_currencies = sorted(fiat_currencies + crypto_currencies)
    
    # Create columns for side-by-side dropdowns
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        source_currency = st.selectbox(
            "From Currency",
            all_currencies,
            index=all_currencies.index("USD") if "USD" in all_currencies else 0,
            help="Select the source currency"
        )
        
        # Show currency type
        if source_currency in crypto_currencies:
            st.caption("Cryptocurrency")
        else:
            st.caption("Fiat Currency")
    
    with col2:
        st.write("###")  # Spacer
        st.write("👉")  # Arrow icon
    
    with col3:
        # Default to BTC if source is USD, otherwise USD
        default_target = "BTC" if source_currency == "USD" else "USD"
        default_index = all_currencies.index(default_target) if default_target in all_currencies else 0
        
        target_currency = st.selectbox(
            "To Currency",
            all_currencies,
            index=default_index,
            help="Select the target currency"
        )
        
        # Show currency type
        if target_currency in crypto_currencies:
            st.caption("Cryptocurrency")
        else:
            st.caption("Fiat Currency")
    
    return source_currency, target_currency

def create_amount_input(source_currency: str) -> float:
    """
    Create an amount input field with validation.
    
    Args:
        source_currency: The selected source currency
        
    Returns:
        float: The input amount
    """
    # Set reasonable min/max based on currency type
    if source_currency in ["BTC", "ETH"]:
        # For high-value cryptos, allow smaller amounts
        min_val = 0.00001
        max_val = 1000.0
        default_val = 0.1
        step = 0.01
    elif source_currency in ["USDT", "USDC", "BNB"]:
        min_val = 0.01
        max_val = 10000.0
        default_val = 100.0
        step = 1.0
    else:
        # For fiat currencies
        min_val = 0.01
        max_val = 1000000.0
        default_val = 100.0
        step = 1.0
    
    amount = st.number_input(
        f"Amount ({source_currency})",
        min_value=min_val,
        max_value=max_val,
        value=default_val,
        step=step,
        help=f"Enter the amount in {source_currency} to convert"
    )
    
    return amount

def create_theme_toggle():
    """Create a light/dark theme toggle in the sidebar."""
    theme_options = ["Light", "Dark"]
    selected_theme = st.radio("Theme", theme_options, horizontal=True)
    
    # In a real app, you would use Streamlit's theming capabilities
    # For now, we'll just show a message
    st.caption(f"{selected_theme} theme selected")