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