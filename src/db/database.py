"""
database.py

SQLite Database Connection
"""

import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path="database/nifty100.db"):

        self.db_path = Path(db_path)

        # Create database directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = None

    def connect(self):
        """
        Open SQLite connection.
        """

        self.connection = sqlite3.connect(self.db_path)

        # Enable Foreign Keys
        self.connection.execute("PRAGMA foreign_keys = ON;")

        return self.connection

    def execute_script(self, sql_script):
        """
        Execute complete SQL script.
        """

        cursor = self.connection.cursor()

        cursor.executescript(sql_script)

        self.connection.commit()

    def execute(self, query, values=None):
        """
        Execute SQL query.
        """

        cursor = self.connection.cursor()

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        self.connection.commit()

        return cursor

    def close(self):

        if self.connection:

            self.connection.close()