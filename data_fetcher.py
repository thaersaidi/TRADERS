import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
from iexfinance.stocks import Stock
import logging

# Setup logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# API Keys (Normally, you'd store these securely, or outside your version control system)
ALPHA_VANTAGE_API_KEY = '2XJY7S44R6Y5S31D'
IEX_CLOUD_API_KEY = 'sk_50267f0882f141c8b5af23390382fb94'

# Function to fetch data from Alpha Vantage
def fetch_data_alpha_vantage(symbol):
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        return data['4. close'].rename('Alpha_Close')
    except Exception as e:
        logging.error(f"Error fetching data from Alpha Vantage for symbol {symbol}: {e}")
        return pd.DataFrame()

# Function to fetch data from IEX Cloud
def fetch_data_iex_cloud(symbol):
    try:
        stock = Stock(symbol, token=IEX_CLOUD_API_KEY)
        df = stock.get_chart(range='1y')
        df = pd.DataFrame(df)
        # Check if 'date' exists in the df, otherwise look for other possible date column names
        date_column = None
        for possible_date_column in ['date', 'priceDate']:
            if possible_date_column in df.columns:
                date_column = possible_date_column
                break
        if date_column is None:
            raise ValueError("No recognizable date column found in IEX Cloud data")
        df.index = pd.to_datetime(df[date_column])
        return df['close'].rename('IEX_Close')
    except Exception as e:
        logging.error(f"Error fetching data from IEX Cloud for symbol {symbol}: {e}")
        return pd.DataFrame()

# Function to fetch data from Yahoo Finance
def fetch_data_yahoo_finance(symbol):
    try:
        data = yf.download(symbol, period='5y')
        return data['Close'].rename('YF_Close')
    except Exception as e:
        logging.error(f"Error fetching data from Yahoo Finance for symbol {symbol}: {e}")
        return pd.DataFrame()

def merge_stock_data(alpha_vantage_data, iex_cloud_data, yahoo_finance_data):
    try:
        # Combine the data using the 'date' as the joining key
        combined_data = pd.concat([alpha_vantage_data, iex_cloud_data, yahoo_finance_data], axis=1, join='outer')
        
        # Fill any missing values by using the forward-fill method to propagate the last valid observation forward
        combined_data.fillna(method='ffill', inplace=True)
        
        # If there are still missing values (e.g., at the beginning where there's no previous data), backfill them
        combined_data.fillna(method='bfill', inplace=True)
        
        # Ensure the date is the DataFrame index
        combined_data.index = pd.to_datetime(combined_data.index)
        
        return combined_data
    except Exception as e:
        logging.error(f"An error occurred while merging stock data: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    symbol = 'AAPL'  # Example stock symbol
    try:
        logging.info("Fetching data from Alpha Vantage...")
        alpha_vantage_data = fetch_data_alpha_vantage(symbol)
        logging.info("Fetching data from IEX Cloud...")
        iex_cloud_data = fetch_data_iex_cloud(symbol)
        logging.info("Fetching data from Yahoo Finance...")
        yahoo_finance_data = fetch_data_yahoo_finance(symbol)
        
        logging.info("Merging stock data from different sources...")
        combined_stock_data = merge_stock_data(alpha_vantage_data, iex_cloud_data, yahoo_finance_data)
        print(combined_stock_data.tail())  # Display the last few rows of the combined data
    except Exception as e:
        logging.error(f"An error occurred: {e}")