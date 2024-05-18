import logging
import numpy as np
import pandas as pd
from pytrends.request import TrendReq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def fetch_trending_topics(kw_list, timeframe='now 1-d', geo='US', gprop=''):
    """
    Fetch trending topics from Google Trends.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo, gprop=gprop)
        data = pytrends.interest_over_time()
        if data.empty:
            logging.info("No trending data found.")
            return pd.DataFrame()
        logging.info(f"Fetched trending topics data for keywords: {kw_list}")
        return data
    except Exception as e:
        logging.error("An error occurred while fetching trending topics", exc_info=True)
        return pd.DataFrame()


def correlate_insights_with_stock_data(trending_topics, stock_data, kw_list):
    try:
        if trending_topics.empty:
            logging.info("No trending topics data available for correlation.")
            return pd.DataFrame(), None

        if stock_data.empty:
            logging.info("Stock data is empty.")
            return pd.DataFrame(), None

        keyword = kw_list[0] if kw_list[0] in trending_topics.columns else None
        if keyword is None:
            logging.error(f"Keyword {kw_list[0]} not found in trending topics.")
            return pd.DataFrame(), None

        if not all([isinstance(df.index, pd.DatetimeIndex) for df in [trending_topics, stock_data]]):
            logging.error("One or both dataframes are not indexed by date.")
            return pd.DataFrame(), None

        # Ensuring both dataframes cover the same time period
        min_date = max(trending_topics.index.min(), stock_data.index.min())
        max_date = min(trending_topics.index.max(), stock_data.index.max())

        trending_topics = trending_topics.loc[min_date:max_date].resample('1T').asfreq().fillna(method='ffill')
        stock_data = stock_data.loc[min_date:max_date].resample('1T').asfreq().fillna(method='ffill')

        # Calculate the average stock price
        stock_data['Average_Price'] = stock_data.mean(axis=1)

        correlated_data = pd.DataFrame({
            'Search Interest': trending_topics[keyword],
            'Average Stock Price': stock_data['Average_Price']
        }, index=trending_topics.index)

        # Calculate correlation
        correlation_result = correlated_data['Search Interest'].corr(correlated_data['Average Stock Price'])

        logging.info(f"Correlated insights with stock data. Correlation is {correlation_result}")
        
        return correlated_data, correlation_result

    except Exception as e:
        logging.error("An error occurred while correlating insights with stock data", exc_info=True)
        return pd.DataFrame(), None


# Example usage
if __name__ == '__main__':
    kw_list = ['AAPL']
    trending_topics = fetch_trending_topics(kw_list, timeframe='now 1-d', geo='US')
    print("Trending Topics:", trending_topics)

    # Placeholder for fetching stock data, replace with actual method to fetch stock data
    stock_data = pd.DataFrame({
        'price': [100, 102, 105, 107, 109],  # Simulated stock prices, use real data instead
    }, index=pd.date_range(start='2023-10-01', periods=5, freq='T'))

    insights = correlate_insights_with_stock_data(trending_topics, stock_data, kw_list)
    print(insights)