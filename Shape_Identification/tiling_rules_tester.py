import tiling_rules as tr
from shapely.geometry import Polygon

# generic testing method
def test(test_name, shape, actual, expected):
    print("-----", test_name, "-----")
    if expected == actual:
        print(shape, ": TEST PASSED\n")
    else:
        print(shape, ": TEST FAILED\n")

# testing regular and irregular polygons
square = Polygon([(0,0), (1,0), (1,1), (0,1), (0,0)])
rectangle = Polygon([(0,0), (2,0), (2,5), (0,5), (0,0)])
test("REGULAR POLYGON TEST", "square", tr.is_regular(square), True)
test("REGULAR POLYGON TEST", "rectangle", tr.is_regular(rectangle), False)