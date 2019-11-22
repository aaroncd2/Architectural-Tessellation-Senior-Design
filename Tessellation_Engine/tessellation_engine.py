# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:06:12 2019

This class functions as the primary tessellation engine for the application.
It offers functions for displaying both single polygon and multiple polygons.
Additionally, It can create regular tilings of a single polygon
"""

from shapely.geometry import * # for geometric objects
from shapely import affinity # for transformations
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export
import numpy as np # for math
import main as main
# simple function for displaying a single polygon with matplotlib.
# Used to display a base unit
# INPUT: A single shapely Polygon object
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
    #plt.show()
    
# simple function for displaying array of shapes with matplotlib.
# Used to display a tiling
# INPUT: An array of shapely Polygons
# OUTPUT: Displays matplotlib plot of shapes
# RETURNS: None
def displayPolygons(polygons, mainPlot, mainCanvas):
    mainPlot.clear()
    for poly in polygons:
        x = []
        y = []
        first = poly[0]
        for p in poly:
            x.append(p.x)
            y.append(p.y)
        x.append(first.x)
        y.append(first.y)
        mainPlot.plot(x,y)
    print()
    mainCanvas.draw()

# generates a tiling for regular polygons
# INPUT: A shapely Polygon, number of tiles in x direction, number of tiles in y direction,
#       an integer mode. 1 = standard, 2 = vertical flip, 3 = horizontal flip
# OUTPUT: NONE
# RETURNS: Array of Polygon objects
def tileRegularPolygon(polygon, xNum, yNum, mode, mainPlot, mainCanvas):
    bounds = polygon.bounds # returns a tuple of (xmin, ymin, xmax, ymax)
    xIncrement = abs(bounds[2] - bounds[0])
    yIncrement = abs(bounds[3] - bounds[1])

    polygons = []
    temp = []
    xCount = 1
    yCount = 1
    while yCount <= yNum:
        if(mode == 2):
            polygon = Polygon(flipPolygonVertically(polygon))
        if(mode == 3):
            polygon = Polygon(flipPolygonHorizontally(polygon))
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
    displayPolygons(polygons, mainPlot, mainCanvas)

# Function for mirroring a polygon horizontally across its center
# INPUT: Shapely Polygon object
def flipPolygonHorizontally(poly):
    pts = np.array(poly.exterior.coords)
    return pts.dot([[-1,0],[0,1]])

def flipPolygonVertically(poly):
    pts = np.array(poly.exterior.coords)
    return pts.dot([[1,0],[0,-1]])

# Exports array of multipoints into a column of X coordinates and Y coordinates
# in a CSV file called output.csv
# INPUT: Array of Shapely Polygon objects
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