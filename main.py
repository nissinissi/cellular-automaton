from logging import getLogger, StreamHandler, INFO, FileHandler
from os import mkdir
from os.path import join
from pathlib import Path
from sys import argv, stdout
from datetime import datetime
from typing import Optional

from model import configurable
from model.configurable import DAY_COUNT
from model.grid import Grid
from model.statistics import Statistics
from view.display import Graphics
from view.textures import texture_by_name


def get_logger(output_directory: Path):
    logger = getLogger()
    logger.setLevel(INFO)

    stdout_handler = StreamHandler(stdout)
    stdout_handler.setLevel(INFO)
    logger.addHandler(stdout_handler)

    file_handler = FileHandler(join(output_directory.resolve(), "output.txt"))
    file_handler.setLevel(INFO)
    logger.addHandler(file_handler)
    return logger


def display_step(logger, day, graphics, grid) -> None:
    logger.info(f"Day: {day + 1}/{DAY_COUNT}")
    statistics_str = Grid.statistics_str(grid.get_statistics(for_printing=True))
    logger.info(statistics_str)
    logger.info(graphics.get_grid_str(grid))


def get_graphics_texture(logger) -> Optional[dict]:
    assert len(argv) <= 2, "Too many parameters were passed."
    if len(argv) == 2:
        if argv[1] in ("-h", "--help"):
            logger.info("Try running `python main.py [live|block]`")
        return texture_by_name(argv[1])
    return None

def create_output_directory() -> Path:
    directory_name = datetime.now().strftime("%Y-%m-%d-%H:%m:%S")
    mkdir(directory_name)
    return Path(directory_name)

def log_configurable_values(destination_directory: Path) -> None:
    configurable_values = Path(configurable.__file__)
    Path(join(destination_directory, "configurable.txt")).write_text(configurable_values.read_text())

def main():
    output_directory = create_output_directory()
    log_configurable_values(output_directory)
    logger = get_logger(output_directory)

    graphics = Graphics(get_graphics_texture(logger))
    grid = Grid()
    statistics = Statistics(logger)

    display_step(logger, 0, graphics, grid)

    for day in range(1, DAY_COUNT):
        grid.step()
        display_step(logger, day, graphics, grid)
        statistics.sample(grid)

    statistics.display_statistics(optional_output_directory=Path(join(output_directory, "plot.png")), should_show=False)


if __name__ == "__main__":
    main()
