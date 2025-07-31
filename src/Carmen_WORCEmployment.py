import pandas as pd

def load_and_clean(file_path="../../data/WORC_Employment.xlsx"):
    """
    Loads and cleans the WORC Employment dataset.
    
    Parameter:
        file_path (str): Relative path to the Excel file.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Load data
    worc = pd.read_excel(file_path)

    # Drop columns we don't need
    cols_to_drop = ['Employment History Name']
    worc_cols_dropped = worc.drop(columns=cols_to_drop, axis=1)

    # Clean up data types
    worc_cols_dropped['Start Date'] = pd.to_datetime(worc_cols_dropped['Start Date'])
    worc_cols_dropped['Salary'] = pd.to_numeric(worc_cols_dropped['Salary'], errors='coerce')

    # Adjust salary that is listed as 60,000 to 28.84 for consistency with other salaries
    # Took 60,000 / 2080hrs - 28.84
    worc_cols_dropped['Salary'] = worc_cols_dropped['Salary'].replace(60000, 28.84)

    worc_clean = worc_cols_dropped
    return worc_clean
