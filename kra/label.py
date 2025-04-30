import polars as pl

from kra.utils import Cloneable


@pl.api.register_expr_namespace('label')
class LabelExpr:

    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr
    
    def encode(self):
        return self._expr.cast(pl.String).cast(pl.Categorical).to_physical()


@pl.api.register_series_namespace('label')
class LabelSeries:

    def __init__(self, series: pl.Series) -> None:
        self._series = series
    
    def encode(self):
        return self._series.cast(pl.String).cast(pl.Categorical).to_physical()
        # d = {k: v for v, k in enumerate(self._series.unique())}
        # return self._series.replace(d, return_dtype=pl.Int32)
        
