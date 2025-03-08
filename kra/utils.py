import polars as pl
from kra.polars_api import extend_polars, extend_polars_dataframe


class Cloneable:

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def _clone_if(self, in_place) -> pl.DataFrame:
        if not in_place:
            df = self._df.clone()
        else:
            df = self._df
        return df


@extend_polars_dataframe
def to_dod(df: pl.DataFrame, key: str) -> dict:
    """Turn polars DataFrame to dict of dicts, using a column as dictionary
       Bear in mind you have to check the column uniqueness first. 
    """
    return {row[key]: row for row in df.to_dicts()}

to_dict_of_dicts = to_dod
extend_polars_dataframe(to_dict_of_dicts)


@extend_polars
def from_dod(dod: dict, column: str) -> pl.DataFrame:
    """Create polars DataFrame from dictionary of dictionaries"""
    return pl.from_dicts([d | {column: k} for k, d in dod.items()])

from_dict_of_dicts = from_dod
extend_polars(from_dict_of_dicts)
