from utilities.commons import get_project_dir
import datetime as dt
import os

def update_local_database(scrip_name, scrip_data):
    """
    Updates the local CSV file for the given scrip with the provided data.
    Args:
        scrip_name (str): The ticker symbol of the stock.
        scrip_data (pd.DataFrame): The time series data to be saved.
    """
    data_dir = os.path.join(get_project_dir(), "ticker", "scrip_data")
    os.makedirs(data_dir, exist_ok=True)
    scrip_data_file_path = os.path.join(data_dir, f"{scrip_name}.csv")
    
    try:
        latest_available_date = dt.datetime.strptime(scrip_data.iloc[0].index[0].split(" ")[0], "%Y-%m-%d").date()
    except AttributeError:
        latest_available_date = scrip_data.columns[0].date()

    current_date = dt.date.today()
    current_missing_days = (current_date - latest_available_date).days      # Days of missing data

    # Excluding current day data if market is still open
    if current_missing_days == 0:
        current_time = dt.datetime.now().time()
        market_close_time = dt.time(15, 40)
        if current_time < market_close_time:
            scrip_data = scrip_data.drop(columns=scrip_data.columns[0], axis=1)

    scrip_data = scrip_data.iloc[:, :2000].round(2)     # Trimming data to last 2000 trading sessions data
    scrip_data.to_csv(scrip_data_file_path)

    return
    