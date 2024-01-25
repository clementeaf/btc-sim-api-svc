from typing import List
from pydantic import BaseModel

class SpreadHistory(BaseModel):
    market_id: str
    spreads_history: List[float] = []

    class Config:
        schema_extra = {
            "example": {
                "market_id": "BTC-CLP",
                "spreads_history": [228767.0, 228960.0, ...]
            }
        }
