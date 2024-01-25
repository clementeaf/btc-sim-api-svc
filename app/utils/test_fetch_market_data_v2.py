from unittest import mock
from app.utils.spreads_persistence import fetch_market_data_v2

def test_fetch_market_data_v2():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
    'markets': [
        {'id': 'btc_usd', 'symbol': 'BTC/USD'},
        {'id': 'eth_usd', 'symbol': 'ETH/USD'},
    ],
    'ticker': {
        'market_id': 'btc_usd',
        'min_ask': [105.0], 
        'max_bid': [95.0],
    }
}

    mock_response.raise_for_status.return_value = None

    with mock.patch('app.utils.spreads_persistence.requests.get', return_value=mock_response):
        with mock.patch('app.utils.spreads_persistence.MongoDB.update_spreads', return_value=[90.0, 95.0, 100.0]):
            result = fetch_market_data_v2()

    assert len(result) == 2
    assert result[0]['market_id'] == 'btc_usd'
    assert result[0]['recent_spread'] == 10.0
    assert result[0]['spreads_history'] == [90.0, 95.0, 100.0]
    assert result[0]['spread_difference'] == -85.0
    print(f"change_status: {result[0]['spread_change_status']}")
    assert result[0]['spread_change_status'] == 'Disminución'

    assert result[1]['market_id'] == 'eth_usd'
