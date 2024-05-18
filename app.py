import argparse
import sys
import logging
from data_fetcher import fetch_data_alpha_vantage, fetch_data_iex_cloud, fetch_data_yahoo_finance, merge_stock_data
from signal_generator import generate_signals
from trend_analysis import fetch_trending_topics, correlate_insights_with_stock_data
from prediction_model import fetch_preprocessed_data, prepare_data, train_model, predict_future_prices
from decision_maker import make_investment_decisions

def setup_logging():
    # Configure logging to file and console with timestamp and log level
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='traders_app.log',
                        filemode='a')  # Append mode
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def parse_arguments():
    parser = argparse.ArgumentParser(description='TRADERS App Stock Analysis and Decision Making')
    parser.add_argument('symbol', type=str, help='Stock symbol to analyze')
    return parser.parse_args()

def main():
    setup_logging()
    
    args = parse_arguments()
    symbol = args.symbol
    kw_list = [symbol]
    
    try:
        logging.info(f'Starting analysis for {symbol}')
        print(f'Starting analysis for {symbol}...')
        
        # Fetch stock data
        logging.info('Fetching stock data...')
        alpha_vantage_data = fetch_data_alpha_vantage(symbol)
        iex_cloud_data = fetch_data_iex_cloud(symbol)
        yahoo_finance_data = fetch_data_yahoo_finance(symbol)
        print('Stock data fetched from multiple sources.')
        
        # Merge stock data
        logging.info('Merging stock data...')
        combined_stock_data = merge_stock_data(alpha_vantage_data, iex_cloud_data, yahoo_finance_data)
        print('Stock data merged successfully.')
        
        # Generate trading signals
        logging.info('Generating trading signals...')
        signals = generate_signals(combined_stock_data)
        print(f'Trading signals generated: {signals}')
        
        # Trend analysis and sentiment analysis
        logging.info('Analyzing trends and sentiment...')
        trending_topics = fetch_trending_topics(kw_list, timeframe='now 1-d')
        print(f'Trending topics fetched: {trending_topics}')
        
        # # Sentiment analysis
        # if 'description' in trending_topics.columns:
        #     sentiment_scores = [analyze_sentiment(topic) for topic in trending_topics['description']]
        #     print(f'Sentiment scores calculated: {sentiment_scores}')
        # else:
        #     print('No suitable column found for sentiment analysis.')
        
        trends = correlate_insights_with_stock_data(trending_topics, combined_stock_data, kw_list)
        print(f'Correlated insights: {trends}')
        
        # Prediction model
        logging.info('Predicting future stock prices...')
        preprocessed_data = fetch_preprocessed_data()
        X, y = prepare_data(combined_stock_data)
        model = train_model(X, y)
        future_data = preprocessed_data  # Placeholder for actual future data
        predictions = predict_future_prices(model, future_data)
        print(f'Future stock prices predicted: {predictions}')
        
        # Make investment decisions
        logging.info('Making investment decisions...')
        decision = make_investment_decisions(signals, trends, predictions)
        print(f'Investment decisions made: {decision}')
        
    except Exception as e:
        logging.error(f'An error occurred: {e}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
