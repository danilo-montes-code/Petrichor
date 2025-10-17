"""printing.py

Contains methods for printing.
"""
import datetime


def print_petrichor_msg(message : str) -> None:
    """
    Prints a given message to the console with the Petrichor prefix.

    Parameters
    ----------
    message : str
        the message to print
    """
    print(
        prefix_with_time(
            f'[Petrichor] {message}'
        )
    )


def print_petrichor_error(message : str) -> None:
    """
    Prints a given message to the console with the Petrichor error prefix.

    Parameters
    ----------
    message : str
        the message to print
    """
    print(
        prefix_with_time(
            f'[Petrichor] [ERROR] {message}'
        )
    )


def prefix_with_time(message : str) -> str:
    """
    Prefixes a given message with the current time in HH:MM:SS format.

    Parameters
    ----------
    message : str
        the message to prefix

    Returns
    -------
    str
        the message prefixed with the current time
    """
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'[{current_time}] {message}'
