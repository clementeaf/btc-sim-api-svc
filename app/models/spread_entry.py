from typing import Optional
from pydantic import BaseModel

class SpreadEntry(BaseModel):
    """
    Represents a spread entry with relevant data.

    Parameters:
    - market_id (str): Unique identifier for the market.
    - spread (float): Current spread value.
    - previous_spread (float): Previous spread value.
    - spreads_difference (float): Difference between previous and current spread.
    - spread_direction (str): Direction of spread change (Increased, Decreased, No change).
    """
    market_id: str
    spread: float
    previous_spread: Optional[float] = None
    spreads_difference: float
    spread_direction: str