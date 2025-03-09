import streamlit as st

def load_custom_styles():
    """
    Load custom CSS styles to enhance the UI appearance.
    Adds animations, custom colors, and improved visual elements.
    """
    st.markdown("""
    <style>
        /* Custom color variables */
        :root {
            --primary-color: #6236FF;
            --secondary-color: #05BFDB;
            --accent-color: #FF5757;
            --success-color: #00C897;
            --warning-color: #FFB100;
            --light-bg: #F5F7FF;
            --dark-bg: #192655;
            --card-border-radius: 12px;
            --transition-speed: 0.3s;
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header styling */
        h1, h2, h3 {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 50px;
            transition: all var(--transition-speed) ease;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 12px rgba(98, 54, 255, 0.15);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(98, 54, 255, 0.25);
        }
        
        /* Primary button styling */
        .stButton > button[data-baseweb="button"] {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }
        
        /* Card styling for containers */
        [data-testid="stExpander"] {
            border-radius: var(--card-border-radius);
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all var(--transition-speed) ease;
        }
        
        [data-testid="stExpander"]:hover {
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Metric styling */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--card-border-radius);
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all var(--transition-speed) ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            font-weight: 600;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        /* Input field styling */
        [data-testid="stNumberInput"] > div > div > input,
        .stSelectbox > div > div > input {
            border-radius: 50px;
            border: 2px solid rgba(98, 54, 255, 0.2);
            padding: 0.5rem 1rem;
            transition: all var(--transition-speed) ease;
        }
        
        [data-testid="stNumberInput"] > div > div > input:focus,
        .stSelectbox > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(98, 54, 255, 0.2);
        }
        
        /* Selectbox styling */
        .stSelectbox {
            transition: all var(--transition-speed) ease;
        }
        
        .stSelectbox:hover {
            transform: translateY(-2px);
        }
        
        /* Animation for success message */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .element-container [data-testid="stAlert"] {
            animation: fadeIn 0.5s ease-out forwards;
            border-radius: var(--card-border-radius);
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            border-radius: var(--card-border-radius);
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: rgba(245, 247, 255, 0.05);
            border-right: none;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        }
        
        /* Dark mode adjustments */
        .dark [data-testid="stSidebar"] {
            background-color: rgba(25, 38, 85, 0.1);
        }
        
        /* Tooltip styling */
        .stTooltipIcon {
            color: var(--primary-color);
        }
    </style>
    """, unsafe_allow_html=True)

def apply_animation(element_type, animation_name, duration=1, delay=0):
    """
    Apply CSS animation to specific elements.
    
    Args:
        element_type: CSS selector for the element
        animation_name: Name of the animation
        duration: Animation duration in seconds
        delay: Animation delay in seconds
    """
    st.markdown(f"""
    <style>
        @keyframes {animation_name} {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        
        {element_type} {{
            animation: {animation_name} {duration}s ease-out {delay}s forwards;
        }}
    </style>
    """, unsafe_allow_html=True)

def apply_currency_icons():
    """
    Add currency icons to the UI.
    """
    currency_icons = {
        # Fiat currencies
        "USD": "💵", "EUR": "💶", "GBP": "💷", "JPY": "💴",
        "AUD": "$", "CAD": "$", "CHF": "₣", "CNY": "¥",
        "SEK": "kr", "NZD": "$", "MXN": "$", "SGD": "$",
        "HKD": "$", "NOK": "kr", "KRW": "₩", "TRY": "₺",
        "INR": "₹", "BRL": "R$", "ZAR": "R",
        
        # Major cryptocurrencies
        "BTC": "₿", "ETH": "Ξ", "USDT": "₮", "BNB": "BNB",
        "USDC": "$", "XRP": "✕", "SOL": "◎", "ADA": "₳",
        "DOGE": "Ð", "DOT": "●", "LTC": "Ł", "XLM": "*",
        "LINK": "⬡", "BCH": "₿", "ZEC": "ⓩ", "BSV": "₿",
        "TRX": "♦", "ONT": "◊", "ETC": "ξ", "NEO": "NEO",
        "IOTA": "ι", "RED": "🔴", "AAVE": "Ⓐ", "UNI": "🦄",
        "SOLANA": "◎", "SUSHI": "🍣", "YFI": "⟠", "CRV": "⟠",
        "UNISWAP": "🦄", "BELT": "⟠", "KSM": "◆", "SOLANA-SOLV": "◎",
        "AAVE-SOLV": "Ⓐ", "UNISWAP-V2": "🦄", "AUCTIONS": "🔨",
        "DAPP": "Ð", "BTS": "●", "SKY": "☁", "ALGO": "Ⓐ"
    }
    
    return currency_icons

