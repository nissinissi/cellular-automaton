from dataclasses import dataclass
from random import randint, random
from typing import Dict, Iterable, Optional, Sequence

from typing_extensions import Self

from model.cell_types import CellType, City, Glacier, Sea
from model.characteristics import (AirPollution, Cloud, Heat, IsCloudPresent,
                                   Position, Rain, Wind, WindDirection,
                                   WindStrength)
from model.consts import (AIR_POLLUTION_MAX, CLOUD_GENERATION_PROBABILITY,
                          GLACIER_MELTING_THRESHOLD, HEAT_MAX,
                          WIND_RANDOM_FACTOR, CELL_TYPE_MAX_HEIGHTS, RAIN_GENERATION_PROBABILITY,
                          POLLUTION_GENERATION_PROBABILITY, HEAT_MIN)
from model.wind_grid import WindGrid


@dataclass
class Cell:
    position: Position
    neighbors: Sequence[Self]
    heat: Heat
    cloud: Cloud
    air_pollution: AirPollution
    cell_type: CellType

    def __hash__(self):
        return hash(self.position)

    def next_heat(self) -> Heat:
        heat_value = self.heat.value
        if self.cloud.rain.value:
            heat_value -= 1
        heat_value += self.air_pollution.value
        return Heat(max(min(heat_value, HEAT_MAX), HEAT_MIN))

    @staticmethod
    def _may_create_cloud() -> bool:
        return random() > (1 - CLOUD_GENERATION_PROBABILITY)

    @staticmethod
    def _may_create_rain() -> bool:
        return random() > (1 - RAIN_GENERATION_PROBABILITY)

    @staticmethod
    def _may_create_pollution() -> bool:
        return random() > (1 - POLLUTION_GENERATION_PROBABILITY)

    def is_melting_glacier(self) -> bool:
        return (
            type(self.cell_type) is Glacier
            and self.heat.value > GLACIER_MELTING_THRESHOLD
        )

    def next_cloud(self, upwind_cells) -> Cloud:
        # remaining_cloud = (
        #     any(self.position == upwind_cell.position for upwind_cell in upwind_cells)
        #     and self.cloud.cloud.value
        # )
        # incoming_cloud = any([neighbor.cloud.cloud.value for neighbor in upwind_cells])
        new_cloud = Cell._may_create_cloud()
        is_cloud_present = new_cloud  # or incoming_cloud or remaining_cloud
        is_rain_present = new_cloud and Cell._may_create_rain()
        return Cloud(IsCloudPresent(is_cloud_present), Rain(is_rain_present))

    @staticmethod
    def next_air_pollution(upwind_cells):
        upwind_city_sum = sum(
            type(neighbor.cell_type) is City for neighbor in upwind_cells
        )
        upwind_pollution_sum = sum(
            neighbor.air_pollution.value for neighbor in upwind_cells
        )
        if Cell._may_create_pollution():
            return AirPollution(
                min(upwind_city_sum + upwind_pollution_sum, AIR_POLLUTION_MAX)
            )
        else:
            return AirPollution(0)

    def next_cell_type(self, downwind_cells, upwind_cells):
        new_cell_type = self.cell_type
        # Glacier Melt
        if self.is_melting_glacier():
            new_cell_type = Glacier(max(0, self.cell_type.height - 1))
        # Incoming Water Flow
        upwind_water_sources = filter(
            lambda neighbor: type(neighbor) is Sea or neighbor.is_melting_glacier(),
            upwind_cells,
        )
        higher_upwind_water_sources = list(
            filter(
                lambda neighbor: neighbor.cell_type.height
                > self.cell_type.height,
                upwind_water_sources,
            )
        )
        if len(higher_upwind_water_sources) > 0:
            new_cell_type = Sea(min(len(higher_upwind_water_sources), CELL_TYPE_MAX_HEIGHTS[Sea]))
        # Outgoing Water Flow
        if type(self.cell_type) is Sea:
            lower_downwind_neighbors = list(
                filter(
                    lambda neighbor: neighbor.cell_type.height
                                     < self.cell_type.height,
                    upwind_water_sources,
                )
            )
            if lower_downwind_neighbors:
                new_cell_type = Sea(max(0, self.cell_type.height - len(lower_downwind_neighbors)))
        return new_cell_type

    def next_state(
        self, upwind_cells: Iterable[Self], downwind_cells: Iterable[Self]
    ) -> Self:
        new_heat = self.next_heat()
        new_cloud = self.next_cloud(upwind_cells)
        new_air_pollution = self.next_air_pollution(upwind_cells)
        new_cell_type = self.next_cell_type(downwind_cells, upwind_cells)
        return Cell(
            position=self.position,
            neighbors=[],
            heat=new_heat,
            cloud=new_cloud,
            air_pollution=new_air_pollution,
            cell_type=new_cell_type,
        )
