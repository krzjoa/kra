import polars as pl
from kra.utils import extend_polars_dataframe


@extend_polars_dataframe
def drop_null_cols(df: pl.DataFrame):
    """Exclude null columns"""
    return df.with_columns(pl.exclude(pl.Null))