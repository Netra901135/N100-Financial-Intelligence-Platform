import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)


# -----------------------------------------
# Net Profit Margin
# -----------------------------------------

def test_net_profit_margin_normal():

    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():

    assert net_profit_margin(100, 0) is None


# -----------------------------------------
# Operating Profit Margin
# -----------------------------------------

def test_operating_profit_margin_normal():

    assert operating_profit_margin(200, 1000) == 20.0


def test_opm_cross_check_pass():

    assert opm_cross_check(20.0, 20.5)


def test_opm_cross_check_fail():

    assert not opm_cross_check(20.0, 22.5)


# -----------------------------------------
# ROE
# -----------------------------------------

def test_roe_normal():

    assert return_on_equity(100, 200, 300) == 20.0


def test_roe_negative_equity():

    assert return_on_equity(100, -200, 100) is None


# -----------------------------------------
# ROCE
# -----------------------------------------

def test_roce_normal():

    assert return_on_capital_employed(
        200,
        200,
        300,
        100,
    ) == 33.33


# -----------------------------------------
# ROA
# -----------------------------------------

def test_roa_normal():

    assert return_on_assets(100, 1000) == 10.0


def test_roa_zero_assets():

    assert return_on_assets(100, 0) is None

# =====================================================
# DAY 09
# =====================================================

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover,
)


def test_debt_to_equity_normal():

    assert debt_to_equity(200, 100, 300) == 0.5


def test_debt_to_equity_debt_free():

    assert debt_to_equity(0, 100, 300) == 0


def test_debt_to_equity_negative_equity():

    assert debt_to_equity(200, -100, 50) is None


def test_high_leverage():

    assert high_leverage_flag(6, "Industrials") is True


def test_financial_not_flagged():

    assert high_leverage_flag(8, "Financials") is False


def test_interest_coverage():

    assert interest_coverage_ratio(500, 50, 100) == 5.5


def test_interest_zero():

    assert interest_coverage_ratio(500, 50, 0) is None


def test_icr_label():

    assert icr_label(0) == "Debt Free"


def test_icr_warning():

    assert icr_warning(1.2) is True


def test_net_debt():

    assert net_debt(1000, 200) == 800


def test_asset_turnover():

    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero():

    assert asset_turnover(1000, 0) is None