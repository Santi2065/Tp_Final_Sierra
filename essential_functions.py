import math

def difference(p1: tuple|list, p2: tuple|list) -> tuple:
    # returns the x y coords of the vector going from p2 to p1, ignores z value
    return (p1[0] - p2[0], p1[1] - p2[1])
def dot_product(v1: tuple|list, v2: tuple|list) -> float:
    return v1[0] * v2[0] + v1[1] * v2[1]
def magnitude(v: tuple[float, float]) -> float:
    return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))