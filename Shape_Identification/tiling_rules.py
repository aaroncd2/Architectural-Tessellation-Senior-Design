'''
tiling_rules.py
    Contains various rules and tests to determine
    different properties of polygons before they are passed
    into the tessellation engine
'''
from shapely.geometry import Polygon
from shapely.geometry import Point

'''public functions'''
# central function that takes in
# a shape and identifies / manipulate it
def identify_shape(shape):
    number_sides = __num_sides(shape)
    if (number_sides == 3):
        return process_triangle(shape) + process_universal(shape)
    elif (number_sides == 4):
        return process_quadrilateral(shape) + process_universal(shape)
    else:
        # generic recommendation
        return process_universal(shape)

# duplicates triangle and fit sides together to make a parallelogram
def process_triangle(shape):
    recommendations = list()
    original_coords = list(shape.exterior.coords)
    # determining lengths of each side to prepare for recommendations
    second_to_first_vertex_len_x = original_coords[1][0] - original_coords[2][0]
    second_to_first_vertex_len_y = original_coords[1][1] - original_coords[2][1]
    first_to_zeroth_vertex_len_x = original_coords[0][0] - original_coords[1][0]
    first_to_zeroth_vertex_len_y = original_coords[0][1] - original_coords[1][1]
    # first recommendation: flip on first edge to create a parallelogram
    first_rec_coords = list(original_coords)
    first_rec_coords.append((first_rec_coords[0][0] + second_to_first_vertex_len_x, first_rec_coords[0][1] + second_to_first_vertex_len_y))
    first_rec_coords.append(first_rec_coords[1])
    first_rec_exterior_coords = [first_rec_coords[0], first_rec_coords[2], first_rec_coords[1], first_rec_coords[4], first_rec_coords[0]]
    recommendations.append((Polygon(first_rec_coords), "parallelogram", True, Polygon(first_rec_exterior_coords)))
    # second recommendation: reflect on zeroth point and bound the box
    second_rec_coords = list(original_coords)
    second_rec_coords.append((second_rec_coords[0][0] + first_to_zeroth_vertex_len_x, second_rec_coords[0][1] + first_to_zeroth_vertex_len_y))
    second_rec_coords.append((second_rec_coords[4][0] + second_to_first_vertex_len_x, second_rec_coords[4][1] + second_to_first_vertex_len_y))
    second_rec_coords.append(second_rec_coords[0])
    second_rec_coords.append(second_rec_coords[1])
    second_rec_coords.append(second_rec_coords[5])
    second_rec_coords.append(second_rec_coords[4])
    second_rec_coords.append(second_rec_coords[2])
    second_rec_exterior_coords = [second_rec_coords[1], second_rec_coords[5], second_rec_coords[4], second_rec_coords[2], second_rec_coords[1]]
    recommendations.append((Polygon(second_rec_coords), "parallelogram", True, Polygon(second_rec_exterior_coords)))
    return recommendations

