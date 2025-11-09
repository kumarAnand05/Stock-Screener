import yfinance as yf

    
def get_scrip_data(scrip_name, period):
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
