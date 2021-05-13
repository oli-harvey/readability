import pandas as pd
from pandas.api.types import is_string_dtype
import os 
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer



funcs = os.listdir('functions')
for func in funcs:
    if func.startswith('__') or func == 'import_all_functions.py':
        continue
    func = func.replace('.py','')
    exec(f'from functions.{func} import *')

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = df.copy()
    processed_df['GoodQualityTotalSF'] = processed_df['1stFlrSF'] + processed_df['2ndFlrSF']
    
    # drop useless columns. Utilities too sparsely populated to rely on model picking up
    # drop_cols = ['Utilities']
    # processed_df = processed_df.drop(columns=drop_cols)

    # impute missing
    # impute_cols = ['LotFrontage']
    processed_df = impute_cond_mean(
        processed_df,
        col_with_na='LotFrontage',
        cond_cols=['LotShape']
    )
    # imp = IterativeImputer(max_iter=10, random_state=0)
    # imp.fit(processed_df)
    # processed_df = imp.transform(processed_df)

    # these ones have values that correspond to the categories so make dummies afterwards but also make these first
    value_dummies = {
        'BsmtFinTypeSF': (['BsmtFinType1', 'BsmtFinType2'], ['BsmtFinSF1', 'BsmtFinSF2', 'Utilities'])
    }
    for prefix, col_tuple in value_dummies.items():
        cat_columns, value_columns = col_tuple
        processed_df = add_value_dummies_multiple_columns(
            data=processed_df,
            cat_columns=cat_columns,
            value_columns=value_columns,
            prefix=prefix,
            keep_original=True,
        )

    # convert categorical quality to numeric
    quality_cols_convert = [
        'ExterQual', 'ExterCond', 'BsmtQual', 'BsmtCond', 'BsmtExposure',
        'BsmtFinType1', 'BsmtFinType2', 'HeatingQC', 'KitchenQual', 'Functional',
        'FireplaceQu', 'GarageQual', 'GarageCond', 'PoolQC', 'Fence'
    ]
    for column in quality_cols_convert:
        # first convert to number keeping original column
        processed_df = quality_to_number(
            processed_df,
            column=column,
            keep_original=True,
        )
        # then flag zeros
        number_column = column + 'Number'
        processed_df = add_zero_flag(
            processed_df,
            column=number_column,
        )
    
    # these ones need combining after turning into dummies since values spread over pairs of columns
    dummy_pairs = {
        'Condition': ['Condition1', 'Condition2'],
        'Exterior': ['Exterior1st', 'Exterior2nd'],
        'BsmtFinType': ['BsmtFinType1', 'BsmtFinType2']
    }
    for prefix, columns in dummy_pairs.items():
        processed_df = add_dummies_multiple_columns(
            data=processed_df,
            columns=columns,
            prefix=prefix,
        )

    # create simple dummies
    # dummy_cols = [
    #     'MSSubClass', 'MSZoning', 'Alley', 'MoSold', 'SaleType', 'Street', 'LotShape', 'LandContour', 'LotConfig',
    #     'LandSlope', 'Neighborhood', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'MasVnrType', 'ExterQual', 
    #     ]
    # add quality cols as one hots too
    # filter for all str columns left
    dummy_cols = [
        col for col in
        processed_df.columns
        if is_string_dtype(processed_df[col])
    ]

    processed_df = pd.get_dummies(processed_df, columns=dummy_cols)

    # flag columns with 0s where useful
    zero_flags = [
        'MasVnrArea', '2ndFlrSF', 'BsmtFinSF1', 'BsmtFinSF2', 'LowQualFinSF', 'GarageYrBlt', 
        'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch'
    ]
    for column in zero_flags:
        processed_df = add_zero_flag(
            processed_df,
            column=column,
        )
    
    # calculate years since built and remodAdded
    columns_to_calculate_years_since = [
        ('YearBuilt', 'YrSold'),
        ('YearRemodAdd', 'YrSold'),
    ]
    for from_column, to_column in columns_to_calculate_years_since:
        processed_df = add_years_since(
            data=processed_df,
            from_column=from_column,
            to_column=to_column,
        )

    # deal with remod odd cases. hopefully flagging them is enough
    processed_df = add_had_remod_flag(processed_df)
    processed_df = add_year_remod_pre1950_flag(processed_df)

    processed_df = processed_df.fillna(-999)
    
    return processed_df