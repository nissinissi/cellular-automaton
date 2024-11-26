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


TEXTURE_BY_NAME = {'live': live_texture, 'block': block_texture}


def texture_by_name(texture_name: str):
    assert texture_name in TEXTURE_BY_NAME
    return TEXTURE_BY_NAME[texture_name]


def texture_parameter_from_cell(cell: Cell) -> str:
    return str(type(cell.cell_type).__name__).upper()
