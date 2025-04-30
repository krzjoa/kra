import polars as pl
from kra.utils import extend_polars_dataframe


@extend_polars_dataframe
def drop_null_cols(df: pl.DataFrame) -> pl.DataFrame:
    """Exclude null columns"""
    return df.with_columns(pl.exclude(pl.Null))

@extend_polars_dataframe
def fork(df: pl.DataFrame, new_dfs: list) -> tuple[pl.DataFrame]:
    """Fork data frame into new ones"""
    # TODO: 
    return [df.with_columns(**n) for n in new_dfs]
