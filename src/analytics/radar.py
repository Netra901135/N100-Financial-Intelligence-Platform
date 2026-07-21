import os
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RadarChartGenerator:

    def __init__(self):

        self.db = "database/nifty100.db"
        self.conn = sqlite3.connect(self.db)

        self.df = None

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn
        )

        sector_df = pd.read_sql(
            """
            SELECT *
            FROM sectors
            """,
            self.conn
        )

        self.df = self.df.merge(
            sector_df,
            on="company_id",
            how="left"
        )

        peer_df = pd.read_excel(
            "data/raw/peer_groups.xlsx"
        )

        self.df = self.df.merge(
            peer_df,
            on="company_id",
            how="left"
        )

        latest_year = self.df["year"].max()

        self.df = self.df[
            self.df["year"] == latest_year
        ]

        self.df["peer_group_name"] = self.df["peer_group_name"].fillna(
            self.df["broad_sector"]
        )

        print("Radar data loaded.")
        print(f"Companies: {len(self.df)}")
        print(f"Latest year: {latest_year}")

        print(self.df.columns.tolist())

    def calculate_quality_score(self):

        self.df["composite_quality_score"] = 0

        # ROE
        self.df.loc[
            self.df["return_on_equity_pct"] >= 20,
            "composite_quality_score"
        ] += 20

        # ROCE
        self.df.loc[
            self.df["return_on_capital_employed_pct"] >= 20,
            "composite_quality_score"
        ] += 20

        # Net Profit Margin
        self.df.loc[
            self.df["net_profit_margin_pct"] >= 15,
            "composite_quality_score"
        ] += 15

        # Debt to Equity
        self.df.loc[
            self.df["debt_to_equity"] <= 0.5,
            "composite_quality_score"
        ] += 15

        # Interest Coverage
        self.df.loc[
            self.df["interest_coverage"] >= 5,
            "composite_quality_score"
        ] += 10

        # Revenue CAGR
        self.df.loc[
            self.df["revenue_cagr_5yr"] >= 10,
            "composite_quality_score"
        ] += 10

        # PAT CAGR
        self.df.loc[
            self.df["pat_cagr_5yr"] >= 10,
            "composite_quality_score"
        ] += 10

        print("Composite quality scores calculated.")

        print(
            self.df[
                [
                    "company_id",
                    "composite_quality_score"
                ]
            ].head()
        )

    def normalize_metrics(self):

        self.metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow",
            "pat_cagr_5yr",
            "revenue_cagr_5yr",
            "composite_quality_score",
        ]

        for metric in self.metrics:

            minimum = self.df[metric].min()
            maximum = self.df[metric].max()

            if maximum == minimum:

                self.df[f"{metric}_norm"] = 50

            else:

                self.df[f"{metric}_norm"] = (
                    (
                        self.df[metric] - minimum
                    )
                    /
                    (
                        maximum - minimum
                    )
                ) * 100

            # Lower Debt/Equity is better
            if metric == "debt_to_equity":

                self.df[f"{metric}_norm"] = (
                    100 - self.df[f"{metric}_norm"]
                )

        print("Metrics normalized.")

        print(
            self.df[
                [
                    "company_id",
                    "return_on_equity_pct_norm",
                    "debt_to_equity_norm",
                    "composite_quality_score_norm",
                ]
            ].head()
        )

    def generate_radar_chart(self, company_id):
        row = self.df[self.df["company_id"] == company_id]
        if row.empty:
            print(f"{company_id} not found.")
            return

        row = row.iloc[0]

        peer_group = row["peer_group_name"]

        peer_df = self.df[
            self.df["peer_group_name"] == peer_group
        ]

        metrics = [
            "return_on_equity_pct_norm",
            "return_on_capital_employed_pct_norm",
            "net_profit_margin_pct_norm",
            "debt_to_equity_norm",
            "free_cash_flow_norm",
            "pat_cagr_5yr_norm",
            "revenue_cagr_5yr_norm",
            "composite_quality_score_norm"
        ]

        labels = [
            "ROE",
            "ROCE",
            "NPM",
            "Debt/Equity",
            "FCF",
            "PAT CAGR",
            "Revenue CAGR",
            "Composite"
        ]

        company_values = row[metrics].values.astype(float)
        peer_values = peer_df[metrics].mean().values.astype(float)

        company_values = np.append(company_values, company_values[0])
        peer_values = np.append(peer_values, peer_values[0])

        angles = np.linspace(
            0,
            2 * np.pi,
            len(labels),
            endpoint=False
        )

        angles = np.append(angles, angles[0])

        fig, ax = plt.subplots(
            figsize=(8, 8),
            subplot_kw=dict(polar=True)
        )

        ax.plot(
            angles,
            company_values,
            linewidth=2,
            label=company_id
        )

        ax.fill(
            angles,
            company_values,
            alpha=0.25
        )

        ax.plot(
            angles,
            peer_values,
            linestyle="--",
            linewidth=2,
            label="Peer Average"
        )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        ax.set_ylim(0, 100)

        ax.set_title(company_id)

        ax.legend(loc="upper right")

        os.makedirs(
            "output/reports/radar_charts",
            exist_ok=True
        )

        plt.savefig(
            f"output/reports/radar_charts/{company_id}_radar.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Saved {company_id}_radar.png")
    def generate_all_radar_charts(self):

        companies = (
            self.df["company_id"]
            .dropna()
            .unique()
        )

        print(f"Generating radar charts for {len(companies)} companies...")

        for company in sorted(companies):

            try:
                self.generate_radar_chart(company)

            except Exception as e:
                print(f"Failed: {company} -> {e}")

        print("All radar charts generated.")
def main():

    radar = RadarChartGenerator()

    radar.load_data()

    radar.calculate_quality_score()

    radar.normalize_metrics()
    radar.generate_radar_chart("TCS")
    radar.generate_all_radar_charts()
if __name__ == "__main__":
    main()