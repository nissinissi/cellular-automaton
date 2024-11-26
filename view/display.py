from typing import List, Optional

from model.cell import Cell
from model.grid import Grid
from view.textures import live_texture, texture_parameter_from_cell, block_texture

EMPTY = " "
LINE_COUNT_PER_CELL = 2


def optional_chr(value: bool, character: chr) -> chr:
    return character if value else EMPTY


class Graphics:
    def __init__(self, texture: Optional[dict] = None):
        self.texture = live_texture if texture is None else texture

    def cloud_or_rain(self, cell: Cell):
        if cell.cloud.rain.value:
            return self.texture["RAIN"]
        if cell.cloud.cloud.value:
            return self.texture["CLOUD"]
        return self.texture["SUN"]

    def cell_representation(self, cell: Cell) -> List[str]:
        cell_texture = self.texture[texture_parameter_from_cell(cell)]
        return [
            cell_texture + EMPTY + str(cell.cell_type.height) + EMPTY,
            self.cloud_or_rain(cell) + str(cell.heat.value) + EMPTY + str(cell.air_pollution.value),
        ]

    def get_grid_str(self, grid: Grid) -> str:
        grid_str = ""
        for line in grid.grid:
            representations = [self.cell_representation(cell) for cell in line]
            for i in range(LINE_COUNT_PER_CELL):
                for rep in representations:
                    grid_str += rep[i] + EMPTY*2
                grid_str += "\n"
            grid_str += "\n"
        return grid_str + "\n"
