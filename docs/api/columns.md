# kra.columns.Cols

A namespace for convenient DataFrame column operations, accessible via `df.cols` for any Polars DataFrame.

---

## Methods

### apply(fun, in_place=False)
**Description:**
Apply a function to all column names.

**Parameters:**
- `fun` (callable): Function to apply to each column name.
- `in_place` (bool, default False): If True, modify the DataFrame in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with transformed column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"A": [1], "B": [2]})
df.cols.apply(lambda x: x.lower())
# shape: (1, 2)
# ┌─────┬─────┐
# │ a   ┆ b   │
# └─────┴─────┘
```

---

### to_lowercase(in_place=False)
**Description:**
Convert all column names to lowercase.

**Parameters:**
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with lowercase column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"A": [1], "B": [2]})
df.cols.to_lowercase()
# shape: (1, 2)
# ┌─────┬─────┐
# │ a   ┆ b   │
# └─────┴─────┘
```

---

### to_uppercase(in_place=False)
**Description:**
Convert all column names to uppercase.

**Parameters:**
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with uppercase column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"a": [1], "b": [2]})
df.cols.to_uppercase()
# shape: (1, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# └─────┴─────┘
```

---

### to_titlecase(in_place=False)
**Description:**
Convert all column names to title case.

**Parameters:**
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with title-cased column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"first name": [1], "last name": [2]})
df.cols.to_titlecase()
# shape: (1, 2)
# ┌────────────┬───────────┐
# │ First Name ┆ Last Name │
# └────────────┴───────────┘
```

---

### to_camelcalse(in_place=False)
**Description:**
Convert all column names to camel case (e.g., "FirstName").

**Parameters:**
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with camelCase column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"first name": [1], "last name": [2]})
df.cols.to_camelcalse()
# shape: (1, 2)
# ┌──────────┬─────────┐
# │ FirstName┆ LastName│
# └──────────┴─────────┘
```

---

### to_snakecase(in_place=False)
**Description:**
Convert all column names to snake_case.

**Parameters:**
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with snake_case column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"First Name": [1], "Last Name": [2]})
df.cols.to_snakecase()
# shape: (1, 2)
# ┌────────────┬───────────┐
# │ first_name ┆ last_name │
# └────────────┴───────────┘
```

---

### replace(pattern, repl, in_place=False)
**Description:**
Replace a regex pattern in all column names.

**Parameters:**
- `pattern` (str or re.Pattern): Pattern to search for.
- `repl` (str): Replacement string.
- `in_place` (bool, default False): If True, modify in place. If False, return a copy.

**Returns:**
- `pl.DataFrame`: DataFrame with replaced column names.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"foo-bar": [1], "baz-bar": [2]})
df.cols.replace("-bar", "_suffix")
# shape: (1, 2)
# ┌──────────┬────────────┐
# │ foo_suffix ┆ baz_suffix │
# └──────────┴────────────┘
```

---

### has_all(columns, return_missing=True)
**Description:**
Check if all specified columns are present in the DataFrame.

**Parameters:**
- `columns` (list of str): List of column names to check.
- `return_missing` (bool, default True): If True, also return a list of missing columns.

**Returns:**
- `bool` or `(bool, list of str)`: True if all columns are present, otherwise False. If `return_missing` is True, also returns a list of missing columns.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"a": [1], "b": [2]})
df.cols.has_all(["a", "b"])
# (True, [])
df.cols.has_all(["a", "c"])
# (False, ['c'])
```

---

### has_any(columns)
**Description:**
Check if any of the specified columns are present in the DataFrame.

**Parameters:**
- `columns` (list of str): List of column names to check.

**Returns:**
- `bool`: True if any column is present, otherwise False.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"a": [1], "b": [2]})
df.cols.has_any(["b", "c"])
# True
df.cols.has_any(["x", "y"])
# False
```

---

### has_exactly(columns)
**Description:**
Check if the DataFrame has exactly the specified columns (no more, no less).

**Parameters:**
- `columns` (list of str): List of column names to check.

**Returns:**
- `bool`: True if the DataFrame has exactly these columns, otherwise False.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"a": [1], "b": [2]})
df.cols.has_exactly(["a", "b"])
# True
df.cols.has_exactly(["a"])
# False
```

---

### rename(mapping)
**Description:**
Rename columns using a mapping, skipping keys not present in the DataFrame. A non-strict version of DataFrame.rename().

**Parameters:**
- `mapping` (dict of str to str): Mapping from old column names to new names.

**Returns:**
- `pl.DataFrame`: DataFrame with renamed columns.

**Example:**
```python
import polars as pl
df = pl.DataFrame({"a": [1], "b": [2]})
df.cols.rename({"a": "x", "c": "y"})
# shape: (1, 2)
# ┌─────┬─────┐
# │ x   ┆ b   │
# └─────┴─────┘
```

---

For more details, see the source code or the [Usage](../usage.md) page.
