import pandas as pd
import numpy as np

class EnrollmentsCleaning:
    def __init__(self, raw_data):
        self.raw_data = raw_data
    
    def Drop_columns(self, df):
        COLUMNS_TO_DROP = ['Full Name']
        result = df.drop(columns=COLUMNS_TO_DROP)
        return result
    
    def Fix_nan_values(self, df):
        # Fix NaN values
        NAN_VALUE_SUBSTITUTE = 'NA'
        columns_to_fix = {
            'Projected Start Date': NAN_VALUE_SUBSTITUTE, 'Actual Start Date': NAN_VALUE_SUBSTITUTE, 'Projected End Date': NAN_VALUE_SUBSTITUTE,
            'Actual End Date': NAN_VALUE_SUBSTITUTE, 'Outcome': NAN_VALUE_SUBSTITUTE
        }
        # 'ATP Cohort' NA will handle in a separed function
        for column, substitute_value in columns_to_fix.items():
            df[column] = df[column].fillna(substitute_value)
        
        return df
    
    def Rename_values(self, df):
        # Fix change name Data Analitics 2 to Data Analysis 2 for consistency
        df.loc[df['Service'] == 'Data Analytics 2', 'Service'] = 'Data Analysis 2'
        return df
    
    def Delete_values(self, df):
        # Delete values not needed
        # 'Referral to External Service', 'Supportive Services Referral', are deleted because dont have a "Projected Start Date" 
        values_not_needed = {
            'Service': ['Software Development 1', 'Software Development 2', 'Web Development 1', 'Web Development 2', 'Data Analysis 1','Data Analysis 2', 'Referral to External Service', 'Supportive Services Referral']
        }
        for column, value in values_not_needed.items():
            df = df[~df[column].isin(value)]
        return df
        
    def Set_data_types(self, df):
        # DataTypes
        column_datatype: dict = {'Auto Id': str, 'KY Region': str, 'Assessment ID': str, 'EnrollmentId': str,
        'Enrollment Service Name': str, 'Service': str, 'Projected Start Date': str,
        'Actual Start Date': str, 'Projected End Date': str, 'Actual End Date': str, 'Outcome': str,
        'ATP Cohort': 'datetime64[ns]'}
        # TODO: 'Projected Start Date', 'Actual Start Date', 'Projected End Date', 'Actual End Date' are all datetime types but have a value fix of NA
        
        for column, type in column_datatype.items():
            df[column] = df[column].astype(type)
        return df
    
    def Find_cohort(self, id: str, projected_start_date: str, cohort_to_find: str, df_to_clean: pd.DataFrame):
        ## Q: What to do with Service: ['Referral to External Service', 'Supportive Services Referral']
        ## TODO: Clean the NaTType before this function runs
        if pd.isna(cohort_to_find):
            student_df = df_to_clean[df_to_clean['Auto Id'] == id]
            # remove ATP Cohort NA values, it can be more than one
            student_df: pd.DataFrame = student_df[~student_df['ATP Cohort'].isna()]
            cohorts_participaded = student_df['ATP Cohort'].astype('datetime64[ns]').unique()
            
            # print(cohorts_participaded)
            if len(cohorts_participaded) == 1:
                return cohorts_participaded[0]
            else:
                # cohorts_participaded.append(pd.to_datetime(projected_start_date))
                stimated_module_date = np.datetime64(projected_start_date)
                cohorts_participaded = np.append(cohorts_participaded, stimated_module_date)
                cohorts_participaded.sort()
                previus_date = cohorts_participaded[0]
                for cohort in cohorts_participaded:
                    if stimated_module_date == cohort:
                        return previus_date
        else:
            return np.datetime64(cohort_to_find)

    def Get_clean_data(self):
        df = self.raw_data
        df = self.Drop_columns(df)
        df = self.Fix_nan_values(df)
        df = self.Rename_values(df)
        df = self.Delete_values(df)
        df = self.Set_data_types(df)
        df['ATP Cohort'] = df.apply(lambda row: self.Find_cohort(row['Auto Id'], row['Projected Start Date'], row['ATP Cohort'], df), axis=1)
        return df