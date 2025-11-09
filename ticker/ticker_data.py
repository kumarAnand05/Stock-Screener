import yfinance as yf
import os
import pandas as pd
from utilities.commons import get_project_dir
import datetime
import time

def get_scrip_data(scrip_name):
    """
    Returns the time series data for the given scrip name.
        - Checks local dir and updates it with latest data.
        - If local data is not present then fetches the entire data.
        - If data is already upto date, then loads from local dir.
    Args:
        scrip_name (str): The ticker symbol of the stock.
    """
    data_dir = os.path.join(get_project_dir(), "ticker", "scrip_data")
    os.makedirs(data_dir, exist_ok=True)
    
    scrip_data_file_path = os.path.join(data_dir, f"{scrip_name}.csv")

    if(os.path.exists(scrip_data_file_path)):

        print(f"[INFO] Local data found for {scrip_name}. Checking for updates...")

        stored_df = pd.read_csv(scrip_data_file_path).set_index('Unnamed: 0')
        latest_available_date = stored_df.iloc[0].index[0].split(' ')[0]
        latest_available_date = datetime.datetime.strptime(latest_available_date, "%Y-%m-%d").date()

        # Finding the number of days of missing data
        current_time = datetime.datetime.now().time()
        market_opening_time = datetime.time(9, 20)
        if current_time > market_opening_time:
            latest_trading_session = datetime.date.today()
        else:
            latest_trading_session = datetime.date.today() - datetime.timedelta(days=1)

        missing_days = (latest_trading_session - latest_available_date).days        # Days of missing data

        if missing_days > 0:
            missing_data = get_scrip_history(scrip_name, str(missing_days))
            
            # Retry fetching data if empty
            if len(missing_data.columns) == 0:
                time.sleep(5)
                missing_data = get_scrip_history(scrip_name, str(missing_days))

            # Removing existing data from collected missing data
            missed_trading_sessions = 0
            for days in range(missing_days):
                current_missing_days = (missing_data.iloc[0].index[days].date() - latest_available_date).days
                if current_missing_days > 0:
                    missed_trading_sessions += 1
                else:
                    break
            missing_data = missing_data.iloc[0:, :missed_trading_sessions]
            scrip_data = pd.concat([missing_data, stored_df], axis=1)

            return scrip_data
        else:
            return stored_df

    # Fetch all historical data if local file not found
    else:
        print(f"[INFO] No local data found for {scrip_name}. Fetching full data...")

        scrip_data = get_scrip_history(scrip_name, "max")
        if len(scrip_data.columns) == 0:
            time.sleep(5)
            scrip_data = get_scrip_history(scrip_name, "max")

        return scrip_data

    
def get_scrip_history(scrip_name, period):
    """
    Fetches the latest data for the given scrip name and period from yfinance.
    Args:
        scrip_name (str): The ticker symbol of the stock.
        period (str): The period for which to fetch data (e.g., '1d', '5d', '1mo', 'max').
    """

    scrip = yf.Ticker(f"{scrip_name}.NS" )     # Using .NS for NSE (National Stock Exchange of India) listed stocks

    # Colledcting historical market data
    if period == 'max':
        scrip_data = scrip.history(period='max').T.iloc[:, ::-1].round(2)
    else:
        period = get_period_value(period)
        scrip_data = scrip.history(period=f'{period}').T.iloc[:, ::-1].round(2) 
    
    # removing non-required data rows
    if "Dividends" in scrip_data.index:
        scrip_data = scrip_data.drop('Dividends')
    if "Stock Splits" in scrip_data.index:
        scrip_data = scrip_data.drop('Stock Splits')

    return scrip_data

def get_period_value(period):
    """
    Converts period in days to yfinance compatible string.
    Args:
        period (int): Number of days of data required.
    """
    days = int(period)
    period_map = {
        range(0, 4): '5d',
        range(4, 26): '1mo',
        range(26, 81): '3mo',
        range(81, 161): '6mo',
        range(161, 351): '1y',
        range(351, 701): '2y',
        range(701, 1751): '5y',
        range(1751, 2000): '10y',
    }
    
    for period_range, value in period_map.items():
        if days in period_range:
            return value
    return 'max'
