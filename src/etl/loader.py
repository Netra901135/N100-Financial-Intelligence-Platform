"""
loader.py

Excel Loader for Nifty100 Financial Intelligence Platform

Responsibilities
----------------
1. Read all Excel datasets
2. Handle files with title rows
3. Clean column names
4. Remove empty rows
5. Remove duplicate rows
6. Normalize common columns
7. Return cleaned pandas DataFrames
"""

from pathlib import Path
import pandas as pd

from src.etl.normaliser import DataNormaliser


class ExcelLoader:
    """
    Excel Loader class for reading and cleaning datasets.
    """

    # Files having an extra title row before actual headers
    FILES_WITH_TITLE_ROW = {
        "companies.xlsx",
        "profitandloss.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "analysis.xlsx",
        "documents.xlsx",
        "prosandcons.xlsx",
    }

    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}"
            )

    # ======================================================
    # FILE UTILITIES
    # ======================================================

    def list_excel_files(self):
        """
        Return all Excel files in the data directory.
        """
        return sorted(self.data_dir.glob("*.xlsx"))

    def get_sheet_names(self, filename):
        """
        Return sheet names of an Excel workbook.
        """
        file_path = self.data_dir / filename

        workbook = pd.ExcelFile(file_path)

        return workbook.sheet_names

    # ======================================================
    # CLEANING FUNCTIONS
    # ======================================================

    @staticmethod
    def clean_column_names(df):
        """
        Standardize DataFrame column names.

        Example:
        Company Name -> company_name
        Net Profit (%) -> net_profit_percent
        """

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("%", "_percent", regex=False)
            .str.replace("/", "_", regex=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
        )

        return df

    @staticmethod
    def remove_empty_rows(df):
        """
        Remove rows where all columns are empty.
        """
        return df.dropna(how="all")

    @staticmethod
    def remove_duplicates(df):
        """
        Remove duplicate rows.
        """
        return df.drop_duplicates()

    def normalize_dataframe(self, df):
        """
        Apply normalization to common columns.
        """

        for column in df.columns:

            col = column.lower()

            # Normalize company ticker
            if col == "company_id":
                df[column] = df[column].apply(
                    DataNormaliser.normalize_company_id
                )

            # Normalize years
            elif "year" in col:
                df[column] = df[column].apply(
                    DataNormaliser.normalize_year
                )

            # Normalize dates
            elif "date" in col:
                df[column] = df[column].apply(
                    DataNormaliser.normalize_date
                )

            # Normalize URLs
            elif (
                "url" in col
                or "report" in col
                or "logo" in col
            ):
                df[column] = df[column].apply(
                    DataNormaliser.normalize_url
                )

        return df

    def clean_dataframe(self, df):
        """
        Apply all cleaning operations.
        """

        df = self.clean_column_names(df)

        df = self.remove_empty_rows(df)

        df = self.remove_duplicates(df)

        df = self.normalize_dataframe(df)

        df.reset_index(drop=True, inplace=True)

        return df

    # ======================================================
    # EXCEL LOADING
    # ======================================================

    def load_excel(self, filename):
        """
        Load a single Excel file.

        Parameters
        ----------
        filename : str

        Returns
        -------
        pandas.DataFrame
        """

        file_path = self.data_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        skip_rows = (
            1 if filename in self.FILES_WITH_TITLE_ROW else 0
        )

        df = pd.read_excel(file_path, skiprows=skip_rows)

        df = self.clean_dataframe(df)

        return df

    def load_all_files(self):
        """
        Load every Excel dataset.

        Returns
        -------
        dict
        """

        datasets = {}

        for file in self.list_excel_files():

            print(f"Loading {file.name}...")

            datasets[file.stem] = self.load_excel(file.name)

        return datasets

    # ======================================================
    # REPORTING
    # ======================================================

    @staticmethod
    def dataset_summary(datasets):
        """
        Print dataset summary.
        """

        print("\nDataset Summary")
        print("-" * 65)

        for name, df in datasets.items():

            print(
                f"{name:<20}"
                f"Rows: {len(df):<6}"
                f"Columns: {len(df.columns):<4}"
            )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    loader = ExcelLoader()

    datasets = loader.load_all_files()

    loader.dataset_summary(datasets)

    print("\nSample Data\n")

    for name, df in datasets.items():

        print("=" * 70)

        print(name.upper())

        print(df.head())

        print()