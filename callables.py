"""
Functions for callable manipulation.
"""
import functools
from typing import Callable


def compose(*functions: Callable) -> Callable:
    """
    Compose an arbitrary number of functions.

    This will compose the functions such that they will be executed from left to
    right. For example, consider the assignment below::

        plus_one_times_two = compose(plus_one, times_two)

    When ``plus_one_times_two`` is called, this will call ``plus_one`` first and
    then ``times_two``::

        plus_one_times_two(x) = times_two(plus_one(x))

    Source:

    - https://mathieularose.com/function-composition-in-python

    :param functions: The functions to compose from left to right.
    :return: The composed function.
    """
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions[::-1],
        lambda x: x
    )
