# Usage

## Basic Example

```python
import polars as pl
import kra

df = pl.DataFrame({"First Name": [1], "Last Name": [2]})
print(df.cols.to_snakecase())
```

Output:
```
shape: (1, 2)
┌────────────┬───────────┐
│ first_name ┆ last_name │
└────────────┴───────────┘
```

## Renaming Columns

```python
df = pl.DataFrame({"a": [1], "b": [2]})
print(df.cols.rename({"a": "x", "c": "y"}))
```

Output:
```
shape: (1, 2)
┌─────┬─────┐
│ x   ┆ b   │
└─────┴─────┘
```

See the [API Reference](api/columns.md) for more details.
