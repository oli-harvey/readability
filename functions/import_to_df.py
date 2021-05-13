import pandas as pd

def import_to_df(
        list: str,
        path: str = "competition_data"
         ) -> dict:
    """
        Imports all the files in the list given
        Returns dictionary with file name minus extension as 
    """

    df_dict = {}
    for file in list:
        if 'csv' not in file:
            continue
        df = pd.read_csv("/".join([path, file]))
        # remove extension
        name = file.split('.')[0]
        df_dict[name] = df
    
    return df_dict
[

]