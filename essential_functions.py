import math

def difference(p1: tuple|list, p2: tuple|list) -> tuple:
    '''returns the x y coords of the vector going from p2 to p1, ignores z value'''
    return (p1[0] - p2[0], p1[1] - p2[1])

def dot_product(v1: tuple|list, v2: tuple|list) -> float:
    '''returns the dot product of v1 and v2, ignores z value'''
    return v1[0] * v2[0] + v1[1] * v2[1]

def magnitude(v: tuple[float, float]) -> float:
    '''returns the magnitude of the vector, ignores z value'''
    return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

def distance_between(p1: tuple[float, float], p2: tuple[float,float]) -> float:
    '''returns the distance between p1 and p2, ignores z value'''
    v = difference(p1, p2)
    return magnitude(v)

def direction(hiker_coord: list|tuple[float, float], objective: list|tuple[float, float]) -> float:
    '''returns the angle in radians (-pi, pi] for hiker to go in direction to objetive'''
    dx, dy = difference(objective, hiker_coord)
    return math.atan2(dy, dx)