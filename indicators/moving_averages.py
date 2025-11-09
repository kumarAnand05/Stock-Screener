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
            row_index = f"EMA{period}"
            col_index = len(scrip_data.loc['Close']) - min(periods)
            scrip_data.loc[row_index, col_index] = sma_values[periods.index(period)]

    for period in periods:
        add_ema_value(scrip_data, period, len(scrip_data.columns) - min(periods))
    
    return scrip_data

     
def add_ema_value(scrip_data, period, start_index):
    """
    Calculate the Exponential Moving Average (EMA) for a given period at a specific index.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    period (int): The period over which to calculate the EMA.
    index (int): The index at which to calculate the EMA.
    
    Returns:
    pd.DataFrame: The DataFrame with the EMA value added at the specified index.
    """
    ema_values = scrip_data.loc[f"EMA{period}"].to_numpy().copy()
    close_prices = ema_values = scrip_data.loc['Close'].to_numpy().copy()
    smoothing_factor = 2 / (period + 1)
    
    for i in range( start_index- 1, -1, -1):
        if len(close_prices) - i >= period:
            previous_ema = ema_values[i + 1]
            close_price = close_prices[i]
            ema_values[i] = round((close_price * smoothing_factor) + (previous_ema * (1 -smoothing_factor)), 2)

    scrip_data.loc[f"EMA{period}"] = ema_values

    return scrip_data


def update_exponential_moving_averages(scrip_data, periods, missed_trading_sessions):
    """
    Update the existing Exponential Moving Averages (EMAs) for given periods in the scrip_data DataFrame
    for the missed trading sessions.

    Parameters:
    scrip_data (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    periods (list): List of periods over which to update the EMAs.
    missed_trading_sessions (int): Number of missed trading sessions to account for.

    Returns:
    pd.DataFrame: The updated DataFrame with recalculated EMAs.
    """
    periods = sorted(periods)
    unavailable_ema_periods = []

    sma_values = get_simple_moving_average(scrip_data, periods)
    
    for period in periods:
        if f"EMA{period}" not in scrip_data.index:
            unavailable_ema_periods.append(period)
            continue
        else:
            scrip_data = add_ema_value(scrip_data, period, missed_trading_sessions)
    if len(unavailable_ema_periods)>0:
        scrip_data = add_all_exponential_moving_averages(scrip_data, unavailable_ema_periods)
    return scrip_data