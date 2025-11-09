import pandas as pd
import pandas_ta as ta
from utilities.commons import TRADING_SESSIONS_LIMIT
import numpy as np

def get_rsi(scrip_data):
    """
    Calculate the Relative Strength Index (RSI) for the given scrip data.
    Args:
        scrip_data (pd.DataFrame): The time series data of the scrip.
    """

    if "RSI" not in scrip_data.index:
        # Adding empty RSI row if not present
        rsi = pd.Series(dtype="float64", name="RSI", index=scrip_data.columns)
        scrip_data = pd.concat([scrip_data, rsi.to_frame().T])

    # Calculating RSI using pandas_ta
    rsi14 = ta.rsi(scrip_data.loc['Close'][TRADING_SESSIONS_LIMIT+14::-1], length=14)[::-1].to_numpy()
    
    rsi_values = scrip_data.loc['RSI'].to_numpy().copy()

    for r in range(len(rsi14)):
        cell_data = rsi_values[r]
        if np.isnan(cell_data):
            rsi_values[r] = rsi14[r]
        else:
            break
    scrip_data.loc['RSI'] = rsi_values
    return scrip_data