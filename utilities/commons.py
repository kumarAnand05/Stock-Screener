import os
from datetime import datetime

TRADING_SESSIONS_LIMIT = 2000 

def get_project_dir():
    """
    Returns the root directory of the project.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    