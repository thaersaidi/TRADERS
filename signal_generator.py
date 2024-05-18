import pandas as pd
import numpy as np

def generate_signals(data):
    """
    Generate buy/sell signals based on short and long moving averages.
    :param data: DataFrame with stock price data.
    :return: DataFrame with signals and moving averages.
    """
    try:
        # Define window lengths for short and long moving averages
        short_window = 40
        long_window = 100

        # Initialize the DataFrame to store the signals
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0  # Default to no signal

        # Calculate short and long moving averages
        signals['short_mavg'] = data['Alpha_Close'].rolling(window=short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Alpha_Close'].rolling(window=long_window, min_periods=1, center=False).mean()

        # Generate the signals based on moving average crossovers
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        
        # Generate trading orders (1 = buy, -1 = sell, 0 = hold)
        signals['positions'] = signals['signal'].diff()

        print("Signal generation completed successfully.")
        return signals
    except Exception as e:
        print(f"An error occurred during signal generation: {e}")
        raise