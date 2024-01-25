from app.utils.math_utils import calculate_spread_direction

def test_calculate_spread_direction_no_change():
    result = calculate_spread_direction(None)
    assert result == "No change"

def test_calculate_spread_direction_increased():
    result = calculate_spread_direction(5.0)
    assert result == "Increased"

def test_calculate_spread_direction_decreased():
    result = calculate_spread_direction(-3.0)
    assert result == "Decreased"

def test_calculate_spread_direction_no_change_positive():
    result = calculate_spread_direction(0.0)
    assert result == "No change"

def test_calculate_spread_direction_no_change_negative():
    result = calculate_spread_direction(-0.0)
    assert result == "No change"
