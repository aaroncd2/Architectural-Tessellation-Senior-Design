"""
tessellation_utilities.py
Set of backend utilities for manipulating Polygon objects and coordinate lists for display on tessellation widget
"""

from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.ops import triangulate
from kivy.graphics.tesselator import Tesselator

# Takes a Shapely Polygon object and converts it to an array format for display
# on a Kivy canvas 
def shapely_to_kivy(polygon):
    kivy_points = []
    for p in polygon.exterior.coords:
        kivy_points.append(p[0])
        kivy_points.append(p[1])
    return kivy_points

# Takes a list of points in kivy format ([x0,y0,x1,y1,...,xn,yn])
# returns list of tuples in shapely format ([(x0,y0),(x1,y1),...,(xn,yn)])
def kivy_to_shapely(polygon):
        shapely_points = []
        xs = []
        ys = []
        count = 0
        for p in polygon:
            if count % 2 == 0:
                xs.append(p)
            else:
                ys.append(p)
            count = count + 1
        for (x,y) in zip(xs,ys):
            shapely_points.append((x,y))
        return shapely_points

#offsets a polygon to ensure all its vertices are positive
def make_positive(polygon):
    bounds = polygon.bounds
    temp = []
    if bounds[0] < 0 and bounds[1] < 0:
        for p in polygon.exterior.coords:
            temp.append((p[0] + abs(bounds[0]), p[1] + abs(bounds[1])))
        return Polygon(temp)
    elif bounds[1] < 0:
        for p in polygon.exterior.coords:
            temp.append((p[0], p[1] + abs(bounds[1])))
        return Polygon(temp)
    elif bounds[0] < 0:
        for p in polygon.exterior.coords:
            temp.append((p[0] + abs(bounds[0]), p[1]))
        return Polygon(temp)
    else:
        return polygon

# creates a list of points for drawing mesh
def make_mesh_list(polygon):
    tess = Tesselator()
    tess.add_contour(polygon)
    tess.tesselate()
    return tess

# determines whether a polygon is convex or not
def is_convex(shape):
    coords = list(shape.exterior.coords)
    positive_z_coords = list()
    negative_z_coords = list()
    # starting z component coord calculation
    if compute_z_cross_product(coords[len(coords) - 2], coords[0], coords[1]) >= 0:
        positive_z_coords.append(0)
    else:   
        negative_z_coords.append(0)
    # rest of the z component coord calculation
    for i in range(1, len(coords) - 1):
        if compute_z_cross_product(coords[i - 1], coords[i], coords[i + 1]) >= 0:
            positive_z_coords.append(i)
        else:   
            negative_z_coords.append(i)
    if len(positive_z_coords) > 0 and len(negative_z_coords) > 0:
        # the shape is concave
        if len(positive_z_coords) > len(negative_z_coords):
            return False, negative_z_coords
        else:
            return False, positive_z_coords
    else:
        # the shape is convex
        return True, list()

def compute_z_cross_product(first_coord, second_coord, third_coord):
    dx1 = second_coord[0] - first_coord[0]
    dy1 = second_coord[1] - first_coord[1]
    dx2 = third_coord[0] - second_coord[0]
    dy2 = third_coord[1] - second_coord[1]
    return dx1 * dy2 - dy1 * dx2