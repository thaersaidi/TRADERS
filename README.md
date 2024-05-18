# TRADERS

TRADERS is a Python application designed to enhance stock market analysis and trading strategies by fetching, analyzing, and combining stock data from multiple financial data providers including Alpha Vantage, IEX Cloud, and Yahoo Finance. It incorporates advanced data manipulation and analysis techniques using pandas and NumPy, alongside predictive analytics to forecast stock movements.

## Overview

The application is built on Python, utilizing several libraries for data fetching (`requests`, `alpha_vantage`, `yfinance`, `iexfinance`), data manipulation (`pandas`, `numpy`), and sentiment analysis (`nltk`). The project structure includes scripts for data fetching (`data_fetcher.py`), signal generation (`signal_generator.py`), and trend analysis (`trend_analysis.py`), alongside a virtual environment setup for dependency management.

## Features

- Fetch real-time stock data from Alpha Vantage, IEX Cloud, and Yahoo Finance.
- Analyze stock data to generate trading signals based on moving averages.
- Correlate insights from web-scraped trending topics with stock market data.
- Implement predictive analytics to forecast stock movements based on correlated data.
- Automate investment decisions using analyzed data and generated signals.

## Getting started

### Requirements

- Python 3.11.8
- Alpha Vantage API key
- IEX Cloud API key
- Internet connection for data fetching

### Quickstart

1. Clone the repository to your local machine.
2. Navigate to the project directory and activate the virtual environment:
   - On Windows: `traders_env\Scripts\activate.bat`
   - On Unix or MacOS: `source traders_env/bin/activate`
3. Install the required Python packages: `pip install -r requirements.txt`
4. Run the main script with a stock symbol as an argument: `python app.py AAPL`

### License

Copyright (c) 2024.