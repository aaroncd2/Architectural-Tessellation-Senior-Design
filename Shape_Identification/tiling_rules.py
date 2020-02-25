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
    if (__is_regular(shape)):
        # process to tessellation engine
        return shape
    else:
        number_sides = __num_sides(shape)
        if (number_sides == 3):
            return process_triangle(shape)
        elif (number_sides == 4):
            return process_quadrilateral(shape)
        else:
            pass

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
        # return the convex quad for now
        recommendations.append((shape, "convex_quad", False, shape))
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
