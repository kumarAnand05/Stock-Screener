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
    rsi14 = ta.rsi(scrip_data.loc['Close'][TRADING_SESSIONS_LIMIT+14::-1], length=14)[::-1]

    for r in range(len(rsi14)):
        cell_data = scrip_data.loc['RSI'].iloc[0]
        if np.isnan(cell_data):
            cell_data = rsi14.iloc[r]
        else:
            break
    return scrip_data