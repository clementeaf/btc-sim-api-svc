import pytest
from unittest import mock

import requests
from app.utils.spreads_persistence import fetch_ticker_data_v2, HTTPException

def test_fetch_ticker_data_v2():
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        'ticker': {
            'market_id': 'btc_usd',
            'min_ask': [105.0],
            'max_bid': [95.0],
        }
    }
    mock_response.raise_for_status.return_value = None
    with mock.patch('app.utils.spreads_persistence.requests.get', return_value=mock_response):
        result = fetch_ticker_data_v2('btc_usd')

    assert result == {'market_id': 'btc_usd', 'spread': 10.0}

def test_fetch_ticker_data_v2_api_failure():
    mock_response = mock.Mock()
    mock_response.raise_for_status.side_effect = requests.RequestException("API Error")
    mock_response.json.side_effect = Exception("Invalid JSON") 

    with mock.patch('app.utils.spreads_persistence.requests.get', return_value=mock_response):
        with pytest.raises(HTTPException, match=r'Error en la solicitud ticker para el mercado btc_usd: API Error'):
            fetch_ticker_data_v2('btc_usd')
