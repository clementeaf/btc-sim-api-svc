from app.utils.spreads_persistence import determine_change_status


def test_determine_change_status_increased():
    spread_difference = 5.0
    result = determine_change_status(spread_difference)
    assert result == "Aumento"

def test_determine_change_status_decreased():
    spread_difference = -3.0
    result = determine_change_status(spread_difference)
    assert result == "Disminución"

def test_determine_change_status_no_change():
    spread_difference = 0.0
    result = determine_change_status(spread_difference)
    assert result == "Sin cambios"