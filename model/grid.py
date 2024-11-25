from collections import Counter
from itertools import product
from typing import Callable

from model.cell import Cell
from model.characteristics import AirPollution, Cloud, Heat, Position
from model.consts import (CELL_TYPE_MAX_HEIGHTS, CELL_TYPE_MIN_HEIGHTS,
                          DEFAULT_HEAT, GRID_SIZE)
from model.generate_terrain import generate_terrain
from model.wind_grid import WindGrid


class Grid:
    def __init__(self):
        terrain = generate_terrain()
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = Position(row, col)
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
                    air_pollution=AirPollution(),
                    cell_type=cell_type(cell_height),
                )
        self._amend_neighbors()
        self.wind_grid = WindGrid()

    def _amend_neighbors(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                positions = cell.position.neighbors()
                cell.neighbors = [
                    self.grid[position.x.value][position.y.value]
                    for position in positions
                ]

    def cell_by_position(self, position: Position):
        return self.grid[position.x.value][position.y.value]

    def step(self):
        self.wind_grid.next_grid()
        new_grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = Position(row, col)
                new_grid[row][col] = self.grid[row][col].next_state(
                    [
                        self.cell_by_position(position)
                        for position in self.wind_grid.incoming_wind(position)
                    ],
                    [
                        self.cell_by_position(position)
                        for position in self.wind_grid.outgoing_wind(position)
                    ],
                )
        self.grid = new_grid
        self._amend_neighbors()

    @staticmethod
    def _percent(occurrences: int):
        return 100 * occurrences / (GRID_SIZE * GRID_SIZE)

    def _filter(self, condition: Callable, return_value: Callable = None):
        if return_value is None:
            return_value = lambda cell: cell
        return [return_value(self.grid[i][j]) for (i, j) in product(range(1, GRID_SIZE), repeat=2) if condition(self.grid[i][j])]

    def get_statistics(self) -> str:
        clouds = Grid._percent(len(self._filter(lambda cell: cell.cloud.cloud.value)))
        rain = Grid._percent(len(self._filter(lambda cell: cell.cloud.rain.value)))
        cell_types = Counter(self._filter(lambda _: True, lambda cell: type(cell.cell_type).__name__))
        pollution = Grid._percent(len(self._filter(lambda cell: cell.air_pollution.value > 0)))
        return f"""
Clouds: {clouds:.2f}%
Rain: {rain:.2f}%
Pollution: {pollution:.2f}%
Cell types: {dict(cell_types)}
"""
