"""
Utilities to use throughout the modules.
"""


def string_list_to_list(string_list: str, sep: str = ",") -> list:
    """
    Convert a string list to a Python list by splitting on the separator.
    """
    return [category.strip() for category in string_list.split(sep)] if string_list else []


def get_first_item_in_dict(dictionary: dict) -> tuple:
    """
    Return the first key and value in a dictionary as a tuple.
    """
    return next(iter(dictionary.items()))


"""
Generic helper functions for the project.
"""
import contextlib
import datetime
import functools
import os
import pathlib
import re
from typing import Any, AnyStr, Callable

import pandas as pd

import utils.bank_holidays
import utils.logger


DEBUG = False


def is_date_valid(date_string: Any) -> bool:
    """
    Validate that a value is a valid date string in the ``%Y-%m-%d`` format.

    Note that date strings are validated by how the `Python Standard Library
    module datetime`_ understands strings representing dates which is a *slight*
    subset of the formats laid out in the `ISO-8601 standard`_.

    .. _Python Standard Library module datetime: https://docs.python.org/3/library/datetime.html
    .. _ISO-8601 standard: https://www.iso.org/iso-8601-date-and-time-format.html

    .. image:: https://imgs.xkcd.com/comics/iso_8601.png

    :return: ``True`` if the ``date_string`` is a valid ISO-8601 date string and
     ``False`` otherwise.
    """
    try:
        datetime.datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def string_to_date(
    date_string: str,
    date_format: str = "%Y-%m-%d",
) -> datetime.date:
    """
    Convert a date string into a ``datetime.date`` object.

    :param date_string: The text to convert into a ``datetime.date`` object.
    :param date_format: The format to use in converting the date string into the
     ``datetime.date`` object. Defaults to ``%Y-%m-%d``.
    :return: A ``datetime.date`` object corresponding to the text and format.
    """
    return datetime.datetime.strptime(date_string, date_format).date()


def _is_working_day(date: datetime.date, holidays: list[datetime.date]) -> bool:
    """
    A date is a "working day" if it is neither a weekend nor a holiday.
    """
    return (
        date.weekday() < 5  # 5 Saturday, 6 Sunday
        and date not in holidays
    )


def add_working_days(
    from_date: str | datetime.date,
    working_days: int,
    holidays: list[datetime.date] | None = None,
) -> datetime.date:
    """
    Add some number of working days to a date.

    If an argument is not passed to the ``holidays`` parameter, this will make a
    call to the UK Government website so an internet connection is required.

    Note that this is an extremely naive implementation but works for now.

    :param from_date: The ``datetime.date`` to add some number of working days
     to.
    :param working_days: The number of working days to add to ``from_date``.
    :param holidays: The list of ``datetime.date``s that should be considered
     holidays for the calculation. Defaults to ``None`` which uses the bank
     holidays for England and Wales from the UK Government website.
    :return: The ``datetime.date`` corresponding to the ``from_date`` plus the
     ``working_days``, accounting for holidays.
    """
    if type(from_date) == str:
        from_date = string_to_date(from_date)

    holidays = holidays or utils.bank_holidays.BankHolidayHandler(connect_on_init=True).bank_holidays

    working_day_counter = 0
    while working_day_counter < working_days:
        from_date += datetime.timedelta(days=1)
        if _is_working_day(from_date, holidays):
            working_day_counter += 1

    return from_date


def extract_directory(base_rate_date: str, filename: str = '') -> AnyStr:
    """
    Return the relative directory path for the given filename in the
    ``Extracts`` directory corresponding to the base rate date.

    :param base_rate_date: The base rate change date as a string in the ISO-8601
     format (date only). This will be used as the subdirectory name.
    :param filename: The name of the file being referenced. Defaults to ``''``.
    :return: The directory path for the given filename and base rate date.
    """
    # raise NotImplemented("This function needs to define a better extracts folder.")
    return os.path.abspath(os.path.join(".", "base_rate_change", "Extracts", base_rate_date, filename))


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


def clean_extract(dataframe: pd.DataFrame, columns_and_casing: list[tuple[str, bool]]) -> pd.DataFrame:
    """
    Return the dataframe with many of the string columns cleansed.

    :param dataframe: The Pandas.DataFrame to be cleaned.
    :param columns_and_casing: A list of tuples where the first element is the
     column name and the second element is whether it should be title-cased.
    :return: The cleaned version of the dataframe.
    """
    for col, case in columns_and_casing:
        with contextlib.suppress(AttributeError):
            dataframe.loc[:, col] = dataframe.loc[:, col].apply(clean_string, title_case=case)

    return dataframe


