from model.cell import Cell
from model.characteristics import AirPollution, Cloud, Heat, Position, Wind
from model.consts import (
    CELL_TYPE_MAX_HEIGHTS,
    CELL_TYPE_MIN_HEIGHTS,
    DEFAULT_HEAT,
    GRID_SIZE,
)
from model.generate_terrain import generate_terrain
from model.position import Coordinate


class Grid:
    def __init__(self):
        terrain = generate_terrain()
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = Position(Coordinate(row), Coordinate(col))
                height_random_factor, cell_type = terrain[row][col]
                min_height, max_height = (
                    CELL_TYPE_MIN_HEIGHTS[cell_type],
                    CELL_TYPE_MAX_HEIGHTS[cell_type],
                )
                cell_height = min_height + int(
                    height_random_factor * (max_height - min_height)
                )
                self.grid[row][col] = Cell(
                    position=position,
                    neighbors=[],
                    heat=Heat(DEFAULT_HEAT),
                    cloud=Cloud(),
                    wind=Wind(),
                    air_pollution=AirPollution(),
                    cell_type=cell_type(cell_height),
                )
        self._amend_neighbors()

    def _amend_neighbors(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                positions = cell.position.neighbors()
                cell.neighbors = [
                    self.grid[position.x.value][position.y.value]
                    for position in positions
                ]

    def step(self):
        new_grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                new_grid[row][col] = self.grid[row][col].next_state()
        self.grid = new_grid
        self._amend_neighbors()
