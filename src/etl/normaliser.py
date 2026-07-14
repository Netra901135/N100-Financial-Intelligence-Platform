"""
normaliser.py

Normalization utilities for the ETL pipeline.

Purpose:
--------
Convert inconsistent values into a standard format before
loading into the SQLite database.
"""

import re
from datetime import datetime
import pandas as pd


class DataNormaliser:

    @staticmethod
    def normalize_company_id(company_id):
        """
        Normalize company ticker.

        Examples:
        ---------
        abb
        ABB
        abb.ns

        becomes

        ABB
        """

        if pd.isna(company_id):
            return None

        company_id = str(company_id).strip().upper()

        company_id = company_id.replace(".NS", "")

        company_id = company_id.replace(".BO", "")

        return company_id

    @staticmethod
    def normalize_year(value):
        """
        Convert different year formats into an integer year.

        Examples
        --------
        Dec 2012 -> 2012
        Mar 2014 -> 2014
        Mar-13 -> 2013
        FY23 -> 2023
        2024 -> 2024
        """

        if pd.isna(value):
            return None

        value = str(value).strip()

        # Four-digit year
        match = re.search(r"(20\d{2}|19\d{2})", value)

        if match:
            return int(match.group())

        # Two-digit year
        match = re.search(r"-(\d{2})$", value)

        if match:
            return 2000 + int(match.group(1))

        match = re.search(r"FY(\d{2})", value.upper())

        if match:
            return 2000 + int(match.group(1))

        if value.isdigit():

            if len(value) == 4:
                return int(value)

            if len(value) == 2:
                return 2000 + int(value)

        return None

    @staticmethod
    def normalize_numeric(value):
        """
        Convert numbers into float.

        Handles commas and blanks.
        """

        if pd.isna(value):
            return None

        try:
            value = str(value).replace(",", "")

            return float(value)

        except Exception:

            return None

    @staticmethod
    def normalize_text(text):
        """
        Clean generic text.
        """

        if pd.isna(text):
            return None

        return " ".join(str(text).strip().split())

    @staticmethod
    def normalize_url(url):
        """
        Ensure URL starts with http:// or https://
        """

        if pd.isna(url):
            return None

        url = str(url).strip()

        if url.startswith("http://") or url.startswith("https://"):
            return url

        return "https://" + url

    @staticmethod
    def normalize_date(date_value):
        """
        Convert date into pandas datetime.
        """

        if pd.isna(date_value):
            return None

        try:

            return pd.to_datetime(date_value)

        except Exception:

            return None