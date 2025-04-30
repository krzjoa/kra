import polars as pl
import re

from kra.utils import Cloneable


@pl.api.register_dataframe_namespace('cols')
class Cols(Cloneable):

    def apply(self, fun: callable, in_place: bool = False):
        df = self._clone_if(in_place)
        df.columns = [fun(x) for x in df.columns]
        return df 
    
    def to_lowercase(self, in_place: bool = False):
        return self.apply(lambda x: x.lower(), in_place=in_place)
    
    def to_uppercase(self, in_place: bool = False):
        return self.apply(lambda x: x.upper(), in_place=in_place)
    
    def to_titlecase(self, in_place: bool = False):
        return self.apply(lambda x: x.title(), in_place=in_place)
    
    def to_camelcalse(self, in_place: bool = False):
        fun = lambda x: ''.join(word for word in x.title() if not x.isspace())
        return self.apply(fun, in_place=in_place)

    def to_snakecase(self, in_place: bool = False):
        fun = lambda x: re.sub('\\s', '', re.sub(r'(?<!^)(?=[A-Z])', '_', x)).lower()
        return self.apply(fun, in_place=in_place)
    
    def replace(self, pattern: str | re.Pattern, repl: str, in_place: bool = False):
        return self.apply(lambda x: re.sub(pattern, repl, x), in_place=in_place)
    
    def has_all(self, columns: list[str], return_missing: bool = True) -> bool | tuple[bool, list[str]]:
        missing = self._missing_cols(columns)
        if return_missing:
            return len(missing) == 0, missing
        return len(missing) == 0
    
    def has_any(self, columns: list[str]) -> bool:
        return len(self._common_cols(columns)) > 0
    
    def has_exactly(self, columns: list[str]) -> bool:
        return set(columns) == set(self._df.columns)
    
    def rename(self, mapping: dict[str, str]) -> pl.DataFrame:
        """A non-strict version of DataFrame.rename() method.
           It skips missing keys without raising an error.
        """
        mapping = {k:v for k, v in mapping.items() if k in self._df.columns}
        return self._df.rename(mapping)
                 
    def _common_cols(self, columns: list[str]):
        return set(columns).intersection(set(self._df.columns))

    def _missing_cols(self, columns: list[str]):
        return set(columns).difference(set(self._df.columns))