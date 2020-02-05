from shapely.geometry import Polygon
from shapely.geometry import Point

def identify_shape(shape):
    if (not is_regular(shape)):
        print("irregular")
        number_sides = num_sides(shape)
        if (num_sides == 3):
            process_triangle(shape)
        elif (num_sides == 4):
            process_quadrilateral(shape)
    else:
        print("regular")
        # process to tessellation engine

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

def process_triangle(shape):
    # duplicate triangle and fit side together to make a quad
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
    side1_length = ((coords[1][1] - coords[0][1])**2 + (coords[1][0] - coords[0][0])**2)**0.5
    side2_length = ((coords[2][1] - coords[1][1])**2 + (coords[2][0] - coords[1][0])**2)**0.5
    side3_length = ((coords[3][1] - coords[2][1])**2 + (coords[3][0] - coords[2][0])**2)**0.5
    side4_length = ((coords[4][1] - coords[3][1])**2 + (coords[4][0] - coords[3][0])**2)**0.5
    if num_sides(shape) == 4 and side1_length == side3_length and side2_length == side4_length:
        # shape is a parallelogram
        pass
    else:
        pass
        # duplicate quad and fit longer sides together to make a hexagon
    
def process_hexagon(shape):
    pass 