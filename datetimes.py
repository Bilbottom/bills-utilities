"""
Functions for datetime manipulation.
"""
import datetime
from typing import Any


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

    Note that this is an extremely naive implementation but works for now.

    :param from_date: The ``datetime.date`` to add some number of working days
     to.
    :param working_days: The number of working days to add to ``from_date``.
    :param holidays: The list of ``datetime.date``s that should be considered
     holidays for the calculation. Defaults to ``None``.
    :return: The ``datetime.date`` corresponding to the ``from_date`` plus the
     ``working_days``, accounting for holidays.
    """
    if type(from_date) == str:
        from_date = string_to_date(from_date)

    working_day_counter = 0
    while working_day_counter < working_days:
        from_date += datetime.timedelta(days=1)
        if _is_working_day(from_date, holidays):
            working_day_counter += 1

    return from_date
