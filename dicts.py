"""
Functions for dictionary manipulation.
"""
from typing import Any


def get_first_item_in_dict(dictionary: dict) -> tuple:
    """
    Return the first key and value in a dictionary as a tuple.
    """
    return next(iter(dictionary.items()))


def chained_get(dictionary: dict, *args, default: Any = None) -> Any:
    """
    Get a value nested in a dictionary by its nested path.

    :param dictionary: The dictionary to search.
    :param args: The keys to search for, in order.
    :param default: The value to return if the nested path does not exist.
     Defaults to ``None``.
    :return: The value in the dictionary at the nested path.
    """
    value_path = list(args)
    dict_chain = dictionary
    while value_path:
        try:
            dict_chain = dict_chain.get(value_path.pop(0))
        except AttributeError:
            return default

    return dict_chain
