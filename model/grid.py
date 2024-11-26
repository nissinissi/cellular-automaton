from collections import Counter
from itertools import product
from random import random
from typing import Callable, Dict

from model.cell import Cell
from model.cell_types import Sea, Glacier
from model.characteristics import AirPollution, Cloud, Heat, Position
from model.configurable import (CELL_TYPE_MAX_HEIGHTS, CELL_TYPE_MIN_HEIGHTS,
                                DEFAULT_HEAT, GRID_SIZE, HEAT_MAX, HEAT_MIN, AIR_POLLUTION_MIN, AIR_POLLUTION_MAX, MIN_HEIGHT,
                                MAX_HEIGHT)
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
                    random() * (max_height - min_height)
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
    def _portion(occurrences: int):
        return occurrences / (GRID_SIZE * GRID_SIZE)

    @staticmethod
    def _percent(occurrences: int):
        return 100 * Grid._portion(occurrences)

    def _filter(self, condition: Callable, return_value: Callable = None):
        if return_value is None:
            return_value = lambda cell: cell
        return [return_value(self.grid[i][j]) for (i, j) in product(range(1, GRID_SIZE), repeat=2) if condition(self.grid[i][j])]

    def get_statistics(self, for_printing: bool=False) -> Dict:
        every = lambda cell: True

        clouds = Grid._percent(len(self._filter(lambda cell: cell.cloud.cloud.value))),
        rain = Grid._percent(len(self._filter(lambda cell: cell.cloud.rain.value))),

        avg_heat = Grid._portion(sum(self._filter(every, lambda cell: cell.heat.value)))
        avg_heat_percent = 100 * (avg_heat - HEAT_MIN) / (HEAT_MAX - HEAT_MIN)

        pollution_percent = Grid._percent(len(self._filter(lambda cell: cell.air_pollution.value > 0)))
        pollution_strength = Grid._portion(len(self._filter(every, lambda cell: cell.air_pollution.value)))
        pollution_strength_percent = 100 * (pollution_strength - AIR_POLLUTION_MIN) / (AIR_POLLUTION_MAX - AIR_POLLUTION_MIN)

        sea_heights = self._filter(lambda cell: type(cell.cell_type) is Sea, lambda cell: cell.cell_type.height)
        avg_sea_height = sum(sea_heights) / len(sea_heights)
        avg_sea_height_percent = 100 * (avg_sea_height - MIN_HEIGHT) / (MAX_HEIGHT - MIN_HEIGHT)
        glacier_heights = self._filter(lambda cell: type(cell.cell_type) is Glacier, lambda cell: cell.cell_type.height)
        avg_glacier_height = sum(glacier_heights) / len(glacier_heights)
        avg_glacier_height_percent = 100 * (avg_glacier_height - MIN_HEIGHT) / (MAX_HEIGHT - MIN_HEIGHT)

        cell_type_counts = dict(Counter(self._filter(every, lambda cell: type(cell.cell_type).__name__)))
        cell_type_percents = {f"{cell_type.lower()}_percent": self._percent(count) for cell_type, count in cell_type_counts.items()}
        cell_type_dict = {'cell_type_percents': cell_type_percents} if for_printing else cell_type_percents

        return {
            'cloud_percentage': clouds,
            'rain_percentage': rain,
            'avg_heat_percent': avg_heat_percent,
            'pollution_percent': pollution_percent,
            'pollution_strength_percent': pollution_strength_percent,
            'avg_sea_height_percent': avg_sea_height_percent,
            'avg_glacier_height_percent': avg_glacier_height_percent,
            **cell_type_dict,
        }

    @staticmethod
    def statistics_str(statistics):
        cell_types_percents = "Cell types:\n\t" + "\n\t".join(f"{cell_type}: {cell_percents:.2f}%" for cell_type, cell_percents in statistics['cell_type_percents'].items())
        return f"""
Cells with clouds: {statistics['cloud_percentage'][0]:.2f}%
Cells with rain: {statistics['rain_percentage'][0]:.2f}%
Avg. heat: {statistics['avg_heat_percent']:.2f}%
Cells with pollution: {statistics['pollution_percent']:.2f}%
Avg. pollution metric: {statistics['pollution_strength_percent']:.2f}%
Avg sea height: {statistics['avg_sea_height_percent']:.2f}%
Avg. glacier height: {statistics['avg_glacier_height_percent']:.2f}%
{cell_types_percents}
"""
