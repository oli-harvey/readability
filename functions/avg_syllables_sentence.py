import re
import pandas as pd

VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
EXCEPTIONS = re.compile(
    # fixes trailing e issues:
    # smite, scared
    "[^aeiou]e[sd]?$|"
    # fixes adverbs:
    # nicely
    + "[^e]ely$",
    flags=re.I
)
ADDITIONAL = re.compile(
    # fixes incorrect subtractions from exceptions:
    # smile, scarred, raises, fated
    "[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|"
    # fixes miscellaneous issues:
    # flying, piano, video, prism, fire, evaluate
    + ".y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua",
    flags=re.I
)

def avg_syllables_sentence(
        df: pd.DataFrame,
        col: str
        ) -> pd.DataFrame:
    out_df = df.copy()
    new_col_name = 'avg_syllables_sentence'
    out_df[new_col_name] = out_df[col].apply(_count_syllables)
    return out_df

def _count_syllables(x):
    vowel_runs = len(VOWEL_RUNS.findall(x))
    exceptions = len(EXCEPTIONS.findall(x))
    additional = len(ADDITIONAL.findall(x))
    syllables = max(1, vowel_runs - exceptions + additional)
    
    sentences = re.split(r'[.?!]\s*', x)
    return syllables / len(sentences)