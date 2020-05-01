from shapely.geometry import Polygon
from shapely import affinity
from shapely.geometry import Point
import matplotlib.pyplot as plt
import math
from shapely.geometry import MultiPoint
import numpy as np

points_to_be_deleted = []


def shape_model(coords):
    ax = plt.axes()
    ax.set_facecolor("white")
    plt.grid(True)

    points = list(zip(coords[::2],coords[1::2]))

    poly = Polygon(points)
    x,y = poly.exterior.xy
    plt.plot(x,y)


    x = (-(poly.centroid.x))
    y = (-(poly.centroid.y))
    poly2 = affinity.translate(poly, xoff= x, yoff= y)

    poly2_simple = Polygon(poly2.simplify(35))
    x,y = poly2_simple.exterior.xy
    plt.plot(x,y)

    poly3= affinity.scale(poly2_simple, xfact= .5, yfact= .5)

    coords = list(poly3.exterior.coords)

    if len(coords) > 12:
        print('here0') 
        poly3 = Polygon(poly3.simplify(40))
    print(len(coords))


    coords = coords[:-1]
    sides = len(coords) 
    n = 0
    angles = []
    while n < sides:
        angles.append(angle(coords[n % sides], coords[(n + 1) % sides], coords[(n + 2) % sides]))
        n = n + 1
    print((sides + 1)-len(points_to_be_deleted))

    print(len(angles))
    if sides > 6:
        print('here')
        anomalies = find_anomalies(angles)
        print(anomalies)
        for elem in anomalies:
            angles.remove(elem)
    else:
        print('here2')
        outliers = angle_outside_range(angles)
        angles = remove_max(angles, outliers)
    print(len(angles))

    sides = len(angles) 
    
    avg_angle = sum(angles)/sides 
    inner_angle = (sides-2) * 180 / sides


    # if sides <= 8 and ((inner_angle + 10) > avg_angle > (inner_angle - 10)):
    #    poly3 = regular_poly(sides)

    x,y = poly3.exterior.xy
    plt.plot(x,y)
    # plt.show()
    return poly3.exterior.coords

#Finds angle between 3 points
def angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    if ang < 0:
        ang = ang + 360
    if ang > 140:
        points_to_be_deleted.append(b)
    return ang
 
def regular_poly(n):
    if n == 8:
        points = [(6,-14),(-6,-14),(-14,-6),(-14,6),(-6,14),(6,14),(14,6),(14,-6)]
    elif n == 7:
        points = [(0,-15),(-12,-9),(-15,3),(-7,14),(7,14),(15,3),(12,-9)]
    elif n == 6:
        points = [(7,-13),(-8,-13),(-15,0),(-7,13),(7,13),(15,0)]
    elif n == 5:
        points = [(0,-15),(-14,-5),(-9,12),(9,12),(14,-5)]
    elif n == 4:
        points = [(11,-11),(-11,-11),(-11,11),(11,11)]
    elif n == 3:
        points = [(0,15.77),(-18,-16),(18,-16)]
    else:
        print ("not valid side number")
    return Polygon(points)

def angle_outside_range(angles):
    count = 0
    for elem in angles:
        if elem >= 135:
            count = count + 1
    return count

def find_anomalies(angles):
    anomalies = []

    angles_std = np.std(angles)
    angles_mean = np.mean(angles)
    anomaly_cut_off = angles_std * 2

    
    lower_limit  = angles_mean - anomaly_cut_off 
    upper_limit = angles_mean + anomaly_cut_off
    # Generate outliers
    for outlier in angles:
        if outlier > upper_limit or outlier < lower_limit:
            anomalies.append(outlier)
  
    return anomalies

def remove_max(angels, outliers):
    n = 0
    while n < outliers:
        angels.remove(max(angels))
        n = n + 1
    return angels

