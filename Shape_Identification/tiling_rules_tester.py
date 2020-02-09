import tiling_rules as tr
from shapely.geometry import Polygon
import matplotlib.pyplot as plt 

# shapely shape objects
triangle_1 = Polygon([(0, 0), (2, 0), (0, 4), (0, 0)])
triangle_2 = Polygon([(0, 4), (0, 1), (2, -2), (0, 4)])
triangle_3 = Polygon([(4, 4), (6, 1), (2, -2), (4, 4)])
square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
rectangle = Polygon([(0, 0), (2, 0), (2, 5), (0, 5), (0, 0)])

# generic testing method
def generic_test(shape, actual, expected):
    if expected == actual:
        print(shape, ": TEST PASSED")
    else:
        print(shape, ": TEST FAILED")

def plot_polygon(shape):
    x, y = shape.exterior.xy
    plt.axis('equal')
    plt.plot(x, y)
    plt.show()

def test_regular_polygons():
    print("-----REGULAR POLYGON TEST-----")
    generic_test("square", tr.is_regular(square), True)
    generic_test("rectangle", tr.is_regular(rectangle), False)
    print()

def test_parallelograms():
    print("-----PARALLELOGRAM TEST-----")
    generic_test("square", tr.is_parallelogram(square), True)
    generic_test("rectangle", tr.is_parallelogram(rectangle), True)
    print()

def test_convex():


plot_polygon(tr.process_triangle(triangle_3))
test_regular_polygons()
test_parallelograms()