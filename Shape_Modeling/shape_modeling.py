from shapely.geometry import Polygon
from shapely import affinity
from shapely.geometry import Point
import matplotlib.pyplot as plt

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
    x,y = poly2.exterior.xy
    plt.plot(x,y)

    poly2_simple = Polygon(poly2.simplify(20))
    x,y = poly2_simple.exterior.xy
    plt.plot(x,y)

    poly3= affinity.scale(poly2_simple, xfact= .5, yfact= .5)
    x,y = poly3.exterior.xy
    plt.plot(x,y)
    plt.show()