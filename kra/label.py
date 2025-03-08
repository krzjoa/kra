import polars as pl

from kra.utils import Cloneable


@pl.api.register_expr_namespace('label')
class LabelExpr:

    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr
    
    def encode(self):
        pass




@pl.api.register_series_namespace('label')
class LabelSecris:

    def __init__(self, series: pl.Series) -> None:
        self._series = series
    
    def encode(self):
        d = {k: v for v, k in enumerate(self._series.unique())}
        return self._series.replace(d, return_dtype=pl.Int32)
        
