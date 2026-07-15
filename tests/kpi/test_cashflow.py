from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


# ----------------------------------------------------
# Free Cash Flow
# ----------------------------------------------------

def test_free_cash_flow():

    assert free_cash_flow(500, -200) == 300


# ----------------------------------------------------
# CFO Quality
# ----------------------------------------------------

def test_cfo_quality_high():

    score, label = cfo_quality_score(500, 400)

    assert score == 1.25
    assert label == "High Quality"


def test_cfo_quality_moderate():

    score, label = cfo_quality_score(300, 400)

    assert score == 0.75
    assert label == "Moderate"


def test_cfo_quality_accrual():

    score, label = cfo_quality_score(100, 400)

    assert score == 0.25
    assert label == "Accrual Risk"


def test_cfo_quality_zero_pat():

    score, label = cfo_quality_score(500, 0)

    assert score is None
    assert label is None


# ----------------------------------------------------
# CapEx Intensity
# ----------------------------------------------------

def test_capex_light():

    value, label = capex_intensity(-50, 5000)

    assert value == 1.0
    assert label == "Asset Light"


def test_capex_moderate():

    value, label = capex_intensity(-200, 5000)

    assert value == 4.0
    assert label == "Moderate"


def test_capex_heavy():

    value, label = capex_intensity(-600, 5000)

    assert value == 12.0
    assert label == "Capital Intensive"


# ----------------------------------------------------
# FCF Conversion
# ----------------------------------------------------

def test_fcf_conversion():

    assert fcf_conversion_rate(300, 600) == 50.0


def test_fcf_conversion_zero():

    assert fcf_conversion_rate(300, 0) is None


# ----------------------------------------------------
# Capital Allocation Pattern
# ----------------------------------------------------

def test_pattern_reinvestor():

    assert capital_allocation_pattern(
        500,
        -300,
        -100,
    ) == "Reinvestor"


def test_pattern_distress():

    assert capital_allocation_pattern(
        -500,
        300,
        100,
    ) == "Distress Signal"


def test_pattern_growth():

    assert capital_allocation_pattern(
        -500,
        -300,
        100,
    ) == "Growth Funded by Debt"


def test_pattern_accumulator():

    assert capital_allocation_pattern(
        500,
        300,
        100,
    ) == "Cash Accumulator"