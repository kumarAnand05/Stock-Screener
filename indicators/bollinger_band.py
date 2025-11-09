import numpy as np
import statistics as stats

def get_bollinger_bands(scrip_data, period=20):
    """
    Calculate Bollinger Bands for the given scrip_data DataFrame.
    
    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    period (int): The number of periods to use for the moving average.
        
    Returns:
    pd.DataFrame: DataFrame with added columns for the middle, upper, and lower Bollinger Bands.
    """
    close_prices = scrip_data.loc['Close'][::-1]
    rolling_mean = close_prices.rolling(window=period).mean()
    rolling_std = close_prices.rolling(window=period).apply(lambda cp: stats.stdev(cp))

    # calculating upper and lower bollinger bands
    upper_band = np.array((rolling_mean + (2 * rolling_std)))[::-1]
    lower_band = np.array(rolling_mean - (2 * rolling_std))[::-1]
    scrip_data.loc['Upper_bollinger'] = upper_band
    scrip_data.loc['Lower_bollinger'] = lower_band
    
    return scrip_data