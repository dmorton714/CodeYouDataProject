import pandas as pd
import os

file_path = "data/WORC_Employment.xlsx"
worc = pd.read_excel(file_path)

cols_to_drop = ['Auto Id','Employment History Name']

worc_cols_dropped = worc.drop(columns=cols_to_drop, axis=1)

worc_cols_dropped_nulls = worc_cols_dropped.dropna()

worc_cleaned = worc_cols_dropped_nulls