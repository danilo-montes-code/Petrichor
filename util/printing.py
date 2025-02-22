"""printing.py

Contains methods for printing.
"""

def print_petrichor_msg(message : str) -> None:
    """
    Prints a given message to the console with the Petrichor prefix.

    Parameters
    ----------
    message : str
        the message to print
    """
    print(f'[Petrichor] {message}')


def print_petrichor_error(message : str) -> None:
    """
    Prints a given message to the console with the Petrichor error prefix.

    Parameters
    ----------
    message : str
        the message to print
    """
    print(f'[Petrichor] [ERROR] {message}')

