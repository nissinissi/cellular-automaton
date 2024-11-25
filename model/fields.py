from dataclasses import dataclass
from random import randint


@dataclass
class Field:
    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(self._value)

    @property
    def value(self):
        return self._value


@dataclass
class RangeField(Field):
    def __init__(self, value=None):
        if value is not None:
            super().__init__(value)
        else:
            super().__init__(randint(self.min, self.max + 1))

    def __hash__(self):
        return super().__hash__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert self.min <= value <= self.max
        self._value = value

    @property
    def min(self):
        raise NotImplementedError()

    @property
    def max(self):
        raise NotImplementedError()
