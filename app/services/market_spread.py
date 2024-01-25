from typing import List
from app.models.spread_entry import SpreadEntry

def upsert_spread_entries(collection, spread_entries: List[SpreadEntry]):
    """
    Upsert spread entries into the specified collection.

    Parameters:
    - collection: MongoDB collection where spread entries will be upserted.
    - spread_entries (List[SpreadEntry]): List of SpreadEntry objects to upsert.

    Returns:
    - None
    """
    for spread_entry in spread_entries:
        spread_entry_dict = spread_entry.__dict__
        market_id = spread_entry_dict.pop('market_id')
        collection.update_one({'market_id': market_id}, {'$set': spread_entry_dict}, upsert=True)


def calculate_spread_direction(spread_diff):
    """
    Calculate the direction of spread change.

    Parameters:
    - spread_diff (float): The difference between previous and current spread.

    Returns:
    - str: Direction of spread change (Increased, Decreased, No change).
    """
    if spread_diff is None:
        return "No change"
    elif spread_diff > 0:
        return "Increased"
    elif spread_diff < 0:
        return "Decreased"
    else:
        return "No change"
