# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:49:32 2019

@author: Aaron Dodge
File for testing the tessellation engine
"""

from shapely.geometry import * # for geometric objects
import math # for trig functions
import tessellation_engine as te # for displaying shapes

square = MultiPoint([(0,0),(0,1),(1,1),(1,0)])
print("4x4 tiling of a square")
te.tileRegularPolygon(square, 4, 4)

triangle = MultiPoint([(2,1),(4.5,16/3),(7,1)])
print("7x3 tiling of a triangle")
te.tileRegularPolygon(triangle, 7, 3)

pentagon = MultiPoint([(550,450),(455,519),(491,631),(609,631),(645,519)])
print("5x4 tiling of a pentagon")
te.tileRegularPolygon(pentagon,5,4)

octagon = MultiPoint([(1,0),(math.sqrt(2)/2,math.sqrt(2)/2),(0,1),(-math.sqrt(2)/2,math.sqrt(2)/2),(-1,0),(-math.sqrt(2)/2,-math.sqrt(2)/2),(0,-1),(math.sqrt(2)/2,-math.sqrt(2)/2)])
print("4x6 tiling of an octagon")
te.tileRegularPolygon(octagon, 4, 6)


star = MultiPoint([(4,4),(0,4),(3.5,1),(2,6),(.5,1)])
print("Trying to tile a star")
te.tileRegularPolygon(star,5,5)

rhombus = MultiPoint([(0,0),(5,0),(8,4),(3,4)])
print("Trying to tile a rhombus")
te.tileRegularPolygon(rhombus, 5, 5)