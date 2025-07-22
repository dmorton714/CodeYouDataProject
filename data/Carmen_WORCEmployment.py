import pandas as pd
import os

file_path = "data/WORC_Employment.xlsx"
worc = pd.read_excel(file_path)

def unique(df, column='column'):
    """
    Check for unique values in a specified DataFrame column.

    Parameters:
    df: The DataFrame that contains the data.
    column: The name of the column to check for uniqueness.

    Returns:
    numpy.ndarray: An array of unique values in the specified column.
    """
    unique_values = df[column].unique()
    print(f"Unique values in '{column}': {unique_values}")
    
    return unique_values

unique(worc, 'ATP Placement Type')

worc.isnull().any().any()

cols_to_drop = ['Auto Id','Employment History Name']

worc_cols_dropped = worc.drop(columns=cols_to_drop, axis=1)

worc_cols_dropped_nulls = worc_cols_dropped.dropna()

worc_cleaned = worc_cols_dropped_nulls