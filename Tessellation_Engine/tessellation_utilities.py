"""
tessellation_utilities.py
Set of backend utilities for manipulating Polygon objects and coordinate lists for display on tessellation widget
"""

from shapely.geometry import Polygon

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