# checks cases with parallelogram
def process_quadrilateral(shape):
    recommendations = list()
    original_coords = list(shape.exterior.coords)
    side1_length = ((original_coords[1][1] - original_coords[0][1])**2 + (original_coords[1][0] - original_coords[0][0])**2)**0.5
    side2_length = ((original_coords[2][1] - original_coords[1][1])**2 + (original_coords[2][0] - original_coords[1][0])**2)**0.5
    side3_length = ((original_coords[3][1] - original_coords[2][1])**2 + (original_coords[3][0] - original_coords[2][0])**2)**0.5
    side4_length = ((original_coords[4][1] - original_coords[3][1])**2 + (original_coords[4][0] - original_coords[3][0])**2)**0.5
    if side1_length == side3_length and side2_length == side4_length:
        recommendations.append((shape, "parallelogram", False, shape))
        return recommendations
    # test concavity 
    is_convex, convex_indexes =  __is_convex(shape)
    if is_convex:
        # first recommendation: flip around convex quad to make a hexagon
        # first step is to find the side with the largest length
        max_length = max(side1_length, side2_length, side3_length, side4_length)
        # rotate coordinates to get the longest side between the 
        # zeroth and first coordinates
        if max_length == side1_length:
            rotations = 0
        elif max_length == side2_length:
            rotations = 1
        elif max_length == side3_length:
            rotations = 2
        else:
            rotations = 3
        first_rec_coords = list(original_coords)
        for x in range(0, rotations):
            del first_rec_coords[0]
            first_rec_coords.append(first_rec_coords[0])
        # setup of the second recommendation coordinates
        second_rec_coords = list(first_rec_coords)
        # here we start reflecting and adding coordinates to 
        # create the hexagon
        second_to_first_vertex_len_x = first_rec_coords[1][0] - first_rec_coords[2][0]
        second_to_first_vertex_len_y = first_rec_coords[1][1] - first_rec_coords[2][1]
        third_to_second_vertex_len_x = first_rec_coords[2][0] - first_rec_coords[3][0]
        third_to_second_vertex_len_y = first_rec_coords[2][1] - first_rec_coords[3][1]
        first_rec_coords.append((first_rec_coords[4][0] + second_to_first_vertex_len_x, first_rec_coords[4][1] + second_to_first_vertex_len_y))
        first_rec_coords.append((first_rec_coords[5][0] + third_to_second_vertex_len_x, first_rec_coords[5][1] + third_to_second_vertex_len_y))
        first_rec_coords.append(first_rec_coords[1])
        # creating exterior of the first recommendation
        first_rec_exterior_coords = list()
        first_rec_exterior_coords.append(first_rec_coords[0])
        first_rec_exterior_coords.append(first_rec_coords[3])
        first_rec_exterior_coords.append(first_rec_coords[2])
        first_rec_exterior_coords.append(first_rec_coords[1])
        first_rec_exterior_coords.append(first_rec_coords[6])
        first_rec_exterior_coords.append(first_rec_coords[5])
        first_rec_exterior_coords.append(first_rec_coords[0])
        recommendations.append((Polygon(first_rec_coords), "hexagon", True, Polygon(first_rec_exterior_coords)))
        # second recommendation, only if the quad's shorter sides are next to each other and if the exterior parallelogram can
        # be created without an extraneous lines coming out of the shape
        side2_length = ((second_rec_coords[2][1] - second_rec_coords[1][1])**2 + (second_rec_coords[2][0] - second_rec_coords[1][0])**2)**0.5
        side3_length = ((second_rec_coords[3][1] - second_rec_coords[2][1])**2 + (second_rec_coords[3][0] - second_rec_coords[2][0])**2)**0.5
        side4_length = ((second_rec_coords[4][1] - second_rec_coords[3][1])**2 + (second_rec_coords[4][0] - second_rec_coords[3][0])**2)**0.5
        second_max_length = max(side2_length, side3_length, side4_length) 
        # calculation of slopes with check to prevent divide by zero error
        try:
            slope_1 = (second_rec_coords[1][1] - second_rec_coords[0][1]) / (second_rec_coords[1][0] - second_rec_coords[0][0])
        except ZeroDivisionError:
            print('cannot divide by zero')
            slope_1 = (second_rec_coords[1][1] - second_rec_coords[0][1]) / 0.01
        try:
            slope_2 = (second_rec_coords[2][1] - second_rec_coords[1][1]) / (second_rec_coords[2][0] - second_rec_coords[1][0])
        except ZeroDivisionError:
            print('cannot divide by zero')
            slope_2 = (second_rec_coords[2][1] - second_rec_coords[1][1]) / 0.01
        try:
            slope_3 = (second_rec_coords[3][1] - second_rec_coords[2][1]) / (second_rec_coords[3][0] - second_rec_coords[2][0])
        except ZeroDivisionError:
            print('cannot divide by zero')
            slope_3 = (second_rec_coords[3][1] - second_rec_coords[2][1]) / 0.01
        try:
            slope_4 = (second_rec_coords[4][1] - second_rec_coords[3][1]) / (second_rec_coords[4][0] - second_rec_coords[3][0])
        except ZeroDivisionError:
            print('cannot divide by zero')
            slope_4 = (second_rec_coords[4][1] - second_rec_coords[3][1]) / 0.01
        slope_list = [slope_1, slope_2, slope_3, slope_4]
        for i in range (0, len(slope_list)):
            print('coord ', i, ': ', second_rec_coords[i])
            print('slope ', i, ': ', slope_list[i])
        slope_list.sort()
        # check to make sure slope difference is large enough for slopes 1 and 3
        slope_threshold = 0.1
        if second_max_length == side2_length:
            # check to make sure slope difference is large enough for slopes 2 and 4
            print('side 2 second max length')
            if True:
                second_rec_coords.append((second_rec_coords[0][0] - second_to_first_vertex_len_x, second_rec_coords[0][1] - second_to_first_vertex_len_y))
                second_rec_coords.append(second_rec_coords[2])
                second_rec_coords.append(second_rec_coords[3])
                second_rec_exterior_coords = list()
                second_rec_exterior_coords.append(second_rec_coords[0])
                second_rec_exterior_coords.append(second_rec_coords[1])
                second_rec_exterior_coords.append(second_rec_coords[2])
                second_rec_exterior_coords.append(second_rec_coords[5])
                second_rec_exterior_coords.append(second_rec_coords[0])
                recommendations.append((Polygon(second_rec_coords), "parallelogram", True, Polygon(second_rec_exterior_coords)))
        elif second_max_length == side4_length:
            # check to make sure slope difference is large enough for slopes 2 and 4
            print('side 4 second max length')
            if True:
                zeroth_to_first_vertex_len_x = second_rec_coords[1][0] - second_rec_coords[0][0]
                zeroth_to_first_vertex_len_y = second_rec_coords[1][1] - second_rec_coords[0][1]
                second_rec_coords.append(second_rec_coords[3])
                second_rec_coords.append((second_rec_coords[3][0] + zeroth_to_first_vertex_len_x, second_rec_coords[3][1] + zeroth_to_first_vertex_len_y))
                second_rec_coords.append(second_rec_coords[1])
                second_rec_exterior_coords = list()
                second_rec_exterior_coords.append(second_rec_coords[0])
                second_rec_exterior_coords.append(second_rec_coords[1])
                second_rec_exterior_coords.append(second_rec_coords[6])
                second_rec_exterior_coords.append(second_rec_coords[5])
                second_rec_exterior_coords.append(second_rec_coords[0])
                recommendations.append((Polygon(second_rec_coords), "parallelogram", True, Polygon(second_rec_exterior_coords)))
        return recommendations
    else:
        # the given shape is a concave quad
        convex_index = convex_indexes[0]
        # place convex index at vertex 1
        if convex_index == 0:
            original_coords.insert(0, original_coords[3])
            del original_coords[len(original_coords) - 1]
        elif convex_index > 1:
            while (convex_index > 1):
                del original_coords[0]
                original_coords.append(original_coords[0])
                convex_index -= 1
        second_to_third_vertex_len_x = original_coords[3][0] - original_coords[2][0]
        second_to_third_vertex_len_y = original_coords[3][1] - original_coords[2][1]
        third_to_zeroth_vertex_len_x = original_coords[0][0] - original_coords[3][0]
        third_to_zeroth_vertex_len_y = original_coords[0][1] - original_coords[3][1]
        first_to_second_vertex_len_x = original_coords[2][0] - original_coords[1][0]
        first_to_second_vertex_len_y = original_coords[2][1] - original_coords[1][1]
        first_to_zeroth_vertex_len_x = original_coords[0][0] - original_coords[1][0]
        first_to_zeroth_vertex_len_y = original_coords[0][1] - original_coords[1][1]
        # first recommendation: creates parallelogram wrapper around concave quadrilateral
        first_rec_coords = list(original_coords)
        first_rec_coords.append(first_rec_coords[1])
        first_rec_coords.append(first_rec_coords[2])
        first_rec_coords.append((first_rec_coords[6][0] + third_to_zeroth_vertex_len_x,  first_rec_coords[6][1] + third_to_zeroth_vertex_len_y))
        first_rec_coords.append((first_rec_coords[7][0] + second_to_third_vertex_len_x,  first_rec_coords[7][1] + second_to_third_vertex_len_y))
        first_rec_exterior_coords = [first_rec_coords[0], first_rec_coords[3], first_rec_coords[6], first_rec_coords[7], first_rec_coords[0]]
        recommendations.append((Polygon(first_rec_coords), "parallelogram", True, Polygon(first_rec_exterior_coords)))
        # second recommendation: creates parallelogram by duplicating concave quadrilateral then
        # flipping it on the concave side
        second_rec_coords = list(first_rec_coords)
        second_rec_coords.append((second_rec_coords[0][0] + first_to_second_vertex_len_x, second_rec_coords[0][1] + first_to_second_vertex_len_y))
        second_rec_coords.append(second_rec_coords[2])
        second_rec_coords.append(second_rec_coords[1])
        second_rec_coords.append(second_rec_coords[0])
        second_rec_exterior_coords = first_rec_exterior_coords
        recommendations.append((Polygon(second_rec_coords), "parallelogram", True, Polygon(second_rec_exterior_coords)))
        # third recommendation: creates parallelogram by duplicating concave quadrilateral then
        # flipping across the third vertex, then bounding it with an exterior parallelogram
        third_rec_coords = list(original_coords)
        third_rec_coords.append(third_rec_coords[3])
        third_rec_coords.append((third_rec_coords[3][0] - third_to_zeroth_vertex_len_x, third_rec_coords[3][1] - third_to_zeroth_vertex_len_y))
        third_rec_coords.append((third_rec_coords[6][0] + first_to_zeroth_vertex_len_x, third_rec_coords[6][1] + first_to_zeroth_vertex_len_y))
        third_rec_coords.append((third_rec_coords[7][0] - first_to_second_vertex_len_x, third_rec_coords[7][1] - first_to_second_vertex_len_y))
        third_rec_coords.append(third_rec_coords[3])
        third_rec_coords.append(third_rec_coords[0])
        third_rec_coords.append(third_rec_coords[2])
        third_rec_coords.append(third_rec_coords[6])
        third_rec_coords.append(third_rec_coords[8])
        third_rec_coords.append(third_rec_coords[0])
        third_rec_exterior_coords = [third_rec_coords[0], third_rec_coords[2], third_rec_coords[6], third_rec_coords[8], third_rec_coords[0]]
        recommendations.append((Polygon(third_rec_coords), "parallelogram", True, Polygon(third_rec_exterior_coords)))
        return recommendations

