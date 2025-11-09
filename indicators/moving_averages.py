import pandas as pd

def get_simple_moving_average(scrip_data, periods):
    """
    Calculate the Simple Moving Average (SMA) for a given period.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    period (int): The period over which to calculate the SMA.

    Returns:
    float: The Simple Moving Average value on the specified period value.
    """
    sma_values = []
    close_prices = scrip_data.loc['Close'][-(max(periods)+1):]
    
    for period in periods:
        sma_values.append(round(sum(close_prices[-period:]) / period, 2))    
    
    return sma_values

def add_all_exponential_moving_averages(scrip_data, periods):
    """
    Calculate and add Exponential Moving Averages (EMAs) for given periods to the scrip_data DataFrame.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    periods (list): List of periods over which to calculate the EMAs.

    Returns:
    pd.DataFrame: The original DataFrame with additional columns for each EMA.
    """
    periods = sorted(periods)
    ema_rows = []
    sma_values = get_simple_moving_average(scrip_data, periods)

    for period in periods:
        ema_rows.append(f"EMA{period}")
        if f"EMA{period}" not in scrip_data.index:
            scrip_data = pd.concat([scrip_data, pd.Series(dtype='float64', name=f'EMA{period}', index=scrip_data.columns).to_frame().T])
            scrip_data.loc[f"EMA{period}"].iloc[len(scrip_data.loc['Close'])-min(periods)] =   sma_values[periods.index(period)]

    for i in range(len(scrip_data.loc['Close'])-min(periods)-1, -1, -1):
        for period in periods:
            if len(scrip_data.loc['Close'])-i >= period:
                add_ema_value(scrip_data, period, i)
    
    return scrip_data

     
def add_ema_value(scrip_data, period, index):
    """
    Calculate the Exponential Moving Average (EMA) for a given period at a specific index.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    period (int): The period over which to calculate the EMA.
    index (int): The index at which to calculate the EMA.
    
    Returns:
    None: The function updates the scrip_data DataFrame in place.
    """
    smoothing_factor = 2 / (period + 1)
    previous_ema = scrip_data.loc[f"EMA{period}"].iloc[index + 1]
    close_price = scrip_data.loc['Close'].iloc[index]

    scrip_data.loc[f"EMA{period}"].iloc[index] = round((close_price * smoothing_factor) + (previous_ema * (1 - smoothing_factor)), 2 )

    return


def update_exponential_moving_averages(scrip_data, periods, missed_trading_sessions):
    """
    Update the existing Exponential Moving Averages (EMAs) for given periods in the scrip_data DataFrame
    for the missed trading sessions.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    periods (list): List of periods over which to update the EMAs.
    missed_trading_sessions (int): Number of missed trading sessions to account for.

    Returns:
    None: The function updates the scrip_data DataFrame in place.
    """
    periods = sorted(periods)
    unavailable_ema_periods = []

    sma_values = get_simple_moving_average(scrip_data, periods)

    for i in range(missed_trading_sessions - 1, -1, -1):
        for period in periods:
            if f"EMA{period}" not in scrip_data.index:
                unavailable_ema_periods.append(period)
                continue
            else:
                add_ema_value(scrip_data, period, i)
    
    add_all_exponential_moving_averages(scrip_data, unavailable_ema_periods)
    return