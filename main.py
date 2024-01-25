from fastapi import FastAPI, Query
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from app.utils.utils import fetch_market_data

app = FastAPI(
    title="Markets Spread API v1",
    description="Api to get Markets Spreads.",
    version="0.1.0",)

# CORS Configueration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# EndPoints 
@app.get(
        '/markets', 
        summary="markets recent spread and brief compare with last one", 
        description="Returns recent spread at the first call, then a compare between recent and last call without persist in database.", 
)
async def get_market_spread():
    """
    Fetch market spread data and return as a JSON response.

    Returns:
    - dict: JSON response containing the history of spread entries.
    """
    try:
        return fetch_market_data()
    except HTTPException as e:
        return {"error": str(e)}
    
    
@app.get("/get_price")
async def get_price(timestamp: int = Query(..., description="Timestamp")):
    market_id = 'btc-clp'

    url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
    response = requests.get(url, params={
        'timestamp': timestamp,
        'limit': 1, 
    })

    if response.status_code == 200:
        data = response.json()
        last_trade = data["trades"]["entries"][0]
        price = float(last_trade[2]) 
        return {"timestamp": timestamp, "price": price}
    else:
        return {"timestamp": timestamp, "price": None}
    