from itertools import product

from model.cell_types import City, Forest, Glacier, Ground, Sea

DAY_COUNT = 365
GRID_SIZE = 15

# Diagonal & Horizontal neighbors
NEIGHBOR_DIRECTIONS = list(set(product([-1, 0, 1], repeat=2)) - {(0, 0)})

CELL_TYPES = Ground, Sea, Forest, City, Glacier
CELL_TYPE_WEIGHTS = 2, 2, 1, 3, 2
CELL_TYPE_MIN_HEIGHTS = {Ground: 0, Sea: 0, Forest: 0, City: 0, Glacier: 0}
CELL_TYPE_MAX_HEIGHTS = {Ground: 7, Sea: 4, Forest: 5, City: 4, Glacier: 4}
MIN_HEIGHT = min(CELL_TYPE_MIN_HEIGHTS.values())
MAX_HEIGHT = max(CELL_TYPE_MAX_HEIGHTS.values())

DEFAULT_HEAT = 1
HEAT_MIN = 0
HEAT_MAX = 6
WIND_STRENGTH_MIN = 0
WIND_STRENGTH_MAX = 3
AIR_POLLUTION_MIN = 0
AIR_POLLUTION_MAX = 5

CLOUD_GENERATION_PROBABILITY = 0.2
RAIN_GENERATION_PROBABILITY = 0.8
POLLUTION_GENERATION_PROBABILITY = 0.02

GLACIER_MELTING_THRESHOLD = 5

EPSILON = 1e-6
