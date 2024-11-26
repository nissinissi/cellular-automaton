import math
from collections.abc import Iterable
from pathlib import Path
from typing import List, Sequence, Optional
from matplotlib import pyplot as plt

from model.configurable import EPSILON
from model.grid import Grid


class Statistics:
    def __init__(self, logger):
        self._samples = []
        self._logger = logger

    @staticmethod
    def _get_single_value(value):
        return value if not isinstance(value, Iterable) else value[0]

    @staticmethod
    def _unpack_statistics(statistics: dict):
        return {key: Statistics._get_single_value(value) for key, value in statistics.items()}

    def sample(self, grid: Grid):
        self._samples.append(Statistics._unpack_statistics(grid.get_statistics()))

    def display_statistics(self, should_show=True, optional_output_directory: Optional[Path]=None):
        assert len(self._samples) > 0
        keys = self._samples[0].keys()
        for key in keys:
            self.display_metric(key)
        plt.legend(bbox_to_anchor=(0.9, 0.5), loc="center left")
        if optional_output_directory is not None:
            plt.savefig(optional_output_directory.resolve(), bbox_inches="tight")
        if should_show:
            plt.subplots_adjust(right=0.7)
            plt.show()

    def _get_normalized_values(self, values: Sequence[float]) -> List[float]:
        avg = sum(values) / len(values)
        std_dev = sum((value - avg) * (value - avg) for value in values) ** 0.5
        std_dev = std_dev if std_dev > 0 else EPSILON
        self._logger.info(f"{avg=}")
        self._logger.info(f"{std_dev=}")
        return [(value - avg) / std_dev for value in values]

    def display_metric(self, key):
        self._logger.info(f"~~ {key} ~~")
        key_samples = [sample[key] for sample in self._samples]
        normalized_key_samples = self._get_normalized_values(key_samples)
        plt.plot(range(len(normalized_key_samples)), normalized_key_samples, label=key)
