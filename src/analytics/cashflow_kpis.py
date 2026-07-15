"""
cashflow_kpis.py

Sprint 2 - Day 11
Cash Flow KPI Engine
"""

from typing import Optional

# =====================================================
# Free Cash Flow
# =====================================================

def free_cash_flow(
    operating_activity,
    investing_activity,
):
    """
    FCF = Operating Activity + Investing Activity

    Investing activity is normally negative.
    """

    return round(
        operating_activity + investing_activity,
        2,
    )

# =====================================================
# CFO Quality
# =====================================================

def cfo_quality_score(
    operating_activity,
    net_profit,
):
    """
    CFO / PAT

    Returns

    score,
    label
    """

    if net_profit == 0:

        return None, None

    score = operating_activity / net_profit

    if score > 1:

        label = "High Quality"

    elif score >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    return round(score, 2), label

# =====================================================
# CapEx Intensity
# =====================================================

def capex_intensity(
    investing_activity,
    sales,
):
    """
    abs(CapEx) / Sales ×100
    """

    if sales <= 0:

        return None, None

    value = (
        abs(investing_activity)
        / sales
    ) * 100

    if value < 3:

        label = "Asset Light"

    elif value <= 8:

        label = "Moderate"

    else:

        label = "Capital Intensive"

    return round(value, 2), label

# =====================================================
# FCF Conversion
# =====================================================

def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit,
):
    """
    FCF / Operating Profit
    """

    if operating_profit == 0:

        return None

    return round(
        (free_cash_flow_value / operating_profit)
        * 100,
        2,
    )

# =====================================================
# Capital Allocation
# =====================================================

def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
):

    cfo = "+" if operating_activity >= 0 else "-"

    cfi = "+" if investing_activity >= 0 else "-"

    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    mapping = {

        ("+", "-", "-"): "Reinvestor",

        ("+", "+", "-"): "Liquidating Assets",

        ("-", "+", "+"): "Distress Signal",

        ("-", "-", "+"): "Growth Funded by Debt",

        ("+", "+", "+"): "Cash Accumulator",

        ("-", "-", "-"): "Pre-Revenue",

        ("+", "-", "+"): "Mixed",

    }

    return mapping.get(

        pattern,

        "Unknown",

    )

