import pandas as pd

def avg_vowels_word(
        df: pd.DataFrame,
        col: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    new_col_name = 'avg_vowels_word'
    out_df[new_col_name] = out_df[col].apply(_avg_vowels)
    return out_df

def _avg_vowels(x):
    num_vowels=0
    for char in x:
        if char in "aeiouAEIOU":
           num_vowels = num_vowels+1
    words = x.split()
    return num_vowels / len(words)