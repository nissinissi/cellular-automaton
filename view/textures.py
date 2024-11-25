from model.cell import Cell


live_texture = {
    "GROUND": "🪨",
    "SEA": "🌊",  # "💧",
    "FOREST": "🌲",
    "CITY": "🏭",
    "GLACIER": "⛄️",  # "❄️",  # "🧊",
    "RAIN": "💧",
    "CLOUD": "💨",
    "SUN": "🌞️",
    "AIR_POLLUTION": "💨",  # "🌫️",
    "HEAT": "🌡️",  # "🔥"
}


block_texture = {
    "GROUND": "🟫",
    "SEA": "🟦",
    "FOREST": "🟩",
    "CITY": "🟨",
    "GLACIER": "⬜️️",
    "RAIN": "🔵",
    "CLOUD": "⚪️️",
    "SUN": "⚫️️",
    "AIR_POLLUTION": "💨",
    "HEAT": "🌡️",  # "🔥"
}


def texture_parameter_from_cell(cell: Cell) -> str:
    return str(type(cell.cell_type).__name__).upper()
