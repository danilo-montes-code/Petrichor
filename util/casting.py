"""casting.py

Contains methods for type casting.
"""

import os

def get_id(name : str) -> int:
    """
    Gets the Discord id from the env file.
    
    Parameters
    ----------
    name : str
        the env variable key to get the value of

    Returns
    -------
    int
        the id of the Discord object
    """
    return int(os.getenv(name))
