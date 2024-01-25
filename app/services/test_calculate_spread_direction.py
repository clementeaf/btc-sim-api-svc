from app.services.market_spread import calculate_spread_direction

def test_calculate_spread_direction():
    assert calculate_spread_direction(None) == "No change"
    assert calculate_spread_direction(5.0) == "Increased"
    assert calculate_spread_direction(-3.0) == "Decreased"
    assert calculate_spread_direction(0.0) == "No change"