from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from typing_extensions import Self

from model.consts import GRID_SIZE, NEIGHBOR_DIRECTIONS
from model.fields import RangeField


@dataclass
class Coordinate(RangeField):
    def __init__(self, value: Optional[int] = None):
        super().__init__(value)

    def __hash__(self):
        return super().__hash__()

    @property
    def min(self):
        return 0

    @property
    def max(self):
        return GRID_SIZE


@dataclass
class Position:
    """Indicates a position on the grid OR the delta between two positions."""

    x: Coordinate
    y: Coordinate

    def __init__(self, x: int, y: int):
        self.x = x if type(x) is Coordinate else Coordinate(x)
        self.y = y if type(y) is Coordinate else Coordinate(y)

    def __add__(self, other):
        x = (other.x.value + self.x.value + GRID_SIZE) % GRID_SIZE
        y = (other.y.value + self.y.value + GRID_SIZE) % GRID_SIZE
        return Position(x, y)

    def __hash__(self):
        return hash((self.x, self.y))

    def multiply(self, factor: float) -> Self:
        return Position(int(self.x.value * factor), int(self.y.value * factor))

    def neighbors(self) -> Iterable[Self]:
        return [self + Position(*direction) for direction in NEIGHBOR_DIRECTIONS]
