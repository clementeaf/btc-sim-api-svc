## Fetch Market Data
from fastapi import HTTPException
import requests

from app.database.mongodb import MongoDB

mongo = MongoDB(connection_string="mongodb+srv://clementefalcone58:C13m3nt3F41c0n3@clemente.ohoibgb.mongodb.net/?retryWrites=true&w=majority", database_name="clemente", 
collection_name="budaTest")

def determine_change_status(spread_difference):
    if spread_difference > 0:
        return "Aumento"
    elif spread_difference < 0:
        return "Disminución"
    else:
        return "Sin cambios"

def fetch_market_data_v2():
    """
    Fetch market spread data for all available markets.

    Returns:
    - list: List of dictionaries containing market_id and spread for each market.
    """
    try:
        response = requests.get('https://www.buda.com/api/v2/markets')
        response.raise_for_status()

        markets = response.json().get('markets', [])

        if not markets:
            return []

        market_spreads = []
        for market in markets:
            market_id = market['id']
            ticker_data = fetch_ticker_data_v2(market_id)
            recent_spread = ticker_data['spread']
            all_spreads = mongo.update_spreads(market_id, recent_spread)
            spread_difference = recent_spread - all_spreads[-2] if len(all_spreads) >= 2 else 0
            change_status = determine_change_status(spread_difference)
            
            market_spreads.append({
                'market_id': market_id,
                'recent_spread': recent_spread,
                'spreads_history': all_spreads,
                'spread_difference': spread_difference,
                'spread_change_status': change_status
            })

        return market_spreads

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f'Error en la llamada a la API de Buda.com: {str(e)}')
    

def fetch_ticker_data_v2(market_id):
    """
    Fetch ticker data for a specific market and return spread details.

    Parameters:
    - market_id (str): Unique identifier for the market.

    Returns:
    - dict: Dictionary containing market_id and spread for the market. 
    """
    ticker_url = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'

    try:
        ticker_response = requests.get(ticker_url)
        ticker_response.raise_for_status()

        ticker_data = ticker_response.json()['ticker']
        min_ask = float(ticker_data['min_ask'][0])
        max_bid = float(ticker_data['max_bid'][0])
        spread = min_ask - max_bid

        return {
            'market_id': market_id,
            'spread': spread,
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f'Error en la solicitud ticker para el mercado {market_id}: {str(e)}')
    
def update_spreads_in_mongodb(self, market_id, new_spread):
        """
        Actualiza la colección de MongoDB con el nuevo spread para un market_id dado.
        Devuelve la lista actualizada de spreads.

        Parameters:
        - market_id (str): Identificador único del mercado.
        - new_spread (float): Nuevo spread a agregar al historial.

        Returns:
        - list: Lista actualizada de spreads para el market_id.
        """
        spread_document = self.collection.find_one({'market_id': market_id})

        if spread_document:
            spreads = spread_document['spreads']
            spreads.append(new_spread)
            self.collection.update_one({'market_id': market_id}, {'$set': {'spreads': spreads}})
        else:
            self.collection.insert_one({'market_id': market_id, 'spreads': [new_spread]})

        return spreads
