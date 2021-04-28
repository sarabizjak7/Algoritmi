import numpy as np
from shapely.geometry import Point, Polygon, MultiPoint, LineString
from shapely.ops import triangulate
from matplotlib import pyplot
from descartes.patch import PolygonPatch
from scipy.spatial import Delaunay
import shapely.wkt
import itertools 


def does_intersect(A, B, C, D):
    """
    Returns wether line segments with endpoint A, B and C, D intersect.
    Points are given as (x, y).
    """
    line1 = LineString([A, B])
    line2 = LineString([C, D])
    return line1.intersects(line2)


def orientation(A, B, C): 
    """
    Returns the orientation of the points A, B and C,
    where points are given as A = (x1, y2), B = (x2, y2) and C = (x3, y3).
    """
    
    cross_product = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1]) 

    if cross_product > 0:   
        return -1    # Clockwise orientation 
    elif cross_product < 0: 
        return 1    # Counterclockwise orientation 
    else:  
        return 0    # None -- points are colinear (not our case!)


def divide_into_upper_lower(S_x, S_y):
    """
    Divide the convex hull into upper and lower part

    Input:  list of x coords
            list of y coords

    Output: upper (zipped x and y)
            lower(zipped x and y)
    """

    # Find the indexes of the most left and most right point for S 
    S_mostleftpoint = S_x.index(min(S_x))
    S_mostrightpoint = S_x.index(max(S_x))

    # List of points in upper part
    # X
    upper_X = S_x[S_mostrightpoint:] + [S_x[S_mostleftpoint]]
    # Y
    upper_Y = S_y[S_mostrightpoint:] + [S_y[S_mostleftpoint]]

    # List of points in lower part
    # X
    lower_X = S_x[S_mostleftpoint:S_mostrightpoint + 1] 
    # Y
    lower_Y = S_y[S_mostleftpoint:S_mostrightpoint + 1]

    upper = list(zip(upper_X, upper_Y))
    lower = list(zip(lower_X, lower_Y))

    return upper, lower


def find_upper_hull(upper):
    """
    Returns the upper hull from upper path (points)
    """
    upper_hull = []
    for p in upper:
        while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], p) != 1:
            upper_hull.pop()
        upper_hull.append(p)
    return upper_hull


def find_lower_hull(lower):
    """
    Returns the lower hull from lower path (points)
    """
    lower_hull = []
    for p in lower:
        while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], p) != 1:
            lower_hull.pop()
        lower_hull.append(p)
    return lower_hull


def union(coords):
    """
    Returns the union of two convex hulls 
    """
    ###

    # First check if one hull contains the other:
    S1 = list(zip(coords[0], coords[1]))
    S2 = list(zip(coords[2], coords[3]))
    poly1 = Polygon(S1)
    poly2 = Polygon(S2)

    if poly1.contains(poly2):
        return S1
    
    if poly2.contains(poly1):
        return S2
    
    ###

    # Point coordinates
    S1_x = coords[0]
    S1_y = coords[1]
    S2_x = coords[2]
    S2_y = coords[3]

    # Divide S1 and S2 into upper and lower paths
    S1_upper, S1_lower = divide_into_upper_lower(S1_x, S1_y)
    S2_upper, S2_lower = divide_into_upper_lower(S2_x, S2_y)

    # Join S1 and S2 into upper and lower paths
    upper = S1_upper + S2_upper 
    lower = S1_lower + S2_lower

    upper.sort(reverse = True)
    lower.sort()

    # Make the upper and lower hulls
    upper_hull = find_upper_hull(upper)
    lower_hull = find_lower_hull(lower)

    convex_hull_union = lower_hull[:-1] + upper_hull[:-1]

    return convex_hull_union


def intersection(coords):
    """
    Reports wether two convex hulls intersect or not 
    """

    S1 = list(zip(coords[0], coords[1]))
    S2 = list(zip(coords[2], coords[3]))

    S1_segments = []
    S2_segments = []
    inter_list = []

    for i in range(len(S1) - 1):
        S1_segments.append([S1[i], S1[i + 1]])
    S1_segments.append([S1[len(S1) - 1], S1[0]])

    for i in range(len(S2) - 1):
        S2_segments.append([S2[i], S2[i + 1]])
    S2_segments.append([S2[len(S2) - 1], S2[0]])

    for segment1 in S1_segments:
        for segment2 in S2_segments:
            intersection = does_intersect(segment1[0], segment1[1], segment2[0], segment2[1])
            inter_list.append(intersection) 
    
    if True in inter_list:
        return True
    else:
        return False

##################################
############## MAIN ##############
##################################

# INPUT FILE:
text_file = "vhod2.txt"

with open(text_file, 'r') as f:
        data = f.readlines()
        coords = []
        for line in data:
            coord =  [float(x) for x in line.split()]
            coords.append(coord)

union = union(coords)
bool_intersect = intersection(coords)

union_X = []
union_Y = []
for element in union:
    union_X.append(element[0])
    union_Y.append(element[1])

print(*union_X)
print(*union_Y)
print(bool_intersect)