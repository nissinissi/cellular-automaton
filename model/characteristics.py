from dataclasses import dataclass
from random import choice
from typing import Optional

from model.configurable import (AIR_POLLUTION_MAX, AIR_POLLUTION_MIN, HEAT_MAX,
                                HEAT_MIN, NEIGHBOR_DIRECTIONS, WIND_STRENGTH_MAX,
                                WIND_STRENGTH_MIN)
from model.fields import Field, RangeField
from model.position import Coordinate, Position


@dataclass
class Heat(RangeField):
    def __init__(self, value: Optional[int] = None):
        super().__init__(value)

    @property
    def min(self):
        return HEAT_MIN

    @property
    def max(self):
        return HEAT_MAX


@dataclass
class Rain(Field):
    def __init__(self, value: bool = False):
        super().__init__(value)


@dataclass
class IsCloudPresent(Field):
    def __init__(self, value: bool = False):
        super().__init__(value)


@dataclass
class Cloud:
    cloud: IsCloudPresent
    rain: Rain

    def __init__(
        self, cloud: Optional[IsCloudPresent] = None, rain: Optional[Rain] = None
    ):
        self.cloud = IsCloudPresent() if cloud is None else cloud
        self.rain = Rain() if rain is None else rain


@dataclass
class WindStrength(RangeField):
    def __init__(self, value: Optional[int] = None):
        super().__init__(value)

    @property
    def min(self):
        return WIND_STRENGTH_MIN

    @property
    def max(self):
        return WIND_STRENGTH_MAX


@dataclass
class WindDirection(Field):
    def __init__(self, value: Position = None):
        if value is None:
            direction = choice(NEIGHBOR_DIRECTIONS)
            value = Position(*direction)
        super().__init__(value)


@dataclass
class Wind:
    strength: WindStrength
    direction: WindDirection

    def __init__(
        self,
        strength: Optional[WindStrength] = None,
        direction: Optional[WindDirection] = None,
    ):
        self.strength = WindStrength() if strength is None else strength
        self.direction = WindDirection() if direction is None else direction


@dataclass
class AirPollution(RangeField):
    def __init__(self, value=0):
        super().__init__(value)

    @property
    def min(self):
        return AIR_POLLUTION_MIN

    @property
    def max(self):
        return AIR_POLLUTION_MAX
