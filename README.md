# Enterprise Currency Converter

![Currency Converter](https://img.shields.io/badge/Currency-Converter-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)

A professional, real-time currency conversion platform supporting both fiat currencies and cryptocurrencies with an intuitive user interface and enterprise-grade features.

## 🌟 Features

- **Real-time Currency Conversion**: Convert between 30+ fiat currencies and 35+ cryptocurrencies
- **Multi-API Support**: Utilizes multiple data sources with automatic failover for high availability
- **Historical Rate Tracking**: View and analyze historical exchange rates with interactive charts
- **Conversion History**: Track and export your conversion history
- **Caching System**: Efficient caching mechanism to reduce API calls and improve performance
- **Responsive UI**: Clean, modern interface that works on desktop and mobile devices
- **PDF Export**: Generate and download conversion reports as PDF documents

## 📋 Supported Currencies

### Fiat Currencies
USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, HKD, NZD, SEK, KRW, SGD, NOK, MXN, INR, RUB, ZAR, TRY, BRL, TWD, DKK, PLN, THB, IDR, HUF, CZK, ILS, CLP, PHP, AED, SAR, MYR, PKR

### Cryptocurrencies
BTC, ETH, USDT, BNB, USDC, XRP, SOL, ADA, DOGE, DOT, LTC, XLM, LINK, BCH, ZEC, BSV, TRX, ONT, ETC, NEO, IOTA, RED, AAVE, UNI, SOLANA, SUSHI, YFI, CRV, UNISWAP, BELT, KSM, SOLANA-SOLV, AAVE-SOLV, UNISWAP-V2, DAPP, BTS, SKY, ALGO

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Git (optional)

### Setup

1. Clone the repository (or download the ZIP file)
   ```bash
   git clone https://github.com/yourusername/currency-converter.git
   cd currency-converter
   ```

2. Install the required dependencies
   ```bash
   pip install -r src/requirments.txt
   ```

## 🔧 Usage

1. Start the application
   ```bash
   cd src
   streamlit run main.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Select your source and target currencies, enter the amount, and click "Convert"

4. Explore additional features like historical rates and conversion history

## 🏗️ Project Structure

```
Currency_Convertor/
├── src/
│   ├── api/
│   │   ├── crypto_client.py   # Cryptocurrency API integration
│   │   └── fiat_client.py     # Fiat currency API integration
│   ├── core/
│   │   ├── cache.py           # Caching mechanism
│   │   └── converter.py       # Core conversion logic
│   ├── ui/
│   │   ├── dashboard.py       # Dashboard and visualization components
│   │   ├── styles.py          # UI styling
│   │   └── widgets.py         # UI components
│   ├── main.py                # Application entry point
│   └── requirments.txt        # Project dependencies
```

## 🔄 How It Works

The application uses a multi-tier architecture:

1. **API Layer**: Connects to external services like CoinGecko, CoinCap, and ExchangeRate-API to fetch real-time currency data
2. **Core Layer**: Handles conversion logic, caching, and data processing
3. **UI Layer**: Provides an intuitive interface built with Streamlit

The converter supports four types of conversions:
- Fiat to Fiat
- Crypto to Crypto
- Fiat to Crypto
- Crypto to Fiat

Each conversion type uses appropriate APIs and calculation methods to ensure accurate results.

## 🛠️ Technologies Used

- **Streamlit**: For the web interface
- **Pandas**: For data manipulation
- **Plotly**: For interactive charts
- **Requests**: For API communication
- **FPDF**: For CSV report generation

## 📊 API Sources

- **Fiat Currencies**: ExchangeRate-API, Open Exchange Rates, European Central Bank
- **Cryptocurrencies**: CoinGecko, CoinCap, CryptoCompare

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

If you have any questions or feedback, please connect with me on [LinkedIn](https://www.linkedin.com/in/ch-muhammad-tayyab/).
