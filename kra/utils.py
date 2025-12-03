import polars as pl
import numpy as np
import numpy.typing as npt

import polars.dataframe.group_by as plg 

from kra.polars_api import extend_polars, extend_polars_dataframe, extend_polars_group_by, extend_polars_series


class Cloneable:

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def _clone_if(self, in_place) -> pl.DataFrame:
        if not in_place:
            df = self._df.clone()
        else:
            df = self._df
        return df


@extend_polars
def maybe_col(name, default=None) -> pl.Expr:
    """
    Return a column expression for a column with the given name, or a default value if the column is missing.

    Parameters
    ----------
    name : str
        The column name to select.
    default : Any, optional
        The default value to use if the column is missing.

    Returns
    -------
    pl.Expr
        A polars expression selecting the column or the default value.

    Examples
    --------
    >>> import polars as pl
    >>> import kra
    >>> df = pl.DataFrame({"a": [1, 2]})
    >>> df.select(kra.maybe_col("a", 0))
    shape: (2, 1)
    ┌─────┐
    │ a   │
    ├─────┤
    │ 1   │
    │ 2   │
    └─────┘
    >>> df.select(kra.maybe_col("b", 0))
    shape: (2, 1)
    ┌─────┐
    │ b   │
    ├─────┤
    │ 0   │
    │ 0   │
    └─────┘
    """
    # https://github.com/pola-rs/polars/issues/18372
    col = pl.col(f"^{name}$")
    if not default:
        return col
    expr = pl.struct(col, default).struct[0]
    return expr.alias(name)


@extend_polars_dataframe
def split_entries_by(df: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Repeat and flatten all columns by the values in a given column.

    Parameters
    ----------
    column : str
        The column whose values determine the number of repetitions for each row.

    Returns
    -------
    pl.DataFrame
        DataFrame with rows repeated and flattened according to the column.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df = pl.DataFrame({"a": [1, 2], "n": [2, 3]})
    >>> df.split_entries_by("n")
    shape: (5, 2)
    ┌─────┬─────┐
    │ a   ┆ n   │
    ├─────┼─────┤
    │ 1   ┆ 1   │
    │ 1   ┆ 1   │
    │ 2   ┆ 1   │
    │ 2   ┆ 1   │
    │ 2   ┆ 1   │
    └─────┴─────┘
    """
    return df.select(pl.all().repeat_by(column).flatten(column)) \
        .with_columns(pl.lit(1).alias(column))


@extend_polars_dataframe
def drop_rows(df: pl.DataFrame, row_idx: list[int] | int) -> pl.DataFrame:
    """
    Drop rows from the DataFrame based on their indices.

    Parameters
    ----------
    row_indices : list of int
        List of row indices to drop.

    Returns
    -------
    pl.DataFrame
        DataFrame with specified rows dropped.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    >>> df.drop_rows([0, 2])
    shape: (1, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    ├─────┼─────┤
    │ 2   ┆ 5   │
    └─────┴─────┘
    """
    if isinstance(row_idx, int):
        row_idx = [row_idx]
    mask = ~pl.arange(0, len(df)).is_in(row_idx)
    return df.filter(mask)



@extend_polars_dataframe
def row_as_header(df: pl.DataFrame, row_idx: int = 0) -> pl.DataFrame:
    """
    Set a specified row as the header (column names) of the DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to modify.
    row_idx : int, default 0
        The index of the row to use as the new header.
    Returns
    -------
    pl.DataFrame
        DataFrame with the specified row set as the header.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df = pl.DataFrame([["Name", "Age"], ["Alice", 30], ["Bob", 25]])
    >>> df = kra.row_as_header(df, 0)
    >>> df
    shape: (2, 2)
    ┌───────┬─────┐
    │ Name  ┆ Age │
    │ ---   ┆ --- │
    │ str   ┆ i64 │
    ╞═══════╪═════╡
    │ Alice ┆ 30  │
    │ Bob   ┆ 25  │
    └───────┴─────┘
    """
    return df \
            .rename({x:str(y) for x,y in zip(df.columns, df.row(row_idx))}) \
            .filter(pl.arange(0, len(df)) != row_idx)


def no(df: pl.DataFrame) -> bool:
    """
    Check if the DataFrame is null or empty.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to check.

    Returns
    -------
    bool
        True if the DataFrame is null or has no rows, False otherwise.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df_empty = pl.DataFrame()
    >>> kra.no(df_empty)
    True
    >>> df_non_empty = pl.DataFrame({"a": [1]})
    >>> kra.no(df_non_empty)
    False
    >>> kra.no(None)
    True
    """
    return (df is None) or (df.is_empty())