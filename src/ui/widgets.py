import streamlit as st
from typing import Tuple
from ui.styles import load_custom_styles, apply_currency_icons, get_currency_color, create_animated_container
from api.crypto_client import CRYPTO_MAPPING

def create_currency_inputs() -> Tuple[str, str]:
    """
    Create currency selection dropdowns with enhanced UI.
    
    Returns:
        Tuple of (source_currency, target_currency)
    """
    # Load custom styles
    load_custom_styles()
    
    # Get currency icons
    currency_icons = apply_currency_icons()
    
    # Define available currencies
    fiat_currencies = [
        "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", 
        "SEK", "NZD", "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", 
        "INR", "BRL", "ZAR", "PKR", "AED", "SAR", "MYR", "IDR",
        "PHP", "THB", "PLN", "ILS"
    ]
    
    # Use all cryptocurrencies from CRYPTO_MAPPING
    crypto_currencies = list(CRYPTO_MAPPING.keys())
    
    # Combine all currencies and sort
    all_currencies = sorted(fiat_currencies + crypto_currencies)
    
    # Create formatted options with icons
    formatted_options = [f"{currency_icons.get(curr, '💱')} {curr}" for curr in all_currencies]
    
    # Create a container with animation
    st.markdown("""<div class='currency-selector-container'></div>""", unsafe_allow_html=True)
    
    # Apply animation to the container
    st.markdown("""
    <style>
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .currency-selector-container {
        animation: slideIn 0.5s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create columns for side-by-side dropdowns with improved styling
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Add a subtle header with consistent color
        header_color = "#6236FF"
        st.markdown(f"""<div style='font-weight: 600; margin-bottom: 8px; color: {header_color};'>Source Currency</div>""", unsafe_allow_html=True)
        
        # Create the selectbox with formatted options
        source_index = all_currencies.index("USD") if "USD" in all_currencies else 0
        source_option = st.selectbox(
            "From",
            formatted_options,
            index=source_index,
            help="Select the source currency",
            label_visibility="collapsed"
        )
        
        # Extract the actual currency code (remove the icon)
        source_currency = all_currencies[formatted_options.index(source_option)]
        
        # Set text color and background color
        badge_bg_color = get_currency_color(source_currency)
        badge_text_color = "white"
        
        if source_currency in crypto_currencies:
            st.markdown(f"""<div style='display: inline-block; background-color: {badge_bg_color}; 
                        color: {badge_text_color}; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;'>Cryptocurrency</div>""", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='display: inline-block; background-color: {badge_bg_color}; 
                        color: {badge_text_color}; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;'>Fiat Currency</div>""", 
                        unsafe_allow_html=True)
    
    with col2:
        st.write("###")  # Spacer
        # Animated arrow with consistent color
        arrow_color = "#05BFDB"
        st.markdown(f"""
        <div style='text-align: center; font-size: 24px;'>        
            <div class='animated-arrow'>⟶</div>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.2); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.8; }}
        }}
        .animated-arrow {{
            animation: pulse 1.5s infinite;
            color: {arrow_color};
            display: inline-block;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    with col3:
        # Add a subtle header with consistent color
        header_color = "#6236FF"
        st.markdown(f"""<div style='font-weight: 600; margin-bottom: 8px; color: {header_color};'>Target Currency</div>""", unsafe_allow_html=True)
        
        # Default to BTC if source is USD, otherwise USD
        default_target = "BTC" if source_currency == "USD" else "USD"
        default_index = all_currencies.index(default_target) if default_target in all_currencies else 0
        
        # Create the selectbox with formatted options
        target_option = st.selectbox(
            "To",
            formatted_options,
            index=default_index,
            help="Select the target currency",
            label_visibility="collapsed"
        )
        
        # Extract the actual currency code (remove the icon)
        target_currency = all_currencies[formatted_options.index(target_option)]
        
        # Set text color and background color
        badge_bg_color = get_currency_color(target_currency)
        badge_text_color = "white"
        
        if target_currency in crypto_currencies:
            st.markdown(f"""<div style='display: inline-block; background-color: {badge_bg_color}; 
                        color: {badge_text_color}; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;'>Cryptocurrency</div>""", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='display: inline-block; background-color: {badge_bg_color}; 
                        color: {badge_text_color}; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;'>Fiat Currency</div>""", 
                        unsafe_allow_html=True)
    
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
    
    # Get currency icon
    currency_icons = apply_currency_icons()
    icon = currency_icons.get(source_currency, "💱")
    
    # Create a container with animation
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .amount-input-container {
        animation: fadeIn 0.5s ease-out 0.2s both;
    }
    </style>
    <div class="amount-input-container">
    </div>
    """, unsafe_allow_html=True)
    
    # Add a subtle header with currency icon
    color = get_currency_color(source_currency)
    st.markdown(f"""
    <div style='font-weight: 600; margin-bottom: 8px; color: {color}; display: flex; align-items: center;'>
        <span style='margin-right: 8px;'>{icon}</span> Amount to Convert
    </div>
    """, unsafe_allow_html=True)
    
    # Create a custom styled number input
    amount = st.number_input(
        f"Amount in {source_currency}",
        min_value=min_val,
        max_value=max_val,
        value=default_val,
        step=step,
        help=f"Enter the amount in {source_currency} to convert",
        label_visibility="collapsed"
    )
    
    # Display the current amount with currency in a nice format
    st.markdown(f"""
    <div style='background-color: rgba({','.join(str(int(c)) for c in tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))}, 0.1); 
         padding: 8px 16px; border-radius: 8px; margin-top: 5px; display: inline-block;'>
        <span style='font-weight: 600; color: {color};'>{amount:,.6f}</span> {source_currency}
    </div>
    """, unsafe_allow_html=True)
    
    return amount

def create_theme_toggle():
    """Create a light/dark theme toggle in the sidebar with enhanced UI."""
    st.markdown("""<div style='font-weight: 600; margin-bottom: 8px; color: #6236FF;'>App Theme</div>""", unsafe_allow_html=True)
    
    # Create custom radio buttons with icons
    col1, col2 = st.columns(2)
    
    # Get current theme from session state or default to light
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"
    
    # Custom styling for the theme selector
    st.markdown("""
    <style>
    .theme-option {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        border: 2px solid transparent;
    }
    .theme-option:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .theme-option.selected {
        border-color: #6236FF;
        background-color: rgba(98, 54, 255, 0.1);
    }
    .theme-icon {
        font-size: 24px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with col1:
        light_selected = st.session_state.theme == "Light"
        light_class = "selected" if light_selected else ""
        if st.button("☀️\nLight", key="light_theme", use_container_width=True):
            st.session_state.theme = "Light"
            # Use st.rerun() instead of the deprecated experimental_rerun()
            st.rerun()
    
    with col2:
        dark_selected = st.session_state.theme == "Dark"
        dark_class = "selected" if dark_selected else ""
        if st.button("🌙\nDark", key="dark_theme", use_container_width=True):
            st.session_state.theme = "Dark"
            # Use st.rerun() instead of the deprecated experimental_rerun()
            st.rerun()
    # Apply theme based on selection
    if st.session_state.theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #192655;
            color: #F5F7FF;
        }
        /* Dark mode adjustments for text and components */
        .stApp p, .stApp div {
            color: #F5F7FF;
        }
        /* Dark mode for dataframes and other components */
        .stApp [data-testid="stDataFrame"] {
            background-color: rgba(255, 255, 255, 0.05);
        }
        /* Dark mode for inputs */
        .stApp [data-testid="stNumberInput"] > div > div > input,
        .stApp .stSelectbox > div > div > input {
            background-color: rgba(255, 255, 255, 0.1);
            color: #F5F7FF;
        }
        /* Dark mode for buttons */
        .stApp .stButton > button {
            background-color: rgba(98, 54, 255, 0.8);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Show current theme with a nice badge
    st.markdown(f"""
    <div style='display: inline-block; background-color: #6236FF; color: white; 
    padding: 4px 12px; border-radius: 50px; font-size: 0.8rem; margin-top: 10px;'>
    {st.session_state.theme} Theme Active</div>
    """, unsafe_allow_html=True)