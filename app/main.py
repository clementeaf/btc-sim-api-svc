from fastapi import FastAPI, Query
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel
import requests
import uvicorn
from app.models.spread_entry import SpreadEntry

from app.utils.utils import fetch_market_data

app = FastAPI(
    title="Markets Spread API v1",
    description="Api to get Markets Spreads.",
    version="0.1.0",)

# CORS Configueration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3600"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Modelo Pydantic para la respuesta de /markets
class MarketSpreadResponse(BaseModel):
    history: List[SpreadEntry]  # Ajusta SpreadEntry según tu modelo real

# Modelo Pydantic para la respuesta de /get_price
class PriceResponse(BaseModel):
    timestamp: int
    price: Optional[float]

# EndPoints 
@app.get(
        '/markets', 
        summary="markets recent spread and brief compare with last one", 
        description="Returns recent spread at the first call, then a compare between recent and last call without persist in database.", 
        response_model=MarketSpreadResponse,
        responses={
            200: {"description": "Successful response", "model": MarketSpreadResponse},
            404: {"description": "Not Found", "content": {"application/json": {"example": {"error": "Data not found"}}}},
            500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"error": "Internal Server Error"}}}},
        }
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
    
    
@app.get("/get_price", 
         response_model=PriceResponse,
         responses={
             200: {"description": "Successful response", "model": PriceResponse},
             404: {"description": "Not Found", "content": {"application/json": {"example": {"timestamp": 123456, "price": None}}}},
             500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"timestamp": 123456, "price": None}}}},
         })

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
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0, port=8000")