def process_universal(shape):
    recommendations = list()
    original_coords = list(shape.exterior.coords)
    # first recommendation: create a bounding parallelogram box around the hexagon
    # first we need to find the extreme points of the hexagon
    min_x = original_coords[0][0]
    min_y = original_coords[0][1]
    max_x = original_coords[0][0]
    max_x_y_coord = original_coords[0][1]
    max_y = original_coords[0][1]
    for i in range(1, len(original_coords)):
        if original_coords[i][0] < min_x:
            min_x = original_coords[i][0]
        if original_coords[i][0] > max_x:
            max_x = original_coords[i][0]
            max_x_y_coord = original_coords[i][1]
        if original_coords[i][1] < min_y:
            min_y = original_coords[i][1]
        if original_coords[i][1] > max_y:
            max_y = original_coords[i][1]
    # next we utilize these points to create the bounding parallelogram
    first_rec_coords = list(original_coords)
    # rotate the coordinates in the list such that the first one has a min_x value
    min_x_found = False
    while not min_x_found:
        if first_rec_coords[0][0] == min_x:
            min_x_found = True
        else:
            del first_rec_coords[0]
            first_rec_coords.append(first_rec_coords[0])
    # set up second recommendation coordinates with the minimum x value
    # coordinate at the front of the list
    second_rec_coords = list(first_rec_coords)
    print('coord list: ', second_rec_coords)
    # appending the exterior box to the list
    first_rec_coords.append((min_x, min_y))
    first_rec_coords.append((min_x, max_y))
    first_rec_coords.append((max_x, max_y))
    first_rec_coords.append((max_x, min_y))
    first_rec_coords.append((min_x, min_y))
    # making the exterior box
    first_rec_exterior_coords = []
    first_rec_exterior_coords.append((min_x, min_y))
    first_rec_exterior_coords.append((min_x, max_y))
    first_rec_exterior_coords.append((max_x, max_y))
    first_rec_exterior_coords.append((max_x, min_y))
    first_rec_exterior_coords.append((min_x, min_y))
    recommendations.append((Polygon(first_rec_coords), "parallelogram", True, Polygon(first_rec_exterior_coords)))
    # second recommendation: reflect shape across the y-axis to the left, then wrap with a parallelogram exterior
    for i in range(0, len(original_coords) - 1):
        x_increment = second_rec_coords[i][0] - second_rec_coords[i + 1][0]
        y_increment = second_rec_coords[i + 1][1] - second_rec_coords[i][1]
        second_rec_coords.append((second_rec_coords[len(second_rec_coords) - 1][0] + x_increment, second_rec_coords[len(second_rec_coords) - 1][1] + y_increment))
    # appending the second recommendation exterior, first we need to find the new
    # minimum x value by utilizing the center_x value 
    center_x = second_rec_coords[0][0]
    x_total_length = 2 * (max_x - center_x)
    min_x = max_x - x_total_length
    # traverse to the edge of the object before appending the exterior
    # on the right side
    coord_index = 1
    max_x_found = False
    while not max_x_found:
        if first_rec_coords[coord_index][0] == max_x:
            max_x_found = True
        else:
            second_rec_coords.append(second_rec_coords[coord_index])
            coord_index += 1
    second_rec_coords.append(second_rec_coords[coord_index])
    # start appending exterior to the coordinate list
    second_rec_coords.append((max_x, max_y))
    second_rec_coords.append((min_x, max_y))
    second_rec_coords.append((min_x, min_y))
    second_rec_coords.append((max_x, min_y))
    second_rec_coords.append((max_x, max_y))
    # connecting polygon back to the center point (due to shapely polygon always appending the last point)
    # loop through the original shape to get to the specified max_x coord
    second_rec_coords.append((max_x, max_x_y_coord))
    max_x_found = False
    max_x_index = 0
    while not max_x_found:
        if second_rec_coords[max_x_index][0] == max_x and second_rec_coords[max_x_index][1] == max_x_y_coord:
            max_x_found = True
        else:
            max_x_index += 1
    # appending back to the central point
    max_x_index_offset = 1
    while second_rec_coords[max_x_index + max_x_index_offset][0] != center_x:
        second_rec_coords.append(second_rec_coords[max_x_index + max_x_index_offset])
        max_x_index_offset += 1
    # making the exterior box
    second_rec_exterior_coords = []
    second_rec_exterior_coords.append((max_x, max_y))
    second_rec_exterior_coords.append((min_x, max_y))
    second_rec_exterior_coords.append((min_x, min_y))
    second_rec_exterior_coords.append((max_x, min_y))
    second_rec_exterior_coords.append((max_x, max_y))
    recommendations.append((Polygon(second_rec_coords), "parallelogram", True, Polygon(second_rec_exterior_coords)))
    return recommendations

