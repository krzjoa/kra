import polars as pl


def extend_polars_dataframe(fun: callable):
    """Decorator to extend polars DataFrame API"""
    setattr(pl.DataFrame, fun.__name__, fun)
    return fun # Needed?

def extend_polars(fun: callable):
    """Decorator to extend polars DataFrame API"""
    setattr(pl, fun.__name__, fun)
    return fun