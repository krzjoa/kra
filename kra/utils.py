import polars as pl
import numpy as np
import numpy.typing as npt

import polars.dataframe.group_by as plg 
# import polars.convert as plt

from kra.polars_api import extend_polars, extend_polars_dataframe, extend_polars_group_by


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
def from_dod(dod: dict, column: str, **kwargs) -> pl.DataFrame:
    """Construct a DataFrame from dictionary of dictionaries"""
    return pl.from_dicts([d | {column: k} for k, d in dod.items()], **kwargs)

from_dict_of_dicts = from_dod
extend_polars(from_dict_of_dicts)


@extend_polars
def from_arraylike(data: npt.ArrayLike,
    schema = None,*,
    schema_overrides: None = None,
    orient = None,
) -> pl.DataFrame:
    """Construct a DataFrame from a Cython memoryview or any other Array-like. This operation clones data.
    
    Parameters
    ----------
    data : :class:`npt.ArrayLike`
        Array-like data
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
        * As a list of column names; in this case types are automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If you supply a list of column names that does not match the names in the
        underlying data, the names given here will overwrite them. The number
        of names given in the schema should match the underlying data dimensions.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the columns param will be overridden.
    orient : {None, 'col', 'row'}
        Whether to interpret two-dimensional data as columns or as rows. If None,
        the orientation is inferred by matching the columns and data dimensions. If
        this does not yield conclusive results, column orientation is used.

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([[1, 2, 3], [4, 5, 6]])
    >>> df = pl.from_numpy(data, schema=["a", "b"], orient="col")
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┴
    
    """
    return pl.from_numpy(np.asarray(data), schema, schema_overrides, orient)

from_memoryview = from_arraylike
extend_polars(from_memoryview)


@extend_polars
def maybe_col(name, default=None):
    # https://github.com/pola-rs/polars/issues/18372
    col = pl.col(f"^{name}$")
    if not default:
        return col
    expr = pl.struct(col, default).struct[0]
    return expr.alias(name)

@extend_polars_dataframe
def split_entries_by(df: pl.DataFrame, column: str) -> pl.DataFrame:
    return df.select(pl.all().repeat_by(column).flatten(column)) \
        .with_columns(pl.lit(1).alias(column))


@extend_polars_group_by
def to_dicts(grouped_df: plg.GroupBy):
    return { k: v.to_dicts() for k, v in grouped_df}