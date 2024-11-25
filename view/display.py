from typing import List

from model.cell import Cell
from model.grid import Grid
from view.textures import live_texture, texture_parameter_from_cell, block_texture

EMPTY = " "
LINE_COUNT_PER_CELL = 2


def optional_chr(value: bool, character: chr) -> chr:
    return character if value else EMPTY


class Graphics:
    def __init__(self, texture: dict = block_texture):
        self.texture = texture

    def cloud_or_rain(self, cell: Cell):
        if cell.cloud.rain.value:
            return self.texture["RAIN"]
        if cell.cloud.cloud.value:
            return self.texture["CLOUD"]
        return EMPTY

    def cell_representation(self, cell: Cell) -> List[str]:
        cell_texture = self.texture[texture_parameter_from_cell(cell)]
        return [
            cell_texture + self.cloud_or_rain(cell) + str(cell.air_pollution.value),
            str(cell.cell_type.height) + EMPTY * 2 + str(cell.heat.value),
        ]
        """return [
            cell_texture + self.cloud_or_rain(cell) + EMPTY + self.texture["AIR_POLLUTION"] +
            str(cell.air_pollution.value),
            str(cell.cell_type.height) + EMPTY * 3 + self.texture["HEAT"] + str(cell.heat.value),
        ]"""

    def show_grid(self, grid: Grid):
        for line in grid.grid:
            representations = [self.cell_representation(cell) for cell in line]
            for i in range(LINE_COUNT_PER_CELL):
                for rep in representations:
                    print(rep[i], end=EMPTY*2)
                print()
            print()
        print()
