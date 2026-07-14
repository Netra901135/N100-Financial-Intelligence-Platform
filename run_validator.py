"""
run_validator.py

Run all Data Quality validations
"""

from src.etl.loader import ExcelLoader
from src.etl.validator import DataValidator


def main():

    print("=" * 70)
    print("N100 Financial Intelligence Platform")
    print("Sprint 1 - Data Quality Validation")
    print("=" * 70)

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------

    loader = ExcelLoader()

    datasets = loader.load_all_files()

    print("\nDatasets Loaded Successfully")

    # --------------------------------------------------
    # Create Validator
    # --------------------------------------------------

    validator = DataValidator()

    # --------------------------------------------------
    # Companies
    # --------------------------------------------------

    if "companies" in datasets:
        validator.validate_companies(
            datasets["companies"]
        )

    # --------------------------------------------------
    # Profit & Loss
    # --------------------------------------------------

    if "profitandloss" in datasets:
        validator.validate_profitandloss(
            datasets["profitandloss"]
        )

    # --------------------------------------------------
    # Balance Sheet
    # --------------------------------------------------

    if "balancesheet" in datasets:
        validator.validate_balancesheet(
            datasets["balancesheet"]
        )

    # --------------------------------------------------
    # Cash Flow
    # --------------------------------------------------

    if "cashflow" in datasets:
        validator.validate_cashflow(
            datasets["cashflow"]
        )

    # --------------------------------------------------
    # Analysis
    # --------------------------------------------------

    if "analysis" in datasets:
        validator.validate_analysis(
            datasets["analysis"]
        )

    # --------------------------------------------------
    # Documents
    # --------------------------------------------------

    if "documents" in datasets:
        validator.validate_documents(
            datasets["documents"]
        )

    # --------------------------------------------------
    # Financial Ratios
    # --------------------------------------------------

    if "financial_ratios" in datasets:
        validator.validate_financial_ratios(
            datasets["financial_ratios"]
        )

    # --------------------------------------------------
    # Peer Groups
    # --------------------------------------------------

    if "peer_groups" in datasets:
        validator.validate_peer_groups(
            datasets["peer_groups"]
        )

    # --------------------------------------------------
    # Sectors
    # --------------------------------------------------

    if "sectors" in datasets:
        validator.validate_sectors(
            datasets["sectors"]
        )

    # --------------------------------------------------
    # Stock Prices
    # --------------------------------------------------

    if "stock_prices" in datasets:
        validator.validate_stock_prices(
            datasets["stock_prices"]
        )

    # --------------------------------------------------
    # Foreign Key Validation
    # --------------------------------------------------

    

    
    # --------------------------------------------------
    # Save Report
    # --------------------------------------------------

    report = validator.save_report()

    print("\nValidation Finished Successfully")

    print(f"\nTotal Issues Found : {len(report)}")

    print("\nReport saved to:")

    print("output/validation_failures.csv")

    print("\nDone.")


if __name__ == "__main__":
    main()