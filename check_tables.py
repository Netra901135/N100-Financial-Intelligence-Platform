import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

tables = [
    "profitandloss",
    "companies",
    "balancesheet",
    "cashflow"
]

for table in tables:
    print(f"\n{table.upper()} COLUMNS")
    print("-" * 40)

    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", conn)

    print(df.columns.tolist())

conn.close()