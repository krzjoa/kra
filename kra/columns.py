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