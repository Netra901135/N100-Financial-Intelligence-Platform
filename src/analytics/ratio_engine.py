"""
ratio_engine.py

Sprint 2
Financial Ratio Engine

Reads data from SQLite,
calculates KPIs,
updates financial_ratios table.
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)

class RatioEngine:

    def __init__(self):

        self.db_path = Path("database/nifty100.db")

        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()

        logging.basicConfig(

            filename="output/ratio_edge_cases.log",

            level=logging.INFO,

            filemode="w",

            format="%(message)s",

        )

    def load_tables(self):

        self.pnl = pd.read_sql(

            "SELECT * FROM profitandloss",

            self.connection,

        )

        self.bs = pd.read_sql(

            "SELECT * FROM balancesheet",

            self.connection,

        )

        self.cf = pd.read_sql(

            "SELECT * FROM cashflow",

            self.connection,

        )

        self.companies = pd.read_sql(

            "SELECT * FROM companies",

            self.connection,

        )
        
        self.sectors = pd.read_sql(

            "SELECT * FROM sectors",

            self.connection,

        )

        print("SQLite tables loaded.")

    def prepare_dataset(self):
        # Remove duplicate id columns before merging
        pnl = self.pnl.drop(columns=["id"], errors="ignore")
        bs = self.bs.drop(columns=["id"], errors="ignore")
        cf = self.cf.drop(columns=["id"], errors="ignore")

        sectors = self.sectors.drop(columns=["id"], errors="ignore")
        # Merge Profit & Loss + Balance Sheet
        df = pnl.merge(
            bs,
        on=["company_id", "year"],
        how="inner",
        )
        # Merge Cash Flow
        df = df.merge(
        cf,
        on=["company_id", "year"],
        how="inner",
        )
        # Merge Sector
        df = df.merge(
        sectors,
        on="company_id",
        how="left",
        )
        
        self.df = df
        print(f"Prepared {len(df)} company-year records.")

    def apply_financials_carveout(self):

        self.ratio_df["high_leverage_flag"] = self.ratio_df.apply(

            lambda row:

            False

            if row["broad_sector"] == "Financials"

            else (

                row["debt_to_equity"] > 5

                if row["debt_to_equity"] is not None

                else False

            ),

            axis=1,

        )

        print("Financial carve-out completed.")


    def calculate_ratios(self):
        df = self.df.copy()
        # -------------------------
    # Profitability
    # -------------------------

        df["net_profit_margin_pct"] = df.apply(
            lambda r: net_profit_margin(
                r["net_profit"],
                r["sales"],
            ),
            axis=1,
        )

        df["operating_profit_margin_pct"] = df.apply(
            lambda r: operating_profit_margin(
                r["operating_profit"],
                r["sales"],
            ),
            axis=1,
        )

        df["return_on_equity_pct"] = df.apply(
            lambda r: return_on_equity(
                r["net_profit"],
                r["equity_capital"],
                r["reserves"],
            ),
            axis=1,
        )
        df["return_on_capital_employed_pct"] = df.apply(
            lambda r: return_on_capital_employed(
                r["operating_profit"],
                r["equity_capital"],
                r["reserves"],
                r["borrowings"],
            ),
            axis=1,
        )
        df["return_on_assets_pct"] = df.apply(
            lambda r: return_on_assets(
                r["net_profit"],
                r["total_assets"],
            ),
            axis=1,
        )

        # -------------------------
    # Leverage
    # -------------------------
        df["debt_to_equity"] = df.apply(
        lambda r: debt_to_equity(
            r["borrowings"],
            r["equity_capital"],
            r["reserves"],
        ),
        axis=1,
        )

        df["interest_coverage"] = df.apply(
        lambda r: interest_coverage_ratio(
            r["operating_profit"],
            r["other_income"],
            r["interest"],
        ),
        axis=1,
        )

        df["asset_turnover"] = df.apply(
        lambda r: asset_turnover(
            r["sales"],
            r["total_assets"],
        ),
        axis=1,
        )

        # -------------------------
        # Cash Flow
        #  -------------------------

        df["free_cash_flow"] = df.apply(
        lambda r: free_cash_flow(
            r["operating_activity"],
            r["investing_activity"],
        ),
        axis=1,
        )
        df["cfo_pat_ratio"] = (
            df["operating_activity"] /
            df["net_profit"]
        )
        
        df.loc[
            df["net_profit"] == 0,
            "cfo_pat_ratio",
        ] = None
        df["sales"] = df["sales"]
        df["dividend_payout"] = df["dividend_payout"]
        # Create CAGR columns
        df["revenue_cagr_3yr"] = None
        df["revenue_cagr_5yr"] = None
        df["pat_cagr_5yr"] = None
        df["eps_cagr_5yr"] = None
        df["fcf_cagr_5yr"] = None
        df["debt_to_equity_declining"] = False
        
        for company_id, company_df in df.groupby("company_id"):
            company_df = company_df.sort_values("year").drop_duplicates(subset="year", keep="last")
            declining = False
            if len(company_df) >= 2:
                previous_de = company_df.iloc[-2]["debt_to_equity"]
                current_de = company_df.iloc[-1]["debt_to_equity"]
                if pd.notna(previous_de) and pd.notna(current_de):
                    declining = current_de < previous_de
                if company_id == "ABB":
                    print(company_df[["year", "debt_to_equity"]])
                    print(
                        f"Previous: {previous_de}, "
                        f"Current: {current_de}, "
                        f"Declining: {declining}"
                    )
            if len(company_df) < 2:
                continue
            latest = company_df.iloc[-1]
            
            target_year = latest["year"] - 5
            
            historical = company_df[
                company_df["year"] == target_year
            ]
            
            if historical.empty:
                historical = company_df.iloc[[0]]
                
            historical = historical.iloc[0]
            
            years = latest["year"] - historical["year"]
            
            if years <= 0:
                continue
            
            revenue_value, _ = revenue_cagr(
                historical["sales"],
                latest["sales"],
                years,
            )
            # ---------------------------------
# Revenue CAGR (3-Year)
# ---------------------------------
            target_year_3 = latest["year"] - 3
            historical_3 = company_df[
                company_df["year"] == target_year_3
            ]
            
            if historical_3.empty:
                revenue_3_value = None
            else:
                historical_3 = historical_3.iloc[0]
                years_3 = latest["year"] - historical_3["year"]
                revenue_3_value, _ = revenue_cagr(
                    historical_3["sales"],
                    latest["sales"],
                    years_3,
                )

            pat_value, _ = pat_cagr(
                historical["net_profit"],
                latest["net_profit"],
                years,
            )
            fcf_value, _ = revenue_cagr(
                historical["free_cash_flow"],
                latest["free_cash_flow"],
                years,
            )
            if "eps" in df.columns:
                eps_value, _ = eps_cagr(
                    historical["eps"],
                    latest["eps"],
                    years,
                )
            else:
                eps_value = None
            
            latest_mask = (
                (df["company_id"] == company_id)
                & (df["year"] == latest["year"])
            )    
            df.loc[
                latest_mask,
                "revenue_cagr_5yr",
            ] = revenue_3_value
            df.loc[
                latest_mask,
                "revenue_cagr_3yr",
            ] = revenue_value
            df.loc[
                latest_mask,
                "pat_cagr_5yr",
            ] = pat_value
            
            df.loc[
                latest_mask,
                "eps_cagr_5yr",
            ] = eps_value
            df.loc[
                latest_mask,
                "debt_to_equity_declining",
            ] = declining
            df.loc[
                latest_mask,
                "fcf_cagr_5yr",
            ] = fcf_value
        self.ratio_df = df
        print(self.ratio_df.columns.tolist())
        print("KPI calculation completed.")

    def save_financial_ratios(self):
        cols = [
            "company_id",
            "year",
            "sales",
            "dividend_payout",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "return_on_assets_pct",
            "debt_to_equity_declining",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow",
            "revenue_cagr_5yr",
            "revenue_cagr_3yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "cfo_pat_ratio",
            "fcf_cagr_5yr",
        ]
        
        output = self.ratio_df[cols].copy()
        output.to_sql(
        "financial_ratios",
        self.connection,
        if_exists="replace",
        index=False,
        )
        print(f"Saved {len(output)} rows to financial_ratios table.")

    def validate_roce(self):
        if "return_on_capital_employed_pct" not in self.ratio_df.columns:
            print("ROCE not calculated yet.")
            return

        for _, row in self.ratio_df.iterrows():
            source = row["roce_percentage"]
            calculated = row["return_on_capital_employed_pct"]
            if pd.isna(source):
                continue
            if pd.isna(calculated):
                continue

            difference = abs(source - calculated)
            if difference > 5:
                logging.info(
                    f"{row['company_id']} "

                    f"{row['year']} "

                    f"ROCE "

                    f"Source={source} "

                    f"Calculated={calculated} "

                    f"Category=FORMULA_DIFFERENCE"
                    
                )

        print("ROCE validation completed.")

def main():

    engine = RatioEngine()

    engine.load_tables()

    engine.prepare_dataset()

    engine.calculate_ratios()

    engine.save_financial_ratios()
    engine.apply_financials_carveout()

    print("Ratio engine completed successfully.")

if __name__ == "__main__":
    main()