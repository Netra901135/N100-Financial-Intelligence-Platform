import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class PeerEngine:

    def __init__(self):

        self.db = Path("database/nifty100.db")
        self.conn = sqlite3.connect(self.db)

    def load_data(self):

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

        self.sectors = pd.read_sql(
            "SELECT * FROM sectors",
            self.conn,
        )

        self.df = self.df.merge(
            self.sectors,
            on="company_id",
            how="left",
        )
        missing_sector = self.df[self.df["broad_sector"].isna()]
        print(f"Companies missing sector: {missing_sector['company_id'].nunique()}")
        print(
            missing_sector["company_id"]
            .drop_duplicates()
            .sort_values()
        )

        self.peer_groups = pd.read_excel(
            "data/raw/peer_groups.xlsx"
        )
        print(self.peer_groups.head())
        print(self.peer_groups.columns.tolist())
        print(f"Rows in peer_groups.xlsx: {len(self.peer_groups)}")
        
        self.df = self.df.merge(
            self.peer_groups,
            on="company_id",
            how="left",
        )
# Fill missing peer groups with broad sector
        self.df["peer_group_name"] = self.df["peer_group_name"].fillna(
            self.df["broad_sector"]
)
        missing = self.df[self.df["peer_group_name"].isna()]
        print(f"Missing peer groups: {len(missing)}")
        print(
            missing[
                ["company_id", "broad_sector"]
            ].sort_values("company_id")
        )
        # Keep only latest financial year
        self.df = (
            self.df.sort_values("year")
            .groupby("company_id", as_index=False)
            .tail(1)
        )

        print("Peer data loaded.")

    def calculate_quality_score(self):

        self.df["composite_quality_score"] = 0

        self.df.loc[
            self.df["return_on_equity_pct"] >= 20,
            "composite_quality_score",
        ] += 20

        self.df.loc[
            self.df["return_on_capital_employed_pct"] >= 20,
            "composite_quality_score",
        ] += 20

        self.df.loc[
            self.df["net_profit_margin_pct"] >= 15,
            "composite_quality_score",
        ] += 15

        self.df.loc[
            self.df["operating_profit_margin_pct"] >= 20,
            "composite_quality_score",
        ] += 15

        self.df.loc[
            self.df["debt_to_equity"] <= 0.5,
            "composite_quality_score",
        ] += 10

        self.df.loc[
            self.df["interest_coverage"] >= 5,
            "composite_quality_score",
        ] += 10

        self.df.loc[
            self.df["asset_turnover"] >= 1,
            "composite_quality_score",
        ] += 5

        self.df.loc[
            self.df["free_cash_flow"] > 0,
            "composite_quality_score",
        ] += 5

    def get_company_sector(self, company_id):

        company = self.df[
            self.df["company_id"] == company_id
        ]

        if company.empty:
            print(f"{company_id} not found.")
            return None

        sector = company.iloc[0]["broad_sector"]

        if pd.isna(sector):
            print(f"No sector information found for {company_id}.")
            return None

        print(f"\nCompany : {company_id}")
        print(f"Sector  : {sector}")

        return sector

    def compare_peers(self, company_id):

        sector = self.get_company_sector(company_id)

        if sector is None:
            return None

        peers = self.df[
            self.df["broad_sector"] == sector
        ].copy()

        peers = peers.sort_values(
            by="composite_quality_score",
            ascending=False,
        )

        columns = [
            "company_id",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow",
            "composite_quality_score",
        ]

        print("\n" + "=" * 100)
        print(f"TOP PEERS IN {sector.upper()}")
        print("=" * 100)

        print(
            peers[columns]
            .reset_index(drop=True)
        )

        print(f"\nTotal Peers : {len(peers)}")

        return peers

    def export_peers(self, peers, filename):

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        peers.to_csv(output_path, index=False)

        print(f"\nReport saved to {output_path}")

    def plot_quality_scores(self, peers):

        plt.figure(figsize=(10, 6))

        plt.bar(
            peers["company_id"],
            peers["composite_quality_score"],
        )

        plt.title("Composite Quality Score")
        plt.xlabel("Company")
        plt.ylabel("Score")

        plt.xticks(rotation=45)

        plt.tight_layout()

        output = Path("output/charts")
        output.mkdir(parents=True, exist_ok=True)

        plt.savefig(output / "quality_scores.png")

        plt.close()

        print("Quality Score chart saved.")

    def plot_roe(self, peers):

        plt.figure(figsize=(10, 6))

        plt.bar(
            peers["company_id"],
            peers["return_on_equity_pct"],
        )

        plt.title("Return on Equity")

        plt.xlabel("Company")

        plt.ylabel("ROE (%)")

        plt.xticks(rotation=45)

        plt.tight_layout()

        output = Path("output/charts")
        output.mkdir(parents=True, exist_ok=True)

        plt.savefig(output / "roe.png")

        plt.close()

        print("ROE chart saved.")

    def plot_roce(self, peers):

        plt.figure(figsize=(10, 6))

        plt.bar(
            peers["company_id"],
            peers["return_on_capital_employed_pct"],
        )

        plt.title("Return on Capital Employed")

        plt.xlabel("Company")

        plt.ylabel("ROCE (%)")

        plt.xticks(rotation=45)

        plt.tight_layout()

        output = Path("output/charts")
        output.mkdir(parents=True, exist_ok=True)

        plt.savefig(output / "roce.png")

        plt.close()

        print("ROCE chart saved.")

    def plot_fcf(self, peers):

        plt.figure(figsize=(10, 6))

        plt.bar(
            peers["company_id"],
            peers["free_cash_flow"],
        )

        plt.title("Free Cash Flow")

        plt.xlabel("Company")

        plt.ylabel("₹ Crore")

        plt.xticks(rotation=45)

        plt.tight_layout()

        output = Path("output/charts")
        output.mkdir(parents=True, exist_ok=True)

        plt.savefig(output / "free_cash_flow.png")

        plt.close()

        print("Free Cash Flow chart saved.")
        
        print(self.df.columns.tolist())

    def calculate_percentiles(self):
        metrics = {
            "return_on_equity_pct": False,
            "return_on_capital_employed_pct": False,
            "net_profit_margin_pct": False,
            "debt_to_equity": True,
            "free_cash_flow": False,
            "revenue_cagr_5yr": False,
            "pat_cagr_5yr": False,
            "eps_cagr_5yr": False,
            "interest_coverage": False,
            "asset_turnover": False,
        }
        for metric, inverse in metrics.items():
            if inverse:
                self.df[f"{metric}_percentile"] = (
                    self.df.groupby("peer_group_name")[metric]
                    .rank(method="average", pct=True, ascending=True)
                    * 100
                )

            else:
                self.df[f"{metric}_percentile"] = (
                    self.df.groupby("peer_group_name")[metric]
                    .rank(method="average", pct=True, ascending=True)
                    * 100
                )
        

        print("Percentile ranking completed.")
        cols = [
            "company_id",
            "peer_group_name",
            "return_on_equity_pct",
            "return_on_equity_pct_percentile",
        ]
        print(
            self.df.sort_values(
                "return_on_equity_pct",
                ascending=False
                )[cols].head(10)
            )
    def save_percentiles(self):
        metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "interest_coverage",
            "asset_turnover",
        ]

        records = []
        for _, row in self.df.iterrows():
            for metric in metrics:
                records.append(
                    {
                        "company_id": row["company_id"],
                        "peer_group_name": row["peer_group_name"],
                        "metric": metric,
                        "value": row[metric],
                        "percentile_rank": row[f"{metric}_percentile"],
                        "year": row["year"],
                    }
                )

        peer_df = pd.DataFrame(records)
        peer_df.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="replace",
            index=False,
        )

        print(f"Saved {len(peer_df)} records to peer_percentiles.")
def main():

    engine = PeerEngine()

    engine.load_data()

    engine.calculate_quality_score()

    peers = engine.compare_peers("TCS")

    if peers is not None:

        engine.export_peers(
            peers,
            "output/reports/tcs_peer_report.csv",
        )

        engine.plot_quality_scores(peers)

        engine.plot_roe(peers)

        engine.plot_roce(peers)

        engine.plot_fcf(peers)
        engine.load_data()
        engine.calculate_percentiles()
        print([c for c in engine.df.columns if "percentile" in c])
        engine.save_percentiles()
        print(engine.df.columns.tolist())
if __name__ == "__main__":
    main()