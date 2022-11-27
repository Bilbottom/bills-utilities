"""
Functions for string manipulation.
"""
from __future__ import annotations

import re
import strings.case_switcher


def snake_to_pascal(snake_case_text: str) -> str:
    """
    Convert a string in ``snake_case`` to ``PascalCase``.

    :param snake_case_text: A string in snake case. This is intended to be a
     single "word" so this function does not respect whitespace.
    :return: The string in Pascal case.
    """
    return strings.case_switcher.switch_case(
        text=snake_case_text,
        from_case=strings.case_switcher.Case.SNAKE_CASE,
        to_case=strings.case_switcher.Case.PASCAL_CASE
    )


def clean_string(string: str, title_case: bool, if_null: str = None, override: bool = False) -> str | None:
    """
    Replace all consecutive whitespace character with spaces, and conditionally
    title-case the string or set it to another value if it is missing.

    Note that, by default, the title-casing is only done if the string is either
    completely uppercase or completely lowercase to avoid changing the case of
    words that are already correct and where title-case is inappropriate, such
    as *McDonald*. This can be overridden with the ``override`` parameter.

    :param string: The string value to be cleaned.
    :param title_case: Whether to title-case the string. Will only title-case
     string if they are either completely uppercase or completely lowercase, but
     this can be overridden with the `override` parameter.
    :param if_null: Replaces ``None`` values with this value. Defaults to
     ``None``.
    :param override: If ``True``, then the title-casing will be applied
     regardless of the current casing of the string. Defaults to ``False``.
    :return: The cleaned version of the string.
    """
    if not string:
        return if_null
    if type(string) != str:
        return string

    stripped = re.sub(r"\s+", " ", string.strip())
    if not title_case:
        return stripped
    elif override:
        return stripped.title()
    else:
        return stripped.title() if (stripped.islower() or stripped.isupper()) else stripped
