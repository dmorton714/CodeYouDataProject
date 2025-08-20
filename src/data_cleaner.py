import pandas as pd
import numpy as np

class DataCleaner:
    """
    General-purpose cleaner for multiple WORC datasets
    (Employment, Enrollments, Demographics).
    
    Uses try/except for safety (does not break if col missing).
    Keeps all rows (no drops), but fills/fixes when possible.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def safe_drop_columns(self, cols_to_drop):
        """Drop columns if they exist, otherwise ignore."""
        try:
            self.df = self.df.drop(columns=cols_to_drop, errors='ignore')
        except Exception as e:
            print(f"[Warning] Failed dropping columns: {e}")
        return self

    def safe_fillna(self, fill_map: dict):
        """Fill NaN values for specific columns safely."""
        for col, val in fill_map.items():
            try:
                if col in self.df.columns:
                    self.df[col] = self.df[col].fillna(val)
            except Exception as e:
                print(f"[Warning] Failed filling NaN for {col}: {e}")
        return self

    def safe_replace(self, col, replacements: dict):
        """Replace values in a column safely."""
        try:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace(replacements)
        except Exception as e:
            print(f"[Warning] Failed replacing values in {col}: {e}")
        return self

    def safe_convert_dtype(self, col, dtype, errors="ignore"):
        """Convert column dtype safely."""
        try:
            if col in self.df.columns:
                if "datetime" in str(dtype):
                    self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                else:
                    self.df[col] = self.df[col].astype(dtype, errors=errors)
        except Exception as e:
            print(f"[Warning] Failed dtype conversion on {col}: {e}")
        return self

    def normalize_gender(self):
        """Unify transgender categories safely."""
        try:
            if "Gender" in self.df.columns:
                self.df["Gender"] = self.df["Gender"].replace({
                    "Transgender male to female": "Transgender",
                    "Transgender female to male": "Transgender"
                })
        except Exception as e:
            print(f"[Warning] Failed gender normalization: {e}")
        return self

    def split_race(self):
        """Split Race column into Race_1, Race_2, etc., if it exists."""
        try:
            if "Race" in self.df.columns:
                splitting = self.df["Race"].astype(str).str.split(";", expand=True)
                splitting.columns = [f"Race_{i+1}" for i in range(splitting.shape[1])]
                self.df = pd.concat([self.df.drop(columns=["Race"]), splitting], axis=1)
        except Exception as e:
            print(f"[Warning] Failed race splitting: {e}")
        return self

    def clean_salary(self):
        """Fix salary inconsistencies."""
        try:
            if "Salary" in self.df.columns:
                self.df["Salary"] = pd.to_numeric(self.df["Salary"], errors="coerce")
                self.df["Salary"] = self.df["Salary"].replace(60000, 28.84)
        except Exception as e:
            print(f"[Warning] Failed salary cleaning: {e}")
        return self

    def finalize(self):
        """Return cleaned dataframe."""
        return self.df
