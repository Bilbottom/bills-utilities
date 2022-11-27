"""
Support for switching between various cases.

Case include:

- Snake case (``snake_case``)
- Kebab case (``kebab-case``)
- Dot case (``dot.case``)
- Camel case (``camelCase``)
- Pascal case (``PascalCase``)
"""
from __future__ import annotations

import abc
import enum
import re
from typing import AnyStr


class _Case(abc.ABC):
    _pattern: str
    _example: str
    pattern: re.Pattern[AnyStr]

    @staticmethod
    @abc.abstractmethod
    def from_case(text: str) -> list[str]:
        """
        Split the words in the text into a list.

        :param text: The text to split.
        :return: The words in the text as a list.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def to_case(text: list[str]) -> str:
        """
        Concatenate a list of words.

        :param text: The list of words to concatenate.
        :return: The concatenated list of words.
        """
        pass


class SnakeCase(_Case):
    _pattern = r"\b\w+\b"
    _example = "snake_case"
    pattern = re.compile(_pattern)

    @staticmethod
    def from_case(text: str) -> list[str]:
        return text.split("_")

    @staticmethod
    def to_case(text: list[str]) -> str:
        return "_".join(text).lower()


class KebabCase(_Case):
    _pattern = r"\b[\dA-Za-z-]+\b"
    _example = "kebab-case"
    pattern = re.compile(_pattern)

    @staticmethod
    def from_case(text: str) -> list[str]:
        return text.split("-")

    @staticmethod
    def to_case(text: list[str]) -> str:
        return "-".join(text).lower()


class DotCase(_Case):
    _pattern = r"\b[\dA-Za-z.]+\b"
    _example = "dot.case"
    pattern = re.compile(_pattern)

    @staticmethod
    def from_case(text: str) -> list[str]:
        return text.split(".")

    @staticmethod
    def to_case(text: list[str]) -> str:
        return ".".join(text).lower()


class CamelCase(_Case):
    _pattern = r"\b[\dA-Za-z]+\b"
    _example = "camelCase"
    pattern = re.compile(_pattern)

    @staticmethod
    def from_case(text: str) -> list[str]:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", text).split("_")

    @staticmethod
    def to_case(text: list[str]) -> str:
        string = "".join(token.title() for token in text)
        return string[0].lower() + string[1:]


class PascalCase(_Case):
    _pattern = r"\b[\dA-Za-z]+\b"
    _example = "PascalCase"
    pattern = re.compile(_pattern)

    @staticmethod
    def from_case(text: str) -> list[str]:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", text).split("_")

    @staticmethod
    def to_case(text: list[str]) -> str:
        return "".join(token.title() for token in text)


class Case(enum.Enum):
    SNAKE_CASE = SnakeCase()
    KEBAB_CASE = KebabCase()
    CAMEL_CASE = CamelCase()
    PASCAL_CASE = PascalCase()
    DOT_CASE = DotCase()


def _switch_case(text: str, from_case: Case, to_case: Case) -> str:
    return to_case.value.to_case(
        from_case.value.from_case(
            text
        )
    )


def switch_case(text: str, from_case: Case, to_case: Case) -> str:
    """
    Switch text from one case to another.

    Intended only for short names (like ``this_is_a_column``) but may also work
    for larger volumes of text.

    :param text: The text to change from one case to another.
    :param from_case: The case to change from.
    :param to_case: The case to change to.
    :return: The changed text.
    """
    if re.search(f"^{from_case.value.pattern}$", text):
        return _switch_case(text, from_case, to_case)

    string = text
    for item in re.findall(from_case.value.pattern, string):
        string = re.sub(f"\\b{item}\\b", _switch_case(item, from_case, to_case), string)
    return string
