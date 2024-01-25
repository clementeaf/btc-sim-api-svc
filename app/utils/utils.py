#buda-api/app/utils/utils.py
from fastapi import HTTPException
import requests
from app.models.spread_entry import SpreadEntry
from app.utils.math_utils import calculate_spread_direction

previous_spread_data = []
    
def fetch_ticker_data(market_id, previous_spread_data):
    """
    Fetch ticker data for a specific market and calculate spread details.

    Parameters:
    - market_id (str): Unique identifier for the market.
    - previous_spread_data (list): List of dictionaries containing previous spread data.

    Returns:
    - SpreadEntry: Object representing the spread details for the market.
    """
    ticker_url = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'

    try:
        ticker_response = requests.get(ticker_url)
        ticker_response.raise_for_status()

        ticker_data = ticker_response.json()['ticker']
        min_ask = float(ticker_data['min_ask'][0])
        max_bid = float(ticker_data['max_bid'][0])
        spread = min_ask - max_bid
        spreads_difference = 0.0
        previous_spread = None

        if previous_spread_data:
            for entry in previous_spread_data:
                if entry['market_id'] == market_id and 'spread' in entry:
                    previous_spread = entry['spread']
                    spreads_difference = previous_spread - spread
                    break

        spread_direction = calculate_spread_direction(spreads_difference)

        return SpreadEntry(
            market_id=market_id,
            spread=spread,
            previous_spread=previous_spread,
            spreads_difference=spreads_difference,
            spread_direction=spread_direction
        )

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f'Error en la solicitud ticker para el mercado {market_id}: {str(e)}')
    
    
def fetch_market_entries(markets, previous_spread_data):
    """
    Fetch spread entries for multiple markets.

    Parameters:
    - markets (list): List of market dictionaries.
    - previous_spread_data (list): List of dictionaries containing previous spread data.

    Returns:
    - list: List of SpreadEntry objects for each market.
    """

    spread_entries = []
    for market in markets:
        market_id = market['id']
        spread_entry = fetch_ticker_data(market_id, previous_spread_data)
        spread_entries.append(spread_entry)
    return spread_entries


def fetch_market_data():
    """
    Fetch market spread data for all available markets.

    Returns:
    - list: List of SpreadEntry objects representing spread data for each market.
    """
    global previous_spread_data

    try:
        response = requests.get('https://www.buda.com/api/v2/markets')
        response.raise_for_status()

        markets = response.json().get('markets', [])

        if not markets:
            return []

        spread_entries = fetch_market_entries(markets, previous_spread_data)

        previous_spread_data = [{'market_id': entry.market_id, 'spread': entry.spread} for entry in spread_entries]

        return spread_entries

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f'Error en la llamada a la API de Buda.com: {str(e)}')
