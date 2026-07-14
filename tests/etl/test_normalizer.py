"""
Unit Tests for normaliser.py

Run:
pytest tests/etl/test_normaliser.py -v
"""

import pytest

from src.etl.normaliser import DataNormaliser


# ==========================================================
# normalize_year() Tests (20)
# ==========================================================

def test_year_dec_2012():
    assert DataNormaliser.normalize_year("Dec 2012") == 2012


def test_year_mar_2014():
    assert DataNormaliser.normalize_year("Mar 2014") == 2014


def test_year_mar13():
    assert DataNormaliser.normalize_year("Mar-13") == 2013


def test_year_mar24():
    assert DataNormaliser.normalize_year("Mar-24") == 2024


def test_year_fy23():
    assert DataNormaliser.normalize_year("FY23") == 2023


def test_year_fy24():
    assert DataNormaliser.normalize_year("FY24") == 2024


def test_year_2020():
    assert DataNormaliser.normalize_year("2020") == 2020


def test_year_2024():
    assert DataNormaliser.normalize_year("2024") == 2024


def test_year_integer():
    assert DataNormaliser.normalize_year(2022) == 2022


def test_year_float():
    assert DataNormaliser.normalize_year(2023.0) == 2023


def test_year_two_digit():
    assert DataNormaliser.normalize_year("21") == 2021


def test_year_spaces():
    assert DataNormaliser.normalize_year(" 2022 ") == 2022


def test_year_none():
    assert DataNormaliser.normalize_year(None) is None


def test_year_empty():
    assert DataNormaliser.normalize_year("") is None


def test_year_invalid():
    assert DataNormaliser.normalize_year("abcd") is None


def test_year_invalid_text():
    assert DataNormaliser.normalize_year("Financial Year") is None


def test_year_nan():
    assert DataNormaliser.normalize_year(float("nan")) is None


def test_year_dec2024():
    assert DataNormaliser.normalize_year("Dec 2024") == 2024


def test_year_mar2018():
    assert DataNormaliser.normalize_year("Mar 2018") == 2018


def test_year_fy20():
    assert DataNormaliser.normalize_year("FY20") == 2020


# ==========================================================
# normalize_company_id() Tests (15)
# ==========================================================

def test_company_upper():
    assert DataNormaliser.normalize_company_id("ABB") == "ABB"


def test_company_lower():
    assert DataNormaliser.normalize_company_id("abb") == "ABB"


def test_company_spaces():
    assert DataNormaliser.normalize_company_id(" abb ") == "ABB"


def test_company_ns():
    assert DataNormaliser.normalize_company_id("ABB.NS") == "ABB"


def test_company_bo():
    assert DataNormaliser.normalize_company_id("ABB.BO") == "ABB"


def test_company_mixed():
    assert DataNormaliser.normalize_company_id("AbB") == "ABB"


def test_company_hdfc():
    assert DataNormaliser.normalize_company_id("hdfcbank") == "HDFCBANK"


def test_company_tcs():
    assert DataNormaliser.normalize_company_id("tcs") == "TCS"


def test_company_reliance():
    assert DataNormaliser.normalize_company_id("Reliance") == "RELIANCE"


def test_company_none():
    assert DataNormaliser.normalize_company_id(None) is None


def test_company_empty():
    assert DataNormaliser.normalize_company_id("") == ""


def test_company_infosys():
    assert DataNormaliser.normalize_company_id(" infosys ") == "INFOSYS"


def test_company_axis():
    assert DataNormaliser.normalize_company_id("axisbank.ns") == "AXISBANK"


def test_company_icici():
    assert DataNormaliser.normalize_company_id("ICICIBANK.BO") == "ICICIBANK"


def test_company_adani():
    assert DataNormaliser.normalize_company_id("adaniports") == "ADANIPORTS"