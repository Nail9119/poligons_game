import pygame
from math import cos, sin, pi
from pygame.surface import Surface, SurfaceType

from colors import *


def load_image(filename, colorkey=None) -> Surface | SurfaceType:
    image = pygame.image.load(filename)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_polygon_vertices(n, radius, rotation: float = 0.001):
    vertices = []
    for i in range(0, n):
        x = radius * cos(rotation + 2 * pi * i / n)
        y = radius * sin(rotation + 2 * pi * i / n)
        vertices.append((x, y))
    return vertices


def draw_hexagon(radius: int = 20, color: tuple = (255, 255, 255)):
    cx = cy = radius
    surface = pygame.surface.Surface((2 * radius, 2 * radius))
    vertices = map(lambda xy: (xy[0] + cx, xy[1] + cy), get_polygon_vertices(6, radius))
    pygame.draw.polygon(surface, color, list(vertices))
    return surface


def positions_field(width: int = 540, height: int = 700, radius: int = 20, padding: int = 4):
    field = []
    hex_side = radius * 2 * sin(pi / 6)
    hex_height = hex_side * cos(pi / 6)
    hex_width = hex_side * 2
    for i in range(0, int(height / (hex_height + padding))):
        row = []
        for j in range(0, int(width / ((hex_width + padding) * 1.5))):
            x = hex_width / 2 + j * (hex_width + padding) * 3 / 2 + (i % 2) * (hex_side + padding / 2) * 3 / 2
            y = -hex_height + i * (hex_height + padding)
            row.append((x, y))
        field.append(row)
    return field


def distance(point1: tuple, point2: tuple) -> float:
    x1, y1 = point1
    x2, y2 = point2
    squared_distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
    return squared_distance ** 0.5


def calculate_angular_coefficient(point1: tuple, point2: tuple) -> float:
    x1, y1 = point1
    x2, y2 = point2
    if x1 != x2:
        return (y1 - y2) / (x1 - x2)
    else:
        return -700


def intersection_ordinate(angular_coefficient: float, point1: tuple, x2) -> float:
    x1, y1 = point1
    y2 = angular_coefficient * (x2 - x1) + y1
    return y2


def nearest_point(point1, points) -> tuple:
    return min(points, key=lambda point2: distance(point1, point2))


def get_value_from(file: str) -> int:
    with open(file, "r") as file:
        line = file.readline()
        if line:
            return int(line)
        return 0


def set_value_to(file: str, record: int) -> None:
    with open(file, "w") as file:
        file.write(str(record))


def get_color_name(color: tuple) -> str:
    if color == black:
        return "Черный"
    if color == red:
        return "Красный"
    if color == gray_red:
        return "Темно-красный"
    if color == green:
        return "Зеленый"
    if color == blue:
        return "Синий"
    if color == yellow:
        return "Желтый"
    if color == peach:
        return "Персиковый"
    if color == purple:
        return "Фиолетовый"
    if color == cyan:
        return "Голубой"
    if color == gray:
        return "Серый"
    if color == white:
        return "Белый"
