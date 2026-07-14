"""
create_database.py

Creates nifty100.db using schema.sql
"""

from pathlib import Path

from src.db.database import Database


def main():

    print("=" * 60)
    print("Creating SQLite Database")
    print("=" * 60)

    db = Database()

    db.connect()

    schema_path = Path("db/schema.sql")

    if not schema_path.exists():

        raise FileNotFoundError(schema_path)

    with open(schema_path, "r", encoding="utf-8") as file:

        sql = file.read()

    db.execute_script(sql)

    db.close()

    print("\nDatabase created successfully!")

    print("\nLocation:")

    print("database/nifty100.db")


if __name__ == "__main__":
    main()