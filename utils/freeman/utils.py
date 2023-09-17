import pandas as pd

_show_commas = lambda v: f'{v:,}'
show_commas = lambda df: df.style.format({
    col: _show_commas for col in df.select_dtypes(include=['int64', 'float64']).columns
})