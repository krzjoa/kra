import polars as pl

pl.api.register_dataframe_namespace('str')
class DataFarmeString:

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def extract(self, pattern) -> pl.DataFrame:
        """
        Extract substrings from all string columns in the DataFrame using a regex pattern.

        Parameters
        ----------
        pattern : str
            The regex pattern to extract.

        Returns
        -------
        pl.DataFrame
            A DataFrame with extracted substrings for each string column.

        Examples
        --------
        >>> import polars as pl
        >>> import kra  # noqa: F401
        >>> df = pl.DataFrame({"text1": ["abc123", "def456"], "text2": ["xyz789", "uvw000"]})
        >>> df.str.extract(r"(\\d+)")
        shape: (2, 2)
        ┌────────┬────────┐
        │ text1  ┆ text2  │
        │ ---    ┆ ---    │
        │ str    ┆ str    │
        ╞════════╪════════╡
        │ 123    ┆ 789    │
        │ 456    ┆ 000    │
        └────────┴────────┘
        """
        return self._df.select(
            pl.all().str.extract(pattern)
        )

