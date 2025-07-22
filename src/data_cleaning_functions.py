# Below is the ARC Application.xlsx cleaning function.

# pandas and numpy used for both functions

def df_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    columnsToRemove = [ # dropping columns of little consequence to any metric we might be exploring
        'KY Region',
        'Contact: Unique ID SSN',
	    'Contact: SSN Opt Out',
        'Contact: Mailing Zip/Postal Code',
	    'Seasonal farm worker?',
        'Contact: First Name',
	    'Contact: Last Name',
        'Status',
	    'Assessment: Created Date',
        'Contact: Approval Status'
    ]

    df = df.rename(columns={
        'Contact: Auto Id': 'Auto ID',
        'Contact: County': 'County',
        'Contact: Mailing State/Province': 'State',
        'Contact: Birthdate': 'Birthdate',
        'Contact: Gender': 'Gender',
        'Contact: Race': 'Race',
        'Contact: Veteran': 'Veteran'
    })

    df['State'] = ( # cleaning up the 'State' column so we can better look at demographics
        df['State']
            .str.strip() # removing whitespace
            .str.upper() # uppercase for ease of removal and change
            .replace({'KY': 'Kentucky'}) # specifically targeting the few cells that're 'KY'
            .str.title() # turning the caps back to title
    )

    df = df.drop(columnsToRemove, axis=1)

    fillElement = "Not Provided"    
    df = df.replace(np.nan, fillElement) # changing 'NaN' to "Not Provided"

    min_pct = 0.01 # giving a minimum percentage value for viable data
    df = df.dropna(axis=1, thresh=int(min_pct * len(df))) # precautionary 'thresh'old for relevant data or lack thereof
    df = df.drop_duplicates(subset=["Auto ID", "Date Completed"], keep="first", ignore_index=True) # being mindful that some students come back to take part in other cohorts

    return(df)

### --------------------------------- ###

# Below is the WORC Employment.xlsx cleaning function.

def df_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    columnsToRemove = [ # columns to remove
            'Full Name',
            'Email',
            'EnrollmentId',
            'Employment History Name',
            'Company Name',
            'Program: Program Name',
            'Mailing City',
            'Mailing Zip/Postal Code',
            'Gender',
            'Race',
            'KY Region'
        ]
    df = df.drop(columnsToRemove, axis=1)

    df = df.rename(columns = { # small rename
        'Auto Id': 'Auto ID'
    })

    fillElement = 'Not Provided'
    df = df.replace(np.nan, fillElement)

    return(df)