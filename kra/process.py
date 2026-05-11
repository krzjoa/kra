import polars as pl
from polars._typing import IntoExpr
from typing import Iterable
from kra.utils import extend_polars_dataframe
import polars.selectors as ps


@extend_polars_dataframe
def drop_null_cols(df: pl.DataFrame) -> pl.DataFrame:
    """
    Exclude columns of type Null from the DataFrame.

    Returns
    -------
    pl.DataFrame
        DataFrame with all columns of type Null removed.

    Examples
    --------
    >>> import polars as pl
    >>> import kra 
    >>> df = pl.DataFrame({"a": [1, 2], "b": [None, None]})
    >>> df.drop_null_cols()
    shape: (2, 1)
    ┌─────┐
    │ a   │
    ├─────┤
    │ 1   │
    │ 2   │
    └─────┘
    """
    return df.with_columns(pl.exclude(pl.Null))

@extend_polars_dataframe
def fork(df: pl.DataFrame, new_dfs: list) -> list[pl.DataFrame]:
    """
    Fork a DataFrame into multiple new DataFrames with additional columns.

    Parameters
    ----------
    new_dfs : list of dict
        Each dict specifies new columns to add to a forked DataFrame.

    Returns
    -------
    list of pl.DataFrame
        List of new DataFrames, each with the specified additional columns.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  
    >>> df = pl.DataFrame({"a": [1, 2]})
    >>> forks = df.fork([{"b": [10, 20]}, {"c": [100, 200]}])
    >>> for f in forks:
    ...     print(f)
    shape: (2, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    ├─────┼─────┤
    │ 1   ┆ 10  │
    │ 2   ┆ 20  │
    └─────┴─────┘
    shape: (2, 2)
    ┌─────┬───────┐
    │ a   ┆ c     │
    ├─────┼───────┤
    │ 1   ┆ 100   │
    │ 2   ┆ 200   │
    └─────┴───────┘
    """
    # TODO: 
    return [df.with_columns(**n) for n in new_dfs]


@extend_polars_dataframe
def agg(df: pl.DataFrame, 
        *aggs: IntoExpr | Iterable[IntoExpr],
        **named_aggs: IntoExpr) -> pl.DataFrame:
    """
    Aggreegate whole DataFrame as a single group. 
    This is a convenient way to apply aggregation expressions to the entire DataFrame without needing to specify a group key.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to aggregate.
    *aggs : IntoExpr or Iterable[IntoExpr]
        Positional aggregation expressions to apply to the DataFrame.
    **named_aggs : IntoExpr
        Named aggregation expressions, where the key is the name of the resulting column and the value is the aggregation expression.

    Returns
    -------
    pl.DataFrame
        Aggregated DataFrame.

    Examples
    --------
    >>> import polars as pl
    >>> import kra
    >>> df = pl.DataFrame({"group": ["A", "A", "B"], "value": [1, 2, 3]})
    >>> kra.agg(df, pl.col("value").sum().alias("total_value"))
    shape: (1, 1)
    ┌─────────────┐
    │ total_value │
    ├─────────────┤
    │ 6           │
    └─────────────┘
    >>> kra.agg(df, total_value=pl.col("value").sum())
    shape: (1, 1)
    ┌─────────────┐
    │ total_value │
    ├─────────────┤
    │ 6           │
    └─────────────┘
    """
    return df.group_by(True) \
             .agg(*aggs, **named_aggs) \
             .select(pl.exclude(pl.col("*").first()))


@extend_polars_dataframe
def round(df: pl.DataFrame, decimals: int = 2) -> pl.DataFrame:
    """
    Round all numeric columns in the DataFrame to a specified number of decimal places.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to round.
    decimals : int
        The number of decimal places to round to (default is 2).

    Returns
    -------
    pl.DataFrame
        DataFrame with all numeric columns rounded to the specified number of decimal places.

    Examples
    --------
    >>> import polars as pl
    >>> import kra
    >>> df = pl.DataFrame({"a": [1.234, 2.345], "b": [3.456, 4.567], "c": ["x", "y"]})
    >>> kra.round(df, decimals=1)
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    ├─────┼─────┼─────┤
    │ 1.2 ┆ 3.5 ┆ x   │
    │ 2.3 ┆ 4.6 ┆ y   │
    └─────┴─────┴─────┘
    """
    return df.with_columns(ps.float().round(decimals))