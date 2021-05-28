import pandas as pd
import re

def avg_char_per_sentence(
        df: pd.DataFrame,
        col: str,
        char: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    new_col_name = col + f'_avg_{char}_per_sentence'
    out_df[new_col_name] = out_df[col].apply(_avg_char_per_sentence, char=char)
    return out_df

def _avg_char_per_sentence(x, char):
    sentences = re.split(r'[.?!]\s*', x)
    chars = x.count(char)
    avg_chars = chars / len(sentences)
    return avg_chars