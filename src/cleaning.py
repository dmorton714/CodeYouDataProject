import pandas as pd


class DemographicsCleaning:
    """
    A class for cleaning and preprocessing demographic data.

    Provides methods to:
    - Remove unused or mostly null columns
    - Normalize gender values
    - Split the 'Race' column into multiple race columns
    - Drop duplicate rows
    """

    @staticmethod
    def remove_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove columns with mostly null values or unnecessary information.

        Args:
            df (pd.DataFrame): Input dataframe containing demographic data.

        Returns:
            pd.DataFrame: Dataframe with specified columns removed.
        """
        columns_to_drop = [
            'First Name', 'Last Name', 'Ethnicity Hispanic/Latino',
            'Single Parent', 'Ex-Offender', 'Program: Program Name', 'Outcome'
        ]
        return df.drop(columns=columns_to_drop, errors='ignore')

    @staticmethod
    def normalize_gender(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize gender values by combining 'Transgender male to female'
        and 'Transgender female to male' into a single 'Transgender' category.

        Args:
            df (pd.DataFrame): Input dataframe containing a 'Gender' column.

        Returns:
            pd.DataFrame: Dataframe with normalized gender values.
        """
        df['Gender'] = df['Gender'].replace({
            'Transgender male to female': 'Transgender',
            'Transgender female to male': 'Transgender'
        })
        return df

    @staticmethod
    def split_race_column(df: pd.DataFrame) -> pd.DataFrame:
        """
        Split the 'Race' column into multiple columns
        if multiple races are selected.

        Args:
            df (pd.DataFrame): Input dataframe containing a 'Race' column.

        Returns:
            pd.DataFrame: Dataframe with new columns Race_1, Race_2, etc.
        """
        splitting = df['Race'].str.split(';', expand=True)
        splitting.columns = [f'Race_{i+1}' for i in range(splitting.shape[1])]
        df = pd.concat([df.drop(columns=['Race']), splitting], axis=1)
        return df

    @staticmethod
    def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataframe.

        Args:
            df (pd.DataFrame): Input dataframe.

        Returns:
            pd.DataFrame: Dataframe without duplicate rows.
        """
        return df.drop_duplicates()

    @classmethod
    def clean(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform the full data cleaning process on demographics data.

        Steps include:
        - Removing unused or mostly null columns
        - Normalizing gender values
        - Splitting the 'Race' column into multiple race columns
        - Dropping duplicate rows

        Args:
            df (pd.DataFrame): Raw demographics dataframe.

        Returns:
            pd.DataFrame: Cleaned dataframe ready for analysis.
        """
        df = cls.remove_unused_columns(df)
        df = cls.normalize_gender(df)
        df = cls.split_race_column(df)
        df = cls.drop_duplicates(df)
        return df


class WorceCleaning:
    """
    A placeholder for a class that can be used to clean Worce data.
    This class can be extended in the future to include specific cleaning methods.
    """
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for cleaning Worce data.
        Currently does nothing but can be extended in the future.

        Args:
            df (pd.DataFrame): Input dataframe containing Worce data.

        Returns:
            pd.DataFrame: Unchanged dataframe.
        """
    pass


class NewClass:
    """
    A placeholder for a new class that can be added in the future.
    This class can be used to extend functionality or add new features.
    """

    @staticmethod
    def example_method():
        """
        An example method that can be implemented in the future.
        This is a placeholder for future functionality.
        """
        pass

    pass


if __name__ == "__main__":
    # Example usage:
    # Load the demographics data from an Excel file
    df = pd.read_excel('../data/All demographics and programs.xlsx')

    # Clean the data using the DemographicsCleaning class
    cleaned_df = DemographicsCleaning.clean(df)
