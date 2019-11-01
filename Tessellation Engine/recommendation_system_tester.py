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

square = MultiPoint([(0,0),(0,1),(1,1),(1,0)])
rs.generateRecommendations(square, 5, 5)

triangle = MultiPoint([(2,1),(4.5,16/3),(7,1)])
rs.generateRecommendations(triangle, 4, 6)

"""
pentagon = MultiPoint([(2,6),(0,4),(.5,1),(3.5,1),(4,4)])
rs.generateRecommendations(pentagon, 5, 5)
"""