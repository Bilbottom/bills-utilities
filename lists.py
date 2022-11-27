"""
Functions for list manipulation.
"""


def string_list_to_list(string_list: str, sep: str = ",") -> list:
    """
    Convert a string list to a Python list by splitting on the separator.
    """
    return [
        item.strip()
        for item in string_list.split(sep)
    ] if string_list else []