'''private helper functions'''
def __num_sides(shape):
    return len(shape.exterior.coords) - 1

def __is_regular(shape):
    coords = shape.exterior.coords
    points = []
    for c in coords:
        points.append(Point(c[0], c[1]))
    starting_edge_length = points[0].distance(points[1])
    for i in range(1, len(points) - 1):
        current_edge_length = points[i].distance(points[i + 1])
        if (round(current_edge_length, 2) != round(starting_edge_length, 2)):
            return False
    return True

def __is_convex(shape):
    coords = list(shape.exterior.coords)
    positive_z_coords = list()
    negative_z_coords = list()
    # starting z component coord calculation
    if __compute_z_cross_product(coords[len(coords) - 2], coords[0], coords[1]) >= 0:
        positive_z_coords.append(0)
    else:   
        negative_z_coords.append(0)
    # rest of the z component coord calculation
    for i in range(1, len(coords) - 1):
        if __compute_z_cross_product(coords[i - 1], coords[i], coords[i + 1]) >= 0:
            positive_z_coords.append(i)
        else:   
            negative_z_coords.append(i)
    if len(positive_z_coords) > 0 and len(negative_z_coords) > 0:
        # the shape is concave
        if len(positive_z_coords) > len(negative_z_coords):
            return False, negative_z_coords
        else:
            return False, positive_z_coords
    else:
        # the shape is convex
        return True, list()
            
def __compute_z_cross_product(first_coord, second_coord, third_coord):
    dx1 = second_coord[0] - first_coord[0]
    dy1 = second_coord[1] - first_coord[1]
    dx2 = third_coord[0] - second_coord[0]
    dy2 = third_coord[1] - second_coord[1]
    return dx1 * dy2 - dy1 * dx2
