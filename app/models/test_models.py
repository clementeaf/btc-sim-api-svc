from pydantic import ValidationError
import pytest

from app.models.spread_entry import SpreadEntry

def test_create_spread_entry():
    data = {
        "market_id": "BTC-USD",
        "spread": 123.45,
        "spreads_difference": 10.0,
        "spread_direction": "Increased"
    }

    entry = SpreadEntry(**data)
    
    assert entry.market_id == "BTC-USD"
    assert entry.spread == 123.45
    assert entry.spreads_difference == 10.0
    assert entry.spread_direction == "Increased"
    assert entry.previous_spread is None

def test_create_spread_entry_with_previous_spread():
    data = {
        "market_id": "BTC-USD",
        "spread": 123.45,
        "previous_spread": 120.0,
        "spreads_difference": 3.45,
        "spread_direction": "Increased"
    }

    entry = SpreadEntry(**data)

    assert entry.previous_spread == 120.0

def test_invalid_spread_entry():
    data = {
        "market_id": "BTC-USD",
        "spread": 123.45,
        "spreads_difference": 3.45
    }

    with pytest.raises(ValidationError):
        entry = SpreadEntry(**data)