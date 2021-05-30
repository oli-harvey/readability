import pandas as pd

def avg_caps_word(
        df: pd.DataFrame,
        col: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    new_col_name = 'avg_caps_word'
    out_df[new_col_name] = out_df[col].apply(_avg_caps)
    return out_df

def _avg_caps(x):
    num_caps=0
    for char in x:
        if char.isupper():
           num_caps += 1
    words = x.split()
    return num_caps / len(words)