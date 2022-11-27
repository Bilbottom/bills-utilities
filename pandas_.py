"""
Functions for Pandas dataframe manipulation.
"""
import pandas as pd


def split_extract_by_column(
    dataframe: pd.DataFrame,
    column_to_split: str,
    values_to_split: list
) -> list[pd.DataFrame]:
    """
    Splits the input dataframe by the ``column_to_split`` column's values.

    Rather than enumerate through all values in the column, the intention is
    that the values should be explicitly passed in the ``values_to_split`` list.

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
    Splits the input dataframe by the ``flag_column`` equal to 1 then 0.

    This is a tailored version of ``split_extract_by_column``.

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
