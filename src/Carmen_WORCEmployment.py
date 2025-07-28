import pandas as pd

file_path = "data/WORC_Employment.xlsx"
worc = pd.read_excel(file_path)

# removed auto id as we may need it later
cols_to_drop = ['Employment History Name']

worc_cols_dropped = worc.drop(columns=cols_to_drop, axis=1)

# Why did we decide to drop all nulls?
# This can be dangerous if we have a lot of nulls
# Also it removed the entire row if any column had a null value
# will this cause issues later?
worc_cols_dropped_nulls = worc_cols_dropped.dropna()

worc_cleaned = worc_cols_dropped_nulls
