from dataclasses import dataclass


@dataclass
class CellType:
    height: int


class Ground(CellType):
    pass


class Sea(CellType):
    pass


class Forest(CellType):
    pass


class City(CellType):
    pass


class Glacier(CellType):
    pass
