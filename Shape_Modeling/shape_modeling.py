from shapely.geometry import Polygon
from shapely import affinity
from shapely.geometry import Point
import matplotlib.pyplot as plt
import math
from shapely.geometry import MultiPoint


def shape_model(coords):
    ax = plt.axes()
    ax.set_facecolor("white")
    plt.grid(True)

    points = list(zip(coords[::2],coords[1::2]))

    poly = Polygon(points)
    x,y = poly.exterior.xy
    # plt.plot(x,y)

    x = (-(poly.centroid.x))
    y = (-(poly.centroid.y))
    poly2 = affinity.translate(poly, xoff= x, yoff= y)
    x,y = poly2.exterior.xy
    # plt.plot(x,y)

    poly2_simple = Polygon(poly2.simplify(35))
    x,y = poly2_simple.exterior.xy
    # plt.plot(x,y)

    poly3= affinity.scale(poly2_simple, xfact= .5, yfact= .5)
    x,y = poly3.exterior.xy
    # plt.plot(x,y)

    coords = list(poly3.exterior.coords)
    coords = coords[:-1]
    sides = len(coords) 
    n = 0
    angle_total = 0
    while n < sides:
        angle_total = angle_total + angle(coords[n % sides], coords[(n + 1) % sides], coords[(n + 2) % sides])
        n = n + 1

    avg_angle = angle_total/sides 
    inner_angle = (sides-2) * 180 / n

    if sides <= 8 and ((inner_angle + 5) > avg_angle > (inner_angle - 5)):
        poly3 = regular_poly(sides)
    x,y = poly3.exterior.xy
    plt.plot(x,y)
    plt.show()
    return poly3

#Finds angle between 3 points
def angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
 

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
        points = [(0,-15),(-13,7),(13,8)]
    else:
        print ("not valid side number")
    return Polygon(points)