def get_currency_color(currency):
    """
    Return a color associated with a specific currency.
    
    Args:
        currency: Currency code
    
    Returns:
        Hex color code
    """
    # Check if dark mode is active to potentially adjust colors for better visibility
    is_dark_mode = False
    if "theme" in st.session_state and st.session_state.theme == "Dark":
        is_dark_mode = True
        
    # Adjust colors for better visibility in dark mode
    crypto_colors = {
        "BTC": "#F7931A",  # Bitcoin orange
        "ETH": "#627EEA",  # Ethereum blue
        "USDT": "#26A17B", # Tether green
        "BNB": "#F3BA2F",  # Binance yellow
        "USDC": "#2775CA", # USD Coin blue
        "XRP": "#718792" if is_dark_mode else "#23292F",  # XRP - lighter in dark mode
        "SOL": "#00FFA3",  # Solana green
        "ADA": "#4A7CFF" if is_dark_mode else "#0033AD",  # Cardano blue - lighter in dark mode
        "DOGE": "#F0D064" if is_dark_mode else "#C3A634", # Dogecoin gold - brighter in dark mode
        "DOT": "#FF6BB3" if is_dark_mode else "#E6007A",  # Polkadot pink - lighter in dark mode
        "LTC": "#BFBBBB" if is_dark_mode else "#345D9D",  # Litecoin silver/blue
        "XLM": "#CCCCCC" if is_dark_mode else "#08B5E5",  # Stellar blue
        "LINK": "#2A5ADA",  # Chainlink blue
        "BCH": "#8DC351",  # Bitcoin Cash green
        "ZEC": "#F4B728",  # Zcash yellow
        "BSV": "#EAB300",  # Bitcoin SV gold
        "TRX": "#FF0013",  # Tron red
        "ONT": "#32A4BE",  # Ontology blue
        "ETC": "#328332",  # Ethereum Classic green
        "NEO": "#58BF00",  # Neo green
        "IOTA": "#242424" if is_dark_mode else "#131F37",  # IOTA dark blue
        "RED": "#FF5555" if is_dark_mode else "#FF0000",   # Red - brighter in dark mode
        "AAVE": "#B6509E",  # Aave purple
        "UNI": "#FF007A",  # Uniswap pink
        "SOLANA": "#00FFA3",  # Solana green
        "SUSHI": "#FA52A0",  # Sushi pink
        "YFI": "#0074FA",  # Yearn Finance blue
        "CRV": "#3A3A3A" if is_dark_mode else "#101010",  # Curve dark
        "UNISWAP": "#FF007A",  # Uniswap pink
        "BELT": "#4C47F7",  # Belt blue
        "KSM": "#000000" if is_dark_mode else "#434343",  # Kusama black
        "SOLANA-SOLV": "#00FFA3",  # Solana green
        "AAVE-SOLV": "#B6509E",  # Aave purple
        "UNISWAP-V2": "#FF007A",  # Uniswap pink
        "AUCTIONS": "#FF8C00",  # Auctions orange
        "DAPP": "#5B58E2",  # Dapp blue
        "BTS": "#35BAEB",  # Bitshares blue
        "SKY": "#0072FF",  # Skycoin blue
        "ALGO": "#000000" if is_dark_mode else "#434343"  # Algorand black
    }
    
    fiat_colors = {
        "USD": "#A0D995" if is_dark_mode else "#85BB65",  # Dollar green - lighter in dark mode
        "EUR": "#4A7CFF" if is_dark_mode else "#0052B4",  # Euro blue - lighter in dark mode
        "GBP": "#FF5555" if is_dark_mode else "#CF142B",  # Pound red - brighter in dark mode
        "JPY": "#FF5555" if is_dark_mode else "#BC002D",  # Yen
        "AUD": "#A0D995" if is_dark_mode else "#85BB65",  # Australian Dollar green - lighter in dark mode
    }

    if currency in crypto_colors:
        return crypto_colors[currency]