import tiling_rules as tr
from shapely.geometry import Polygon

# shapely shape objects
square = Polygon([(0,0), (1,0), (1,1), (0,1), (0,0)])
rectangle = Polygon([(0,0), (2,0), (2,5), (0,5), (0,0)])

# generic testing method
def generic_test(shape, actual, expected):
    if expected == actual:
        print(shape, ": TEST PASSED")
    else:
        print(shape, ": TEST FAILED")

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

# test calls
test_regular_polygons()
test_parallelograms()