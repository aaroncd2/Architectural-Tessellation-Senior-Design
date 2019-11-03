# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:24:36 2019

@author: Aaron Dodge
Class for generating alternate tessellations
Currently only supports rotating regular polygons
"""

from shapely.geometry import * # for geometric objects
import math # for trig functions
import tessellation_engine as te # for displaying shapes
from shapely import affinity # for transformation

# determines details about polygon then calls various generation functions
def generateRecommendations(polygon, xNum, yNum):
     length = polygon[0].distance(polygon[1]) # side length
     numSides = len(polygon) # total number of sides
     angleSum = (numSides - 2) * 180 # sum of interior angles
     angle = angleSum / numSides # degree of single interior angle
     rotated(polygon, angleSum, angle, xNum, yNum)
     
# generates alternate tilings by rotating base unit by half of interior angle
# for shapes with odd numbers of sides and by a fourth of the interior angle for
# shapes with even numbers of sides
def rotated(polygon, angleSum, angle, xNum, yNum):
    numSides = len(polygon)
    if numSides % 2 == 0 and numSides > 4:
        increment = angle / 4
    else:
        increment = angle / 2
    current = 0
    generated = []
    while current < (angleSum - angle):
        start = (polygon[0].x,polygon[0].y)
        if not isRedundant(start, generated):
            te.tileRegularPolygon(polygon, xNum, yNum)
        for p in polygon:
            generated.append((p.x,p.y))
        polygon = affinity.rotate(polygon, increment)
        current = current + increment
        
def isRedundant(point, generated):
    #print(point)
    #print(generated)
    for p in generated:
        if p == point:
            return True
        elif abs(p[0] - point[0]) <= 0.1 and abs(p[1] - point[1]) <= 0.1:
            return True
    return False
            