# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:47:02 2019

@author: Aaron Dodge
"""

from shapely.geometry import * # for geometric objects
import math # for trig functions
import tessellation_engine as te # for displaying shapes
from shapely import affinity # for transformation
import recommendation_system as rs

square = MultiPoint([(0,0),(0,1),(1,1),(1,0)])
rs.generateRecommendations(square, 5, 5)

triangle = MultiPoint([(2,1),(4.5,16/3),(7,1)])
rs.generateRecommendations(triangle, 4, 6)

pentagon = MultiPoint([(550,450),(455,519),(491,631),(609,631),(645,519)])
rs.generateRecommendations(pentagon, 5, 5)