"""env_vars.py

Contains methods for getting environment variables.
"""

import os
import json
from json import JSONDecodeError

from util.printing import print_petrichor_error



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


def get_list(key : str) -> list | None:
    """
    Gets a list from the .env file with the given key, None if value is
    not a list, or key does not exist.

    Parameters
    ----------
    key : str
        the key of the environment variable to search for

    Returns
    -------
    list
        the list that was obtained | 
        None if value is not a list, or key does not exist
    """

    value = os.getenv(key)

    if not value:
        return None

    try:
        value = json.loads(value)

        if type(value) is not list:
            return

        return value

    except TypeError:
        print_petrichor_error('Incorrect encoding for JSON')
    except JSONDecodeError:
        print_petrichor_error('Could not decode JSON')

    return
