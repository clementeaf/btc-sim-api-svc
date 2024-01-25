from app.database.mongodb import MongoDB
from app.models.spread_entry import SpreadEntry
from app.services.market_spread import upsert_spread_entries

mongo_test = MongoDB("mongodb+srv://clementefalcone58:C13m3nt3F41c0n3@clemente.ohoibgb.mongodb.net/?retryWrites=true&w=majority", "clemente", "test_collection")

def test_upsert_spread_entries():
    spread_entries = [
        SpreadEntry(market_id="BTC-USD", spread=100.0, previous_spread=90.0, spreads_difference=10.0, spread_direction="Increased"),
        SpreadEntry(market_id="ETH-USD", spread=50.0, previous_spread=60.0, spreads_difference=-10.0, spread_direction="Decreased"),
        SpreadEntry(market_id="LTC-USD", spread=70.0, previous_spread=70.0, spreads_difference=0.0, spread_direction="No change"),
    ]

    upsert_spread_entries(mongo_test.collection, spread_entries)

    result = mongo_test.collection.find_one({"market_id": "BTC-USD"})
    assert result["spread"] == 100.0
    assert result["previous_spread"] == 90.0
    assert result["spreads_difference"] == 10.0
    assert result["spread_direction"] == "Increased"
    
    result = mongo_test.collection.find_one({"market_id": "ETH-USD"})
    assert result["spread"] == 50.0
    assert result["previous_spread"] == 60.0
    assert result["spreads_difference"] == -10.0
    assert result["spread_direction"] == "Decreased"

    result = mongo_test.collection.find_one({"market_id": "LTC-USD"})
    assert result["spread"] == 70.0
    assert result["previous_spread"] == 70.0
    assert result["spreads_difference"] == 0.0
    assert result["spread_direction"] == "No change"
