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
        
        /* Main container styling with gradient background */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Add a more modern gradient background to the entire app */
        .stApp {
            background: linear-gradient(135deg, var(--light-bg) 0%, #E2E8FF 70%, #D4E2FF 100%);
            background-attachment: fixed;
            background-size: cover;
        }
        
        /* Header styling with enhanced gradient */
        h1, h2, h3 {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* Button styling with improved hover effects */
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
        
        /* Primary button styling with gradient */
        .stButton > button[data-baseweb="button"] {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }
        
        /* Card styling for containers with glass morphism effect */
        [data-testid="stExpander"] {
            border-radius: var(--card-border-radius);
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all var(--transition-speed) ease;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
        }
        
        [data-testid="stExpander"]:hover {
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Metric styling with glass morphism */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: var(--card-border-radius);
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all var(--transition-speed) ease;
            border-left: 4px solid var(--primary-color);
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
        
        /* Input field styling with improved focus states */
        [data-testid="stNumberInput"] > div > div > input,
        .stSelectbox > div > div > input {
            border-radius: 50px;
            border: 2px solid rgba(98, 54, 255, 0.2);
            padding: 0.5rem 1rem;
            transition: all var(--transition-speed) ease;
            background: rgba(255, 255, 255, 0.8);
        }
        
        [data-testid="stNumberInput"] > div > div > input:focus,
        .stSelectbox > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(98, 54, 255, 0.2);
            background: white;
        }
        
        /* Selectbox styling with hover effect */
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
            backdrop-filter: blur(10px);
        }
        
        /* Dataframe styling with glass morphism */
        [data-testid="stDataFrame"] {
            border-radius: var(--card-border-radius);
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: rgba(245, 247, 255, 0.8);
            backdrop-filter: blur(10px);
            border-right: none;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        }
        
        /* Tooltip styling */
        .stTooltipIcon {
            color: var(--primary-color);
        }
        
        /* Currency card styling */
        .currency-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: var(--card-border-radius);
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all var(--transition-speed) ease;
            margin-bottom: 1rem;
            border-left: 4px solid var(--primary-color);
        }
        
        .currency-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
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
        "INR": "₹", "BRL": "R$", "ZAR": "R", "PKR": "₨",
        "AED": "د.إ", "SAR": "﷼", "MYR": "RM", "IDR": "Rp",
        "PHP": "₱", "THB": "฿", "PLN": "zł", "ILS": "₪",
        
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
        "DAPP": "Ð", "BTS": "●", "SKY": "☁", "ALGO": "Ⓐ",
        "MATIC": "◆", "AVAX": "🔺", "FTM": "👻", "ATOM": "⚛",
        "NEAR": "Ⓝ", "FIL": "⨎", "VET": "V", "XTZ": "ꜩ",
        "THETA": "θ", "EOS": "ε", "CAKE": "🍰", "XMR": "ɱ",
        "LUNA": "🌙", "HBAR": "ℏ", "EGLD": "⚡", "ICP": "∞",
        "SHIB": "🐕", "AXS": "🎮", "MANA": "Ⓜ", "SAND": "⏳"
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
    # Use consistent colors without dark mode adjustments
    crypto_colors = {
        "BTC": "#F7931A",  # Bitcoin orange
        "ETH": "#627EEA",  # Ethereum blue
        "USDT": "#26A17B", # Tether green
        "BNB": "#F3BA2F",  # Binance yellow
        "USDC": "#2775CA", # USD Coin blue
        "XRP": "#23292F",  # XRP
        "SOL": "#00FFA3",  # Solana green
        "ADA": "#0033AD",  # Cardano blue
        "DOGE": "#C3A634", # Dogecoin gold
        "DOT": "#E6007A",  # Polkadot pink
        "LTC": "#345D9D",  # Litecoin silver/blue
        "XLM": "#08B5E5",  # Stellar blue
        "LINK": "#2A5ADA",  # Chainlink blue
        "BCH": "#8DC351",  # Bitcoin Cash green
        "ZEC": "#F4B728",  # Zcash yellow
        "BSV": "#EAB300",  # Bitcoin SV gold
        "TRX": "#FF0013",  # Tron red
        "ONT": "#32A4BE",  # Ontology blue
        "ETC": "#328332",  # Ethereum Classic green
        "NEO": "#58BF00",  # Neo green
        "IOTA": "#131F37",  # IOTA dark blue
        "MATIC": "#8247E5", # Polygon purple
        "AVAX": "#E84142",  # Avalanche red
        "FTM": "#1969FF",   # Fantom blue
        "ATOM": "#2E3148",  # Cosmos dark blue
        "NEAR": "#000000",  # NEAR black
        "FIL": "#0090FF",   # Filecoin blue
        "VET": "#15BDFF",   # VeChain blue
        "XTZ": "#A6E000",   # Tezos green
        "THETA": "#2AB8E6", # Theta blue
        "EOS": "#000000",   # EOS black
        "CAKE": "#D1884F",  # PancakeSwap brown
        "XMR": "#FF6600",   # Monero orange
        "LUNA": "#172852",  # Terra blue
        "HBAR": "#00BAFF",  # Hedera blue
        "EGLD": "#1D40FF",  # Elrond blue
        "ICP": "#29ABE2",   # Internet Computer blue
        "SHIB": "#FFA409",  # Shiba Inu gold
        "AXS": "#0055D5",   # Axie Infinity blue
        "MANA": "#FF2D55",  # Decentraland red
        "SAND": "#00AEFF",   # The Sandbox blue
        "RED": "#FF0000",   # Red
        "AAVE": "#B6509E",  # Aave purple
        "UNI": "#FF007A",  # Uniswap pink
        "SOLANA": "#00FFA3",  # Solana green
        "SUSHI": "#FA52A0",  # Sushi pink
        "YFI": "#0074FA",  # Yearn Finance blue
        "CRV": "#101010",  # Curve dark
        "UNISWAP": "#FF007A",  # Uniswap pink
        "BELT": "#4C47F7",  # Belt blue
        "KSM": "#434343",  # Kusama black
        "SOLANA-SOLV": "#00FFA3",  # Solana green
        "AAVE-SOLV": "#B6509E",  # Aave purple
        "UNISWAP-V2": "#FF007A",  # Uniswap pink
        "AUCTIONS": "#FF8C00",  # Auctions orange
        "DAPP": "#5B58E2",  # Dapp blue
        "BTS": "#35BAEB",  # Bitshares blue
        "SKY": "#0072FF",  # Skycoin blue
        "ALGO": "#434343",  # Algorand black
        "PKR": "#01411C"    # Pakistani Rupee green
    }
    
    fiat_colors = {
        "USD": "#85BB65",  # Dollar green
        "EUR": "#0052B4",  # Euro blue
        "GBP": "#CF142B",  # Pound red
        "JPY": "#BC002D",  # Yen
        "AUD": "#85BB65",  # Australian Dollar green
        "PKR": "#01411C",  # Pakistani Rupee green
        "INR": "#FF9933",  # Indian Rupee saffron
        "CNY": "#DE2910",  # Chinese Yuan red
        "CAD": "#FF0000",  # Canadian Dollar red
        "BRL": "#009c3b",  # Brazilian Real green
        "ZAR": "#007A4D",  # South African Rand green
        "AED": "#FF0000",  # UAE Dirham red
        "SAR": "#006C35",  # Saudi Riyal green
        "MYR": "#0032A0",  # Malaysian Ringgit blue
        "IDR": "#FF0000",  # Indonesian Rupiah red
        "PHP": "#0038A8",  # Philippine Peso blue
        "THB": "#00247D",  # Thai Baht blue
        "PLN": "#DC143C",  # Polish Zloty red
        "ILS": "#0038B8"   # Israeli Shekel blue
    }

    if currency in crypto_colors:
        return crypto_colors[currency]
    elif currency in fiat_colors:
        return fiat_colors[currency]
    else:
        # Default color for unknown currencies
        return "#6236FF"  # Primary color from the app
        
def create_animated_container(container_class, animation_name="fadeIn", duration=0.5, delay=0):
    """
    Create an animated container with custom animation settings.
    
    Args:
        container_class: CSS class name for the container
        animation_name: Name of the animation (default: fadeIn)
        duration: Animation duration in seconds (default: 0.5)
        delay: Animation delay in seconds (default: 0)
    """
    # Define animation keyframes based on animation name
    if animation_name == "fadeIn":
        keyframes = """
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        """
    elif animation_name == "slideIn":
        keyframes = """
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        """
    elif animation_name == "zoomIn":
        keyframes = """
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        """
    elif animation_name == "pulse":
        keyframes = """
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        """
    else:  # Default fadeIn
        keyframes = """
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        """
    
    # Create the CSS with animation
    st.markdown(f"""
    <style>
    @keyframes {animation_name} {{
        {keyframes}
    }}
    
    .{container_class} {{
        animation: {animation_name} {duration}s ease-out {delay}s forwards;
    }}
    </style>
    <div class="{container_class}"></div>
    """, unsafe_allow_html=True)