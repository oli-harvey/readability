import pandas as pd

def avg_word_length(
        df: pd.DataFrame,
        col: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    new_col_name = 'avg_word_length'
    out_df[new_col_name] = out_df[col].apply(_avg_word_len)
    return out_df

def _avg_word_len(x):
    words = x.split()
    word_lengths = [len(word) for word in words]
    avg_word_length = sum(word_lengths)/len(words)
    return avg_word_length