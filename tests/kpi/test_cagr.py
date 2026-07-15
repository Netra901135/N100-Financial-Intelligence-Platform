from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
    NORMAL,
    TURNAROUND,
    DECLINE_TO_LOSS,
    BOTH_NEGATIVE,
    ZERO_BASE,
    INSUFFICIENT,
)


# -------------------------------------------------
# Normal CAGR
# -------------------------------------------------

def test_normal_cagr():

    value, flag = calculate_cagr(100, 200, 5)

    assert value == 14.87
    assert flag == NORMAL


# -------------------------------------------------
# Revenue CAGR
# -------------------------------------------------

def test_revenue_cagr():

    value, flag = revenue_cagr(100, 200, 5)

    assert value == 14.87
    assert flag == NORMAL


# -------------------------------------------------
# PAT CAGR
# -------------------------------------------------

def test_pat_cagr():

    value, flag = pat_cagr(100, 200, 5)

    assert value == 14.87
    assert flag == NORMAL


# -------------------------------------------------
# EPS CAGR
# -------------------------------------------------

def test_eps_cagr():

    value, flag = eps_cagr(100, 200, 5)

    assert value == 14.87
    assert flag == NORMAL


# -------------------------------------------------
# Turnaround
# -------------------------------------------------

def test_turnaround():

    value, flag = calculate_cagr(-100, 50, 5)

    assert value is None
    assert flag == TURNAROUND


# -------------------------------------------------
# Decline to Loss
# -------------------------------------------------

def test_decline_to_loss():

    value, flag = calculate_cagr(100, -50, 5)

    assert value is None
    assert flag == DECLINE_TO_LOSS


# -------------------------------------------------
# Both Negative
# -------------------------------------------------

def test_both_negative():

    value, flag = calculate_cagr(-100, -50, 5)

    assert value is None
    assert flag == BOTH_NEGATIVE


# -------------------------------------------------
# Zero Base
# -------------------------------------------------

def test_zero_base():

    value, flag = calculate_cagr(0, 100, 5)

    assert value is None
    assert flag == ZERO_BASE


# -------------------------------------------------
# Insufficient Years
# -------------------------------------------------

def test_insufficient():

    value, flag = calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == INSUFFICIENT


# -------------------------------------------------
# Flat Growth
# -------------------------------------------------

def test_flat_growth():

    value, flag = calculate_cagr(100, 100, 5)

    assert value == 0.0
    assert flag == NORMAL