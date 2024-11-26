from typing import List, Optional

from model.characteristics import Wind, WindDirection
from model.configurable import GRID_SIZE
from model.position import Coordinate, Position


class WindGrid:
    def __init__(self, grid_size: Optional[int] = GRID_SIZE):
        self.grid_size = grid_size
        self.wind_grid = [
            [None for i in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.outgoing_cache = {}

    def next_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.wind_grid[i][j] = Wind()
        self.outgoing_cache = {}

    def outgoing_wind(self, position: Position) -> List[Position]:
        if position in self.outgoing_cache:
            return self.outgoing_cache[position]
        l = []
        wind = self.wind_grid[position.x.value][position.y.value]
        for i in range(wind.strength.value):
            destination = position + wind.direction.value.multiply(i)
            if destination not in l:
                l += [destination]
        self.outgoing_cache[position] = l
        return l

    def incoming_wind(self, position: Position) -> List[Position]:
        l = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                source = Position(i, j)
                if position in self.outgoing_wind(source):
                    l += [source]
        return l
