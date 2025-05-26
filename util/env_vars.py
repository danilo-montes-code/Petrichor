"""env_vars.py

Contains methods for getting environment variables.
"""

from util.printing import print_petrichor_error

import os, json

from json import JSONDecodeError

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


def get_dict(key : str) -> dict | None:
    """
    Gets a dictionary from the .env file with the given key, None if value is
    not a dictionary, or key does not exist.
    
    Parameters
    ----------
    key : str
        the key of the environment variable to search for
    
    Returns
    -------
    dict
        the dictionary that was obtained | 
        None if value is not a dictionary, or key does not exist
    """

    value = os.getenv(key)

    if not value:
        return None
    
    try:
        value = json.loads(value)

        if type(value) is not dict:
            return

        return value
    
    except TypeError:
        print_petrichor_error('Incorrect encoding for JSON')
    except JSONDecodeError:
        print_petrichor_error('Could not decode JSON')
        
    return
    