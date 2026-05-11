
import polars as pl
import numpy as np
import numpy.typing as npt

import polars.dataframe.group_by as plg 
from kra.polars_api import extend_polars, extend_polars_dataframe, extend_polars_group_by, extend_polars_series

@extend_polars_dataframe
def from_dict_rowwise(data: dict, key_col: str, val_col: str) -> pl.DataFrame:
    """
    Construct a DataFrame from a dictionary, assuming each key-value pair represents a row.

    Parameters
    ----------
    data : dict
        Dictionary where each key-value pair represents a row.
    key_col : str
        The name of the column to use for the keys of the dictionary.
    val_col : str
        The name of the column to use for the values of the dictionary.
    
    Returns
    -------
    pl.DataFrame
        DataFrame constructed from the dictionary.
    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> data = {"a": 1, "b": 2}
    >>> pl.from_dict_rowwise(data, "key", "value")
    shape: (2, 2)
    ┌─────┬───────┐
    │ key ┆ value │
    ├─────┼───────┤
    │ a   ┆ 1     │
    │ b   ┆ 2     │
    └─────┴───────┘
    """
    return pl.DataFrame({key_col: list(data.keys()), val_col: list(data.values())})


# TDOO: extend or not? That is the question.
def from_matrix(arr: np.ndarray, 
                schema: dict = {'x': pl.Int64, 'y': pl.Int64, 'value': pl.Float64},
                condition: callable = lambda x: x != 0) -> np.ndarray:
    """"Convert a 2D numpy array into a polars DataFrame with three columns: 'x', 'y', and 'value',
    where 'x' and 'y' are the indices of the non-zero elements in the
    array, and 'value' is the corresponding determined by the condition function (default is non-zero values).
    
    Parameters
    ----------
    arr : np.ndarray
        2D numpy array to convert.
    schema : dict
        Schema for the resulting DataFrame columns.
    condition : callable
        Function to determine which elements to include based on their values.
    Returns
    -------
    pl.DataFrame
        DataFrame with columns 'x', 'y', and 'value' representing the non-zero elements of the array.
    Examples
    --------
    >>> import numpy as np
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> arr = np.array([[0, 2, 0], [3, 0, 4]])
    >>> df = pl.from_matrix(arr)
    >>> df
    shape: (3, 3)
    ┌─────┬─────┬───────┐
    │ x   ┆ y   ┆ value │
    ├─────┼─────┼───────┤
    │ 0   ┆ 1   ┆ 2     │
    │ 1   ┆ 0   ┆ 3     │
    │ 1   ┆ 2   ┆ 4     │
    └─────┴─────┴───────┘
    """
    idx = np.where(condition(arr))
    val = arr[idx]
    concat = np.concatenate([np.array(idx).T, val[:, None]], axis=1)
    return pl.DataFrame(concat, schema=schema)



@extend_polars_dataframe
def to_dod(df: pl.DataFrame, key: str) -> dict:
    """
    Convert a polars DataFrame to a dict of dicts, using a column as the dictionary key.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to convert.
    key : str
        The column name to use as the key for the outer dictionary.
        Each value in this column must be unique.

    Returns
    -------
    dict
        Dictionary mapping unique values from the specified column to row dictionaries.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df = pl.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    >>> df.to_dod("id")
    {1: {'id': 1, 'name': 'Alice'}, 2: {'id': 2, 'name': 'Bob'}}
    """
    return {row[key]: row for row in df.to_dicts()}

to_dict_of_dicts = to_dod
extend_polars_dataframe(to_dict_of_dicts)


@extend_polars
def from_dod(dod: dict, column: str, **kwargs) -> pl.DataFrame:
    """
    Construct a DataFrame from a dictionary of dictionaries.

    Parameters
    ----------
    dod : dict
        Dictionary of dictionaries, where each key-value pair represents a row.
    column : str
        The name of the column to use for the keys of the outer dictionary.
    **kwargs
        Additional keyword arguments passed to `pl.from_dicts`.

    Returns
    -------
    pl.DataFrame
        DataFrame constructed from the dict of dicts.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> dod = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    >>> pl.from_dod(dod, "id")
    shape: (2, 2)
    ┌─────┬───────┐
    │ id  ┆ name  │
    ├─────┼───────┤
    │ 1   ┆ Alice │
    │ 2   ┆ Bob   │
    └─────┴───────┘
    """
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


@extend_polars_group_by
def to_dicts(grouped_df: plg.GroupBy) -> dict:
    """
    Convert a polars GroupBy object to a dictionary of lists of dicts.

    Returns
    -------
    dict
        Dictionary mapping group keys to lists of row dicts.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> df = pl.DataFrame({"g": ["a", "a", "b"], "x": [1, 2, 3]})
    >>> df.groupby("g").to_dicts()
    {'a': [{'g': 'a', 'x': 1}, {'g': 'a', 'x': 2}], 'b': [{'g': 'b', 'x': 3}]}
    """
    return { k: v.to_dicts() for k, v in grouped_df}


@extend_polars_series
def to_set(self: pl.Series) -> set:
    """
    Convert a Series to a set of unique values.

    Returns
    -------
    set
        Set of unique values in the Series.

    Examples
    --------
    >>> import polars as pl
    >>> import kra  # noqa: F401
    >>> s = pl.Series([1, 2, 2, 3])
    >>> s.to_set()
    {1, 2, 3}
    """
    return set(self.to_list())
