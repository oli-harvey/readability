import pandas as pd
import re

def avg_sentence_length(
        df: pd.DataFrame,
        col: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    
    out_df['avg_sentence_length_chars'] = out_df[col].apply(_avg_sentence_len_char)
    out_df['avg_sentence_length_words'] = out_df[col].apply(_avg_sentence_len_words)
    return out_df

def _avg_sentence_len_char(x):
    sentences = re.split(r'[.?!]\s*', x)
    sentence_lengths = [len(s) for s in sentences]
    avg_sentence_length = sum(sentence_lengths)/len(sentences)
    return avg_sentence_length

def _avg_sentence_len_words(x):
    sentences = re.split(r'[.?!]\s*', x)
    sentence_lengths_words = [
        len(s.split()) for s 
        in sentences
    ]
    avg_sentence_length_words = sum(sentence_lengths_words)/len(sentences)
    return avg_sentence_length_words
