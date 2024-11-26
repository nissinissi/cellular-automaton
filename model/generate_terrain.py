from itertools import product
from math import exp, pi
from random import choice, choices, random, uniform

from model.configurable import CELL_TYPE_WEIGHTS, CELL_TYPES, GRID_SIZE


def gaussian_2d(m_x: float, s_x: float, m_y: float, s_y: float, p: float):
    # https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Bivariate_case
    return lambda x, y: exp(
        (
            2 * p * (x - m_x) * (y - m_y) / (s_x * s_y)
            - (x - m_x) * (x - m_x) / s_x / s_x
            - (y - m_y) * (y - m_y) / s_y / s_y
        )
        / 2
        / (1 - p * p)
    ) / (2 * pi * s_x * s_y * (1 - p**2) ** 0.5)


def random_2d_gaussian(grid_size: int):
    m0, m1 = choices(range(grid_size), k=2)
    s0, s1 = (uniform(grid_size / 12, grid_size / 5) for _ in range(2))
    p = uniform(-1, 1)
    return gaussian_2d(m0, s0, m1, s1, p)


def generate_terrain():
    n_distributions = int(GRID_SIZE * 4)
    terrain = [[(0, 0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    for i in range(n_distributions):
        current_class = choices(CELL_TYPES, weights=CELL_TYPE_WEIGHTS)[0]
        new_gaussian = random_2d_gaussian(GRID_SIZE)
        new_distribution = [
            [(new_gaussian(x, y), current_class) for x in range(GRID_SIZE)]
            for y in range(GRID_SIZE)
        ]
        for x, y in product(range(GRID_SIZE), repeat=2):
            if terrain[x][y][0] < new_distribution[x][y][0]:
                terrain[x][y] = new_distribution[x][y]
    return terrain
