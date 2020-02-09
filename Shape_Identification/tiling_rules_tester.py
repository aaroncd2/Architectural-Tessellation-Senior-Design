'''
tiling_rules_tester.py:
    testing file for testing out different rules
    laid out in the tiling_rules.py file
'''
import tiling_rules as tr
from shapely.geometry import Polygon
import matplotlib.pyplot as plt 

def generic_test(shape, actual, expected):
    if expected == actual:
        print(shape, ": TEST PASSED")
    else:
        all_tests_passed = False
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
    generic_test("arrow", tr.is_regular(arrow), False)
    print()

def test_parallelograms():
    print("-----PARALLELOGRAM TEST-----")
    generic_test("square", tr.is_parallelogram(square), True)
    generic_test("rectangle", tr.is_parallelogram(rectangle), True)
    generic_test("arrow", tr.is_parallelogram(arrow), False)
    print()

def test_convex():
    print("-----CONVEX TEST-----")
    generic_test("square", tr.is_convex(square), True)
    generic_test("rectangle", tr.is_convex(rectangle), True)
    generic_test("triangle_1", tr.is_convex(triangle_1), True)
    generic_test("triangle_2", tr.is_convex(triangle_2), True)
    generic_test("triangle_3", tr.is_convex(triangle_3), True)
    generic_test("arrow", tr.is_convex(arrow), False)
    print()

# shapely shape objects
triangle_1 = Polygon([(0, 0), (2, 0), (0, 4), (0, 0)])
triangle_2 = Polygon([(0, 4), (0, 1), (2, -2), (0, 4)])
triangle_3 = Polygon([(4, 4), (6, 1), (2, -2), (4, 4)])
square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
rectangle = Polygon([(0, 0), (2, 0), (2, 5), (0, 5), (0, 0)])
arrow = Polygon([(4, 5), (2.5, 3.7), (0, 4), (3, 3), (4, 5)])

# boolean that represents whether all the tests have passed or not
all_tests_passed = True

# calls to each series of tests
test_regular_polygons()
test_parallelograms()
test_convex()

# logic for printing out overall test results
if all_tests_passed:
    print("-----ALL TESTS HAVE PASSED-----")
else:
    print("-----SOME TESTS HAVE FAILED-----")