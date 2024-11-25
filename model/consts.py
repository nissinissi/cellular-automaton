from itertools import product

from model.cell_types import City, Forest, Glacier, Ground, Sea

DAY_COUNT = 365
GRID_SIZE = 20

# Diagonal & Horizontal neighbors
NEIGHBOR_DIRECTIONS = list(set(product([-1, 0, 1], repeat=2)) - {(0, 0)})

CELL_TYPES = Ground, Sea, Forest, City, Glacier
CELL_TYPE_WEIGHTS = 2, 2, 1, 1, 2
CELL_TYPE_MIN_HEIGHTS = {Ground: 1, Sea: 1, Forest: 1, City: 1, Glacier: 1}
CELL_TYPE_MAX_HEIGHTS = {Ground: 6, Sea: 1, Forest: 6, City: 3, Glacier: 2}

DEFAULT_HEAT = 1
HEAT_MIN = 0
HEAT_MAX = 6
WIND_STRENGTH_MIN = 0
WIND_STRENGTH_MAX = 3
AIR_POLLUTION_MIN = 0
AIR_POLLUTION_MAX = 5

CLOUD_GENERATION_PROBABILITY = 0.2
RAIN_GENERATION_PROBABILITY = 0.3

WIND_RANDOM_FACTOR = 0.9

GLACIER_MELTING_THRESHOLD = 5
