from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
import numpy as np

def identify_shape(shape):
    print(is_regular(shape))

def num_sides(shape):
    return len(shape.exterior.coords) - 1

def is_regular(shape):
    coords = shape.exterior.coords
    points = []
    for c in coords:
        points.append(Point(c[0], c[1]))
    starting_edge_length = points[0].distance(points[1])
    for i in range(1, len(points) - 1):
        current_edge_length = points[i].distance(points[i + 1])
        if (round(current_edge_length, 2) != round(starting_edge_length, 2)):
            return False
    return True