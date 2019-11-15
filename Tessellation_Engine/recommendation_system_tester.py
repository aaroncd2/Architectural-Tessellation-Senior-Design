# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:47:02 2019

@author: Aaron Dodge
file for testing the recommendation system
"""

from shapely.geometry import * # for geometric objects
import math # for trig functions
import tessellation_engine as te # for displaying shapes
from shapely import affinity # for transformation
import recommendation_system as rs

square = Polygon([(0,0),(0,1),(1,1),(1,0)])
rs.generateRecommendations(square, 5, 5)

triangle = Polygon([(2,1),(4.5,16/3),(7,1)])
rs.generateRecommendations(triangle, 4, 6)

hexagon = Polygon([(-.5, math.sqrt(3)/2),(.5, math.sqrt(3)/2), (1,0), (.5, -math.sqrt(3)/2), (-.5, -math.sqrt(3)/2), (-1,0)])
rs.generateRecommendations(hexagon, 4, 4)

star = Polygon([(4,4),(0,4),(3.5,1),(2,6),(.5,1)])
rs.generateRecommendations(star,5,5)

rhombus = Polygon([(0,0),(5,0),(8,4),(3,4)])
rs.generateRecommendations(rhombus, 5, 5)
