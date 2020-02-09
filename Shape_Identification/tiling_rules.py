'''
tiling_rules.py
    Contains various rules and tests to determine
    different properties of polygons before they are passed
    into the tessellation engine
'''
from shapely.geometry import Polygon
from shapely.geometry import Point

def identify_shape(shape):
    if (is_regular(shape)):
        # process to tessellation engine
        return shape
    else:
        number_sides = num_sides(shape)
        if (num_sides == 3):
            return process_triangle(shape)
        elif (num_sides == 4):
            return process_quadrilateral(shape)

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

def is_convex(shape):
    coords = list(shape.exterior.coords)
    positive_z = __compute_z_cross_product(coords[0], coords[1], coords[2]) >= 0
    for i in range(1, len(coords) - 2):
        if (__compute_z_cross_product(coords[i], coords[i + 1], coords[i + 2]) >= 0) != positive_z:
            return False
    return True

def __compute_z_cross_product(first_coord, second_coord, third_coord):
    dx1 = second_coord[0] - first_coord[0]
    dy1 = second_coord[1] - first_coord[1]
    dx2 = third_coord[0] - second_coord[0]
    dy2 = third_coord[1] - second_coord[1]
    return dx1 * dy2 - dy1 * dx2

# duplicates triangle and fit sides together to make a parallelogram
def process_triangle(shape):
    coords = list(shape.exterior.coords)
    x_length = coords[2][0] - coords[1][0]
    y_length = coords[2][1] - coords[1][1]
    triangle_final_coord = coords[len(coords) - 1]
    connection_coords = tuple((triangle_final_coord[0] + x_length, triangle_final_coord[1] + y_length))
    coords.append(connection_coords)
    coords.append(coords[2])
    return Polygon(coords)

def is_parallelogram(shape):
    coords = shape.exterior.coords
    side1_length = ((coords[1][1] - coords[0][1])**2 + (coords[1][0] - coords[0][0])**2)**0.5
    side2_length = ((coords[2][1] - coords[1][1])**2 + (coords[2][0] - coords[1][0])**2)**0.5
    side3_length = ((coords[3][1] - coords[2][1])**2 + (coords[3][0] - coords[2][0])**2)**0.5
    side4_length = ((coords[4][1] - coords[3][1])**2 + (coords[4][0] - coords[3][0])**2)**0.5
    return num_sides(shape) == 4 and side1_length == side3_length and side2_length == side4_length

def process_quadrilateral(shape):
    coords = shape.exterior.coords
    side4_length = ((coords[4][1] - coords[3][1])**2 + (coords[4][0] - coords[3][0])**2)**0.5
    if is_parallelogram(shape):
        return "parallelogram"
    elif:
        pass
        # duplicate quad and fit longer sides together to make a hexagon
    
def process_hexagon(shape):
    pass 