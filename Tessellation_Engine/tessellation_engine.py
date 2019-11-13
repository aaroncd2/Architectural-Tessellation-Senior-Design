# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:06:12 2019

This class functions as the primary tessellation engine for the application.
It offers functions for displaying both single polygon and multiple polygons.
Additionally, It can create regular tilings of a single polygon
"""

from shapely.geometry import * # for geometric objects
from shapely.affinity import * # for transformations
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export

# simple function for displaying a single polygon with matplotlib.
# Used to display a base unit
# INPUT: A single shapely MultiPoint object
# OUTPUT: Displays matplotlib plot of shapes
# RETURNS: None
def displayPolygon(polygon):
    x = []
    y = []
    # add all coordinates
    for p in polygon:
        x.append(p.x)
        y.append(p.y)
    # add first coordinate again to complete shape for display
    x.append(polygon[0].x)
    y.append(polygon[0].y)
    plt.plot(x,y)
    plt.show()
    
# simple function for displaying array of shapes with matplotlib.
# Used to display a tiling
# INPUT: An array of shapely MultiPoints
# OUTPUT: Displays matplotlib plot of shapes
# RETURNS: None
def displayPolygons(polygons):
    for poly in polygons:
        x = []
        y = []
        first = poly[0]
        for p in poly:
            x.append(p.x)
            y.append(p.y)
        x.append(first.x)
        y.append(first.y)
        plt.plot(x,y)
    plt.show()
    print()

# generates a tiling for regular polygons
# INPUT: A shapely MultiPointObject, number of tiles in x direction, number of tiles in y direction
# OUTPUT: NONE
# RETURNS: NONE
def tileRegularPolygon(polygon, xNum, yNum):
    bounds = polygon.bounds # returns a tuple of (xmin, ymin, xmax, ymax)
    xIncrement = abs(bounds[2] - bounds[0])
    yIncrement = abs(bounds[3] - bounds[1])

    polygons = []
    temp = []
    xCount = 1
    yCount = 1
    while yCount <= yNum:
        while xCount <= xNum: 
            xNext = xCount * xIncrement
            yNext = yCount * yIncrement
            for p in polygon.exterior.coords:
                temp.append((p[0] + xNext, p[1] + yNext))
            polygons.append(MultiPoint(temp))
            xCount = xCount + 1
            temp = []
        yCount = yCount + 1
        xCount = 1
    displayPolygons(polygons)
    return polygons

# Exports array of multipoints into a column of X coordinates and Y coordinates
# in a CSV file called output.csv
def exportTiling(polygons):
    points = {}
    num = 1
    for poly in polygons:
        xs = []
        ys = []
        for p in poly:
            xs.append(p.x)
            ys.append(p.y)
        points['x' + str(num)] = xs
        points['y' + str(num)] = ys
        num += 1
    df = pd.DataFrame(points)
    df.to_csv(r'Output/output.csv', index=False)