from pymongo import MongoClient
import pytest

from app.database.mongodb import MongoDB

TEST_CONNECTION_STRING = "mongodb+srv://clementefalcone58:C13m3nt3F41c0n3@clemente.ohoibgb.mongodb.net/?retryWrites=true&w=majority"
TEST_DATABASE_NAME = "clemente"
TEST_COLLECTION_NAME = "budaTest"

@pytest.fixture
def mongodb_fixture():
    client = MongoClient(TEST_CONNECTION_STRING)
    db = client[TEST_DATABASE_NAME]
    collection = db[TEST_COLLECTION_NAME]

    yield MongoDB(TEST_CONNECTION_STRING, TEST_DATABASE_NAME, TEST_COLLECTION_NAME)

    collection.drop()
    client.close()

def test_update_spreads(mongodb_fixture):
    market_id = "BTC-USD"
    new_spread = 123.45

    spreads = mongodb_fixture.update_spreads(market_id, new_spread)

    assert len(spreads) == 1
    assert spreads[0] == new_spread

    document = mongodb_fixture.collection.find_one({'market_id': market_id})
    assert document is not None
    assert document['spreads'] == [new_spread]
