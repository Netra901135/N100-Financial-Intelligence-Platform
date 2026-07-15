"""
ratios.py

Financial Ratio Engine

Sprint 2 - Day 08
"""

from typing import Optional

def net_profit_margin(
    net_profit: float,
    sales: float
) -> Optional[float]:
    """
    Net Profit Margin (%)

    Formula:
        Net Profit / Sales × 100

    Returns None if Sales <= 0
    """

    if sales is None or sales <= 0:
        return None

    return round((net_profit / sales) * 100, 2)

def operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:
    """
    Operating Profit Margin (%)

    Formula:
        Operating Profit / Sales × 100
    """

    if sales is None or sales <= 0:
        return None

    return round((operating_profit / sales) * 100, 2)

def opm_cross_check(
    calculated_opm: float,
    source_opm: float,
    tolerance: float = 1.0
) -> bool:
    """
    Returns True if difference is within tolerance.
    """

    if calculated_opm is None or source_opm is None:
        return True

    return abs(calculated_opm - source_opm) <= tolerance

def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Return on Equity (%)

    ROE = Net Profit / (Equity + Reserves) × 100
    """

    capital = equity_capital + reserves

    if capital <= 0:
        return None

    return round((net_profit / capital) * 100, 2)

def return_on_capital_employed(
    operating_profit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    """
    Return on Capital Employed (%)
    """

    employed = equity_capital + reserves + borrowings

    if employed <= 0:
        return None

    return round((operating_profit / employed) * 100, 2)

def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:
    """
    Return on Assets (%)
    """

    if total_assets is None or total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

# =====================================================
# Debt to Equity Ratio
# =====================================================

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float,
):
    """
    Debt to Equity Ratio

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Rules:
        • If borrowings == 0 → return 0
        • If equity <= 0 → return None
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)

# =====================================================
# High Leverage Flag
# =====================================================

def high_leverage_flag(
    debt_equity,
    broad_sector,
):
    """
    High leverage warning.

    Ignore Financial companies.
    """

    if debt_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_equity > 5

# =====================================================
# Interest Coverage Ratio
# =====================================================

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    """
    Interest Coverage Ratio

    Formula:
        (Operating Profit + Other Income) / Interest
    """

    if interest == 0:
        return None

    ebit = operating_profit + other_income

    return round(ebit / interest, 2)

# =====================================================
# ICR Label
# =====================================================

def icr_label(
    interest,
):
    """
    Label companies having no interest expense.
    """

    if interest == 0:
        return "Debt Free"

    return ""

# =====================================================
# ICR Warning
# =====================================================

def icr_warning(
    icr,
):
    """
    Company cannot comfortably pay interest.
    """

    if icr is None:
        return False

    return icr < 1.5

# =====================================================
# Net Debt
# =====================================================

def net_debt(
    borrowings,
    investments,
):
    """
    Net Debt

    Formula:
        Borrowings - Investments
    """

    return round(borrowings - investments, 2)

# =====================================================
# Asset Turnover
# =====================================================

def asset_turnover(
    sales,
    total_assets,
):
    """
    Asset Turnover

    Formula:
        Sales / Total Assets
    """

    if total_assets <= 0:
        return None

    return round(sales / total_assets, 2)

