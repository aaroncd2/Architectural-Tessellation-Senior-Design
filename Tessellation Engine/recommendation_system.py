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

def generateRecommendations(polygon, xNum, yNum):
     length = polygon[0].distance(polygon[1]) # side length
     numSides = len(polygon) # total number of sides
     angleSum = (numSides - 2) * 180 # sum of interior angles
     angle = angleSum / numSides # degree of single interior angle
     rotated(polygon, angleSum, angle, xNum, yNum)
     
def rotated(polygon, angleSum, angle, xNum, yNum):
    increment = angle / 2
    current = 0
    while current < (angleSum - angle):
        te.tileRegularPolygon(polygon, xNum, yNum)
        polygon = affinity.rotate(polygon, increment)
        current = current + increment