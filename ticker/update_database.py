from utilities.commons import get_formatted_date
import datetime as dt

def update_local_database(scrip_name, scrip_data):
    """
    Updates the local CSV file for the given scrip with the provided data.
    Args:
        scrip_name (str): The ticker symbol of the stock.
        scrip_data (pd.DataFrame): The time series data to be saved.
    """
    scrip_data_file_path = f"ticker/scrip_data/{scrip_name}.csv"
    
    try:
        latest_available_date = get_formatted_date(scrip_data.iloc[0].index[0].split(' ')[0])
    except AttributeError:
        latest_available_date = scrip_data.columns[0].date()

    current_date = dt.date.today()
    current_missing_days = (current_date - latest_available_date).days      # Days of missing data

    # Excluding current day data if market is still open
    if current_missing_days == 0:
        current_time = dt.datetime.now().time()
        market_close_time = dt.time(15, 40)
        if current_time < market_close_time:
            data = data.drop(columns=data.columns[0], axis=1)

    data = data.iloc[:, :2000].round(2)     # Trimming data to last 2000 trading sessions data
    data.to_csv(scrip_data_file_path)

    return
    