def snake_to_pascal(snake_case_text: str) -> str:
    """
    Convert a string in ``snake_case`` to ``PascalCase``.

    :param snake_case_text: A string in snake case. This is intended to be a
     single "word" so this function does not respect whitespace.
    :return: The string in Pascal case.
    """
    return snake_case_text.replace("_", " ").title().replace(" ", "")


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


def split_extract_by_column(
    dataframe: pd.DataFrame,
    column_to_split: str,
    values_to_split: list[Any]
) -> list[pd.DataFrame]:
    """
    Splits the input dataframe by the `column_to_split` column's values.

    Rather than enumerate through all values in the column, the intention is
    that the values should be explicitly passed in the `values_to_split` list.

    Returns a list so that the assignment is easy::

        df_1, df_2 = split_extract_by_column(df, "column", [1, 2])

    :param dataframe: The dataframe to split.
    :param column_to_split: The column whose values should split the dataframe.
    :param values_to_split: The list of values to split the dataframe by.
    :return: A list of dataframes, each corresponding to a value in the list.
    """
    return [
        dataframe.loc[dataframe[column_to_split] == value, :]
        for value in values_to_split
    ]


def split_extract_by_flag(
    dataframe: pd.DataFrame,
    flag_column: str,
    drop_flag: bool = False
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the input dataframe by the `flag_column` equal to 1 then 0.

    This is a tailored version of `split_extract_by_column`.

    :param dataframe: The dataframe to split.
    :param flag_column: The column whose values should split the dataframe. The
     values of this column should be only 1 or 0.
    :param drop_flag: Whether to drop the flag column from the resulting
     dataframes. Defaults to ``False``.
    :return: A tuple of dataframes corresponding to the flag column equal to 1
     and 0, respectively.
    """
    if drop_flag:
        return (
            dataframe.loc[dataframe[flag_column] == 1, :].drop(flag_column, axis=1),
            dataframe.loc[dataframe[flag_column] == 0, :].drop(flag_column, axis=1)
        )
    else:
        return (
            dataframe.loc[dataframe[flag_column] == 1, :],
            dataframe.loc[dataframe[flag_column] == 0, :]
        )


def _is_valid_xlsx_filepath(filepath: str | pathlib.Path) -> bool:
    return filepath.endswith(".xlsx")


def write_to_xlsx(
    dataframe: pd.DataFrame,
    filepath: str,
    loggable: bool = False
) -> None:
    """
    Write a dataframe to an Excel XSLX file without an index.

    :param dataframe: The dataframe to save to an Excel file.
    :param filepath: The filepath of the Excel file. If the file does not exist,
     a new one will be created.
    :param loggable: Whether to log a message with the number of rows and the
     file. Defaults to ``False``.
    :raises ValueError: If the ``filepath`` does not end with ``.xlsx``.
    """
    if not _is_valid_xlsx_filepath(filepath):
        raise ValueError(
            f"File names must end with '.xlsx'. The path {filepath} is invalid."
        )

    if loggable:
        utils.logger.log(f"Writing {len(dataframe)} rows to {filepath}.")

    if not DEBUG:
        with pd.ExcelWriter(filepath, mode="w") as writer:
            dataframe.to_excel(writer, index=False)


def write_many_to_xlsx(
    dataframes: dict[str, pd.DataFrame],
    filepath: str,
    loggable: bool = False
) -> None:
    """
    Write a list dataframe to sheets of an Excel XSLX file.

    :param dataframes: A dictionary with the dataframes to save to an Excel
     file. The keys of the dictionary must be the sheet names, and the values
     must be the corresponding dataframes.
    :param filepath: The filepath of the Excel file. If the file does not exist,
     a new one will be created.
    :param loggable: Whether to log a message with the number of rows and the
     file. Defaults to ``False``.
    :raises ValueError: If the ``filepath`` does not end with ``.xlsx``.
    """
    if not _is_valid_xlsx_filepath(filepath):
        raise ValueError(
            f"File names must end with '.xlsx'. The path {filepath} is invalid."
        )

    if DEBUG:
        for sheet_name, dataframe in dataframes.items():
            if loggable:
                utils.logger.log(f"Writing {len(dataframe)} rows to [{filepath}]{sheet_name}.")
    else:
        with pd.ExcelWriter(filepath, mode="w") as writer:
            for sheet_name, dataframe in dataframes.items():
                if loggable:
                    utils.logger.log(f"Writing {len(dataframe)} rows to [{filepath}]{sheet_name}.")
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
