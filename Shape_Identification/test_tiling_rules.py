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
    generic_test("square", tr.__is_regular(square), True)
    generic_test("rectangle", tr.__is_regular(rectangle), False)
    generic_test("arrow", tr.__is_regular(arrow), False)
    generic_test("box_c", tr.__is_regular(box_c), False)
    print()

def test_convex():
    print("-----CONVEX TEST-----")
    generic_test("square", tr.__is_convex(square)[0], True)
    generic_test("rectangle", tr.__is_convex(rectangle)[0], True)
    generic_test("triangle_1", tr.__is_convex(triangle_1)[0], True)
    generic_test("triangle_2", tr.__is_convex(triangle_2)[0], True)
    generic_test("triangle_3", tr.__is_convex(triangle_3)[0], True)
    generic_test("arrow", tr.__is_convex(arrow)[0], False)
    generic_test("box_c", tr.__is_convex(box_c)[0], False)
    print()

# shapely shape objects (triangles)
triangle_1 = Polygon([(0, 0), (2, 0), (0, 4), (0, 0)])
triangle_2 = Polygon([(0, 4), (0, 1), (2, -2), (0, 4)])
triangle_3 = Polygon([(4, 4), (6, 1), (2, -2), (4, 4)])
triangles = [triangle_1, triangle_2, triangle_3]

# shapely shape objects (convex quads)
concave_quad_1 = Polygon([(0, 0), (-2, 5), (7, 1), (-2, -2), (0, 0)])
concave_quad_2 = Polygon([(4, 5), (2.5, 3.7), (0, 4), (3, 3), (4, 5)])
concave_quad_3 = Polygon([(0, 0), (4, 4), (8, 0), (4, 1), (0, 0)])
convex_quad_1 = Polygon([(0, 0), (4, 4), (8, 0), (5, -1), (0, 0)])
convex_quad_2 = Polygon([(0, 0), (7, 0), (5, 2), (3, 3), (0, 0)])
concave_quads = [concave_quad_1, concave_quad_2, concave_quad_3]
convex_quads = [convex_quad_2]

# boolean that represents whether all the tests have passed or not
all_tests_passed = True

# calls to each series of tests
# for triangle in triangles:
    # plot_polygon(triangle)
    # triangle_recommendations = tr.identify_shape(triangle)
    # for recommendation in triangle_recommendations:
        # plot_polygon(recommendation[0])
        # plot_polygon(recommendation[3])

# for concave_quad in concave_quads:
    # plot_polygon(concave_quad)
    # quad_recommendations = tr.identify_shape(concave_quad)
    # for recommendation in quad_recommendations:
        # plot_polygon(recommendation[0])
        # plot_polygon(recommendation[3])

for convex_quad in convex_quads:
    plot_polygon(convex_quad)
    quad_recommendations = tr.identify_shape(convex_quad)
    for recommendation in quad_recommendations:
        plot_polygon(recommendation[0])
        plot_polygon(recommendation[3])

# logic for printing out overall test results
if all_tests_passed:
    print("-----ALL TESTS HAVE PASSED-----")
else:
    print("-----SOME TESTS HAVE FAILED-----")
