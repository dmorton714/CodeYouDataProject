import pandas as pd


class Most_common_pathways_taken_data:
    def __init__(self, data):
        self.data = data
        self.__starter_pathways = [
            'Web Development M1',
            'Data Analysis M1',
            'Software Development M1',
            'Quality Assurance M1',
            'User Experience M1',
        ]
        self.starter_only_df = self.Get_starting_pathways()

    def Get_starting_pathways(self):
        """
            Returns a pandas.DataFrame were all the services are
            the beginning pathways.

            Args:
                df: pandas.DataFrame

            Return:
                pandas.DataFrame
        """
        mask_starter_pathways = self.data['Service'].isin(self.__starter_pathways) # noqa
        return self.data[mask_starter_pathways]

    def Get_cohorts_list(self):
        """
            List of cohorts from starting pathways.

            Args:
                df: pandas.DataFrame

            Return:
                list
        """
        df = self.starter_only_df
        cohorts = list(pd.to_datetime(df['ATP Cohort'][df['ATP Cohort'] != 'NA']).sort_values(ascending=True).astype(str).unique()) # noqa
        cohorts.insert(0, 'All cohorts')
        return cohorts

    def Get_data_by_cohort(self, cohort: str = 'All cohorts') -> pd.DataFrame:
        """
            Returns a pandas.DataFrame for a specific cohort or all cohorts.

            Args:
                df: pandas.DataFrame
                cohort: str

            Return:
                pandas.DataFrame
        """
        df = self.starter_only_df
        if cohort == 'All cohorts':
            result = df.value_counts('Service').reset_index()
        else:
            result = df[df['ATP Cohort'] == str(pd.to_datetime(cohort))].value_counts('Service').reset_index() # noqa

        return result
