from dataclasses import dataclass
from random import randint, random
from typing import Dict, Optional, Sequence

from typing_extensions import Self

from model.cell_types import CellType, City, Glacier, Sea
from model.characteristics import (
    AirPollution,
    Cloud,
    Heat,
    IsCloudPresent,
    Position,
    Rain,
    Wind,
    WindDirection,
    WindStrength,
)
from model.consts import (
    AIR_POLLUTION_MAX,
    CLOUD_CREATION_PROBABILITY,
    GLACIER_MELTING_THRESHOLD,
    WIND_RANDOM_FACTOR, HEAT_MAX,
)


@dataclass
class Cell:
    position: Position
    neighbors: Sequence[Self]
    heat: Heat
    cloud: Cloud
    wind: Wind
    air_pollution: AirPollution
    cell_type: CellType
    _outgoing_wind_factor_cache: Optional[Dict[Position, WindStrength]] = None

    def __hash__(self):
        return hash(self.position)

    def _may_create_cloud(self) -> bool:
        if type(self.cell_type) is Sea or not any(
            neighbor.cell_type is Sea for neighbor in self.neighbors
        ):
            return False
        return random() > (1 - CLOUD_CREATION_PROBABILITY)

    def is_melting_glacier(self) -> bool:
        return (
            type(self.cell_type) is Glacier
            and self.heat.value > GLACIER_MELTING_THRESHOLD
        )

    def next_state(self) -> Self:
        incoming_wind_factor = self.compute_incoming_wind_factor()
        upwind_neighbors = list(incoming_wind_factor.keys())
        downwind_neighbors = list(self.outgoing_wind_factor.keys())

        heat_value = self.heat.value
        if self.cloud.rain.value:
            heat_value -= 1
        heat_value += self.air_pollution.value
        new_heat = Heat(min(heat_value, HEAT_MAX))

        remaining_cloud = self.wind.strength.value == 0 and self.cloud.cloud.value
        incoming_cloud = any(
            [neighbor.cloud.cloud.value for neighbor in upwind_neighbors]
        )
        new_cloud = self._may_create_cloud()
        is_cloud_present = incoming_cloud or remaining_cloud or new_cloud
        is_rain_present = (
            int(incoming_cloud) + int(remaining_cloud) + int(new_cloud) > 0
        )
        new_cloud = Cloud(IsCloudPresent(is_cloud_present), Rain(is_rain_present))

        incoming_wind_direction_sum = sum(
            (neighbor.wind.direction.value for neighbor in upwind_neighbors),
            start=Position(0, 0),
        )
        incoming_wind_direction = incoming_wind_direction_sum.multiply(
            1 / len(self.neighbors)
        )
        incoming_wind_component = incoming_wind_direction.multiply(
            1 - WIND_RANDOM_FACTOR
        )
        new_wind_component = WindDirection().value.multiply(WIND_RANDOM_FACTOR)
        new_wind_direction = WindDirection(incoming_wind_component + new_wind_component)
        new_wind_strength = WindStrength()
        new_wind = Wind(new_wind_strength, new_wind_direction)

        upwind_city_sum = sum(
            type(neighbor.cell_type) is City for neighbor in upwind_neighbors
        )
        upwind_pollution_sum = sum(
            neighbor.air_pollution.value for neighbor in upwind_neighbors
        )
        new_air_pollution = AirPollution(min(upwind_city_sum + upwind_pollution_sum, AIR_POLLUTION_MAX))

        new_cell_type = self.cell_type
        # Glacier Melt
        if self.is_melting_glacier():
            new_cell_type = Glacier(max(0, self.cell_type.height - 1))
        # Incoming Water Flow
        upwind_water_sources = filter(
            lambda neighbor: type(neighbor) is Sea or neighbor.is_melting_glacier(),
            upwind_neighbors,
        )
        higher_upwind_water_sources = list(
            filter(
                lambda neighbor: neighbor.cell_type.height.value
                > self.cell_type.height.value,
                upwind_water_sources,
            )
        )
        if len(higher_upwind_water_sources) > 0:
            new_cell_type = Sea(len(higher_upwind_water_sources))
        # Outgoing Water Flow
        if type(self.cell_type) is Sea:
            any_lower_downwind_neighbors = any(
                neighbor for neighbor in downwind_neighbors
            )
            if any_lower_downwind_neighbors:
                new_cell_type = Sea(max(0, self.cell_type.height - 1))

        return Cell(
            position=self.position,
            neighbors=[],
            heat=new_heat,
            cloud=new_cloud,
            wind=new_wind,
            air_pollution=new_air_pollution,
            cell_type=new_cell_type,
        )
