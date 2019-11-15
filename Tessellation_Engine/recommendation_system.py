# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:24:36 2019

Class for generating alternate tessellations
Currently only supports rotating regular polygons
"""

from shapely.geometry import * # for geometric objects
import math # for trig functions
from Tessellation_Engine import tessellation_engine as te # for displaying shapes
#import tessellation_engine as te
from shapely import affinity # for transformation

# determines details about polygon then calls various generation functions
def generateRecommendations(polygon, xNum, yNum):
    p1 = polygon.exterior.coords[0]
    p2 = polygon.exterior.coords[1]
    point1 = Point(p1[0], p1[1])
    point2 = Point(p2[0], p2[1])
    length = point1.distance(point2) # side length
    numSides = len(polygon.exterior.coords) - 1 # total number of sides
    print(numSides)
    angleSum = (numSides - 2) * 180 # sum of interior angles
    angle = angleSum / numSides # degree of single interior angle
    rotated(polygon, angleSum, angle, xNum, yNum)
     
# generates alternate tilings by rotating base unit by half of interior angle
# for shapes with odd numbers of sides and by a fourth of the interior angle for
# shapes with even numbers of sides
def rotated(polygon, angleSum, angle, xNum, yNum):
    numSides = len(polygon.exterior.coords) - 1
    if numSides % 2 == 0 and numSides > 4:
        increment = angle / 4
    else:
        increment = angle / 2
    print(increment)
    current = 0
    generated = []
    while current < (angleSum - angle):
        start = polygon.exterior.coords[0]
        if not isRedundant(start, generated):
            te.tileRegularPolygon(polygon, xNum, yNum)
        for p in polygon.exterior.coords:
            generated.append((p[0],p[1]))
        polygon = affinity.rotate(polygon, increment)
        current = current + increment

# compares the provided point with the points in the already generated array.
# if there is an exact match or a match that is +/- 0.1 the point is considered redundant.
# if the function returns True, no tiling is created using these points    
def isRedundant(point, generated):
    offset = 20
    for p in generated:
        if p == point:
            return True
        elif abs(p[0] - point[0]) <= offset and abs(p[1] - point[1]) <= offset:
            return True
    return False
            