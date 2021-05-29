from functions.avg_syllables_word import avg_syllables_word
from functions.avg_char_per_sentence import avg_char_per_sentence
from functions.avg_sentence_length import avg_sentence_length
from functions.avg_word_length import avg_word_length
import pandas as pd
import os 

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = df.copy()
    processed_df = avg_word_length(processed_df, 'excerpt')
    processed_df = avg_sentence_length(processed_df, 'excerpt')
    processed_df = avg_syllables_word(processed_df, 'excerpt')
    chars_to_count = [',', ';', "'", '"']
    for char in chars_to_count:
        processed_df = avg_char_per_sentence(
            processed_df,
            'excerpt',
            char
        )
    return processed_df