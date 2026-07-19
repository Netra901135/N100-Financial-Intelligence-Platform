from src.screener.engine import ScreenerEngine

def test_load_preset():

    engine = ScreenerEngine()

    preset = engine.load_preset(
        "quality_compounder"
    )

    assert preset["roe_min"] == 15

def test_load_preset():

    engine = ScreenerEngine()

    preset = engine.load_preset("quality_compounder")

    assert preset["roe_min"] == 15


def test_quality_compounder():

    engine = ScreenerEngine()

    result = engine.apply_filter("quality_compounder")

    assert result is not None
    assert len(result) > 0


def test_value_pick():

    engine = ScreenerEngine()

    result = engine.apply_filter("value_pick")

    assert result is not None