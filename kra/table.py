from kra.polars_api import extend_polars_dataframe
try:
    from IPython.display import display, HTML
except ImportError:
    pass


@extend_polars_dataframe
def show_scrollable(df,  max_height=400, max_width="100%"):
    """
    Display a scrollable table in Jupyter Notebook.

    Parameters
    ----------
    df : polars.DataFrame
        The DataFrame to display.
    max_height : int, optional
        The maximum height of the table in pixels (default is 400).
    max_width : str, optional
        The maximum width of the table (default is "100%").
    
    Returns
    -------
    None
        Displays the table in a scrollable container.
    
    Example
    -------
    >>> import polars as pl
    >>> from kra.table import show_scrollable
    >>> df = pl.DataFrame({
    ...     "Name": ["Alice", "Bob", "Charlie", "David"],
    ...     "Age": [25, 30, 35, 40],
    ...     "City": ["New York", "Los Angeles", "Chicago", "Houston
    ... ]})
    >>> show_scrollable(df, max_height=200)
    """
    html = f"""
    <div style="
        max-height:{max_height}px;
        max-width:{max_width};
        overflow:auto;
        border:1px solid #ddd;
        border-radius:6px;">
        {df.to_pandas().to_html(index=False)}
    </div>
    """
    display(HTML(html))

