"""
validator.py

Data Quality Validator
N100 Financial Intelligence Platform
"""

from pathlib import Path
import pandas as pd


class DataValidator:

    def __init__(self):
        self.failures = []

    # =====================================================
    # Utility
    # =====================================================

    def add_failure(
        self,
        rule,
        severity,
        table,
        company_id,
        year,
        column,
        value,
        message,
    ):

        self.failures.append(
            {
                "rule": rule,
                "severity": severity,
                "table": table,
                "company_id": company_id,
                "year": year,
                "column": column,
                "value": value,
                "message": message,
            }
        )

    # =====================================================
    # Companies
    # =====================================================

    def validate_companies(self, companies):

        table = "companies"

        # Missing ID

        missing = companies[companies["id"].isna()]

        for _, row in missing.iterrows():

            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table,
                "",
                "",
                "id",
                "",
                "Company ID missing",
            )

        # Duplicate IDs

        duplicate = companies[
            companies["id"].duplicated(keep=False)
        ]

        for _, row in duplicate.iterrows():

            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table,
                row["id"],
                "",
                "id",
                row["id"],
                "Duplicate Company ID",
            )

        # Logo URL

        if "company_logo" in companies.columns:

            invalid = companies[
                companies["company_logo"].notna()
            ]

            invalid = invalid[
                ~invalid["company_logo"]
                .str.startswith(("http://", "https://"))
            ]

            for _, row in invalid.iterrows():

                self.add_failure(
                    "DQ-10",
                    "WARNING",
                    table,
                    row["id"],
                    "",
                    "company_logo",
                    row["company_logo"],
                    "Invalid company logo URL",
                )

    # =====================================================
    # Profit & Loss
    # =====================================================

    def validate_profitandloss(self, pnl):

        table = "profitandloss"

        required = [
            "company_id",
        ]

        for column in required:

            if column not in pnl.columns:
                continue

            missing = pnl[
                pnl[column].isna()
            ]

            for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-02",
                    "CRITICAL",
                    table,
                    row.get("company_id", ""),
                    row.get("year", ""),
                    column,
                    "",
                    f"{column} missing",
                )

        # Sales

        if "sales" in pnl.columns:

            invalid_sales = pnl[
                pnl["sales"].notna()
            ]

            invalid_sales = invalid_sales[
                invalid_sales["sales"] <= 0
            ]

            for _, row in invalid_sales.iterrows():

                self.add_failure(
                    "DQ-06",
                    "WARNING",
                    table,
                    row["company_id"],
                    row["year"],
                    "sales",
                    row["sales"],
                    "Sales should be positive",
                )
                    # =====================================================
    # Balance Sheet
    # =====================================================

    def validate_balancesheet(self, bs):

        table = "balancesheet"

        required = [
            "company_id",
            "year",
            "total_assets",
            "total_liabilities"
        ]

        for column in required:

            if column not in bs.columns:
                continue

            missing = bs[bs[column].isna()]

            for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-03",
                    "CRITICAL",
                    table,
                    row.get("company_id", ""),
                    row.get("year", ""),
                    column,
                    "",
                    f"{column} missing"
                )

        # Assets should approximately equal liabilities

        if "total_assets" in bs.columns:

            invalid_assets = bs[
                bs["total_assets"].notna()
            ]

            invalid_assets = invalid_assets[
                invalid_assets["total_assets"] <= 0
            ]

            for _, row in invalid_assets.iterrows():

                self.add_failure(
                    "DQ-04",
                    "WARNING",
                    table,
                    row["company_id"],
                    row["year"],
                    "total_assets",
                    row["total_assets"],
                    "Total Assets should be greater than zero"
                )
               

    # =====================================================
    # Cash Flow
    # =====================================================

    def validate_cashflow(self, cf):

        table = "cashflow"

        required = [
            "company_id",
            "year",
        ]

        for column in required:

            if column not in cf.columns:
                continue

            missing = cf[
                cf[column].isna()
            ]

            for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-05",
                    "CRITICAL",
                    table,
                    row.get("company_id", ""),
                    row.get("year", ""),
                    column,
                    "",
                    f"{column} missing"
                )

                # ---------------------------------------------
        # Net Cash Flow should not be missing
        # ---------------------------------------------

        if "net_cash_flow" in cf.columns:

            missing_cash = cf[
                cf["net_cash_flow"].isna()
            ]

            for _, row in missing_cash.iterrows():

                self.add_failure(
                    "DQ-07",
                    "WARNING",
                    table,
                    row.get("company_id", ""),
                    row.get("year", ""),
                    "net_cash_flow",
                    "",
                    "Net Cash Flow is missing"
                )
                

    # =====================================================
    # Documents
    # =====================================================

    def validate_documents(self, docs):

        table = "documents"

        if "annual_report" not in docs.columns:
            return

        valid_docs = docs[
            docs["annual_report"].notna()
        ]

        invalid = valid_docs[
            ~valid_docs["annual_report"]
            .str.startswith(("http://", "https://"))
        ]

        for _, row in invalid.iterrows():

            self.add_failure(
                "DQ-10",
                "WARNING",
                table,
                row["company_id"],
                row["year"],
                "annual_report",
                row["annual_report"],
                "Invalid Annual Report URL"
            )

    # =====================================================
    # Analysis
    # =====================================================

    def validate_analysis(self, analysis):

        table = "analysis"

        if "company_id" not in analysis.columns:
            return

        missing = analysis[
            analysis["company_id"].isna()
        ]

        for _, row in missing.iterrows():

            self.add_failure(
                "DQ-11",
                "CRITICAL",
                table,
                "",
                "",
                "company_id",
                "",
                "Company ID missing"
            )
                # =====================================================
    # Financial Ratios
    # =====================================================

    def validate_financial_ratios(self, ratios):

        table = "financial_ratios"
        if "company_id" not in ratios.columns:
            return
        missing = ratios[ratios[ "company_id"].isna()]

        for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-12",
                    "WARNING",
                    table,
                    row.get("company_id", ""),
                    row.get("year", ""),
                     "company_id",
                    "",
                    "company_id missing"
                )


    # =====================================================
    # Peer Groups
    # =====================================================

       # =====================================================
    # Peer Groups
    # =====================================================

    def validate_peer_groups(self, peer):

        table = "peer_groups"

        required = [
            "peer_group_name",
            "company_id"
        ]

        # Check missing required values
        for column in required:

            if column not in peer.columns:
                continue

            missing = peer[
                peer[column].isna()
            ]

            for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-13",
                    "WARNING",
                    table,
                    row.get("company_id", ""),
                    "",
                    column,
                    "",
                    f"{column} missing"
                )

        # Check duplicate peer group + company combination
        if (
            "peer_group_name" in peer.columns and
            "company_id" in peer.columns
        ):

            duplicates = peer[
                peer.duplicated(
                    subset=["peer_group_name", "company_id"],
                    keep=False
                )
            ]

            for _, row in duplicates.iterrows():

                self.add_failure(
                    "DQ-13",
                    "WARNING",
                    table,
                    row["company_id"],
                    "",
                    "peer_group_name",
                    row["peer_group_name"],
                    "Duplicate company in peer group"
                )
    # =====================================================
    # Sectors
    # =====================================================

    def validate_sectors(self, sectors):

        table = "sectors"

        required = [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]

        for column in required:

            if column not in sectors.columns:
                continue

            missing = sectors[
                sectors[column].isna()
            ]

            for _, row in missing.iterrows():

                self.add_failure(
                    "DQ-14",
                    "WARNING",
                    table,
                    row.get("company_id", ""),
                    "",
                    column,
                    "",
                    f"{column} missing"
                )

    # =====================================================
    # Stock Prices
    # =====================================================

    def validate_stock_prices(self, prices):

        table = "stock_prices"

        numeric_columns = [
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "adjusted_close"
        ]

        for column in numeric_columns:

            if column not in prices.columns:
                continue

            invalid = prices[
                prices[column].notna()
            ]

            invalid = invalid[
                invalid[column] <= 0
            ]

            for _, row in invalid.iterrows():

                self.add_failure(
                    "DQ-15",
                    "WARNING",
                    table,
                    row["company_id"],
                    row["date"],
                    column,
                    row[column],
                    f"{column} should be positive"
                )

        if "volume" in prices.columns:

            invalid = prices[
                prices["volume"].notna()
            ]

            invalid = invalid[
                invalid["volume"] < 0
            ]

            for _, row in invalid.iterrows():

                self.add_failure(
                    "DQ-15",
                    "WARNING",
                    table,
                    row["company_id"],
                    row["date"],
                    "volume",
                    row["volume"],
                    "Negative Volume"
                )

    # =====================================================
    # Foreign Keys
    # =====================================================

    def validate_foreign_keys(self, dataframe, table, companies):

        if "company_id" not in dataframe.columns:
            return

        valid = set(
            companies["id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df = dataframe.copy()

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        invalid = df[
            ~df["company_id"].isin(valid)
        ]

        for _, row in invalid.iterrows():

            self.add_failure(
                "DQ-16",
                "CRITICAL",
                table,
                row["company_id"],
                row["year"] if "year" in row.index else "",
                "company_id",
                row["company_id"],
                "Company ID not found"
            )

    # =====================================================
    # Save Report
    # =====================================================

    def save_report(self):

        Path("output").mkdir(exist_ok=True)

        report = pd.DataFrame(self.failures)

        report.to_csv(
            "output/validation_failures.csv",
            index=False
        )

        print("\nValidation Completed")
        print("-" * 60)
        print(f"Total Issues : {len(report)}")

        if report.empty:

            print("No validation issues found.")

        else:

            print(report["severity"].value_counts().to_string())
            print("\nRule Summary")
            
            print(report["rule"].value_counts().to_string())

        return report