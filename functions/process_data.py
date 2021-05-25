from functions.avg_word_length import avg_word_length
import pandas as pd
import os 

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = df.copy()
    processed_df = avg_word_length(processed_df, 'excerpt')
    return processed_df