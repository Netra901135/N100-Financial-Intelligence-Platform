"""
load_database.py

Loads all cleaned Excel datasets into SQLite.
"""

from pathlib import Path
import pandas as pd



from src.etl.loader import ExcelLoader
from src.db.database import Database

class DatabaseLoader:

    def __init__(self):

        self.loader = ExcelLoader()

        self.db = Database()

        self.connection = self.db.connect()

        Path("output").mkdir(exist_ok=True)

        self.audit = []

    def insert_table(self, table_name, dataframe):

        dataframe.to_sql(

            table_name,

            self.connection,

            if_exists="append",

            index=False,

        )

        self.audit.append(

            {

                "table": table_name,

                "rows_loaded": len(dataframe),

                "rejected_rows": 0,

            }

        )

        print(f"Loaded {table_name:<20} {len(dataframe)} rows")    
    
    def load_all_tables(self):

        datasets = self.loader.load_all_files()

        load_order = [

            "companies",

            "analysis",

            "sectors",

            "documents",

            "prosandcons",

            "peer_groups",

            "profitandloss",

            "balancesheet",

            "cashflow",

            "financial_ratios",

            "stock_prices",

        ]

        print("\nLoading tables into SQLite...\n")

        for table in load_order:

            if table not in datasets:

                print(f"{table} not found.")

                continue

            df = datasets[table]

            self.insert_table(table, df)

        print("\nAll tables loaded successfully.")

    def save_audit(self):

        audit_df = pd.DataFrame(self.audit)

        audit_file = Path("output/load_audit.csv")

        audit_df.to_csv(

            audit_file,

            index=False

        )

        print("\nLoad Audit Saved")

        print(audit_df)

    def close(self):

        self.connection.close()

def main():

    print("=" * 60)

    print("Loading Data into SQLite")

    print("=" * 60)

    loader = DatabaseLoader()

    loader.load_all_tables()

    loader.save_audit()

    loader.close()

    print("\nDatabase loading completed successfully.")


if __name__ == "__main__":

    main()