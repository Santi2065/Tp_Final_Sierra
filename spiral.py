from communication.client.client import MountainClient
import math
#TODO: hacer que vayan todos al centro (0,0)

def spiral():
    c = MountainClient()
    #team = ['Santi', 'Pipe', 'Gian', 'Joaco']
    #team = ['Santi']
    c.add_team('Los cracks', ['Santi'])
    c.finish_registration()
    teams = c.get_data()

    separation = 100 #* len(team)
    b = separation / (2 * math.pi)
    #offsets = [(2*math.pi/len(team)) * i for i in range(team)]
    offsets = [0]
    directives = {}

    for climber, offset in zip(teams['Los cracks'], offsets):
        directives[climber] = {'direction': offset, 'speed': 50}
    c.next_iteration('Los cracks', directives)

    while True:
        for team in teams:
            for climber, offset in zip(teams[team], offsets):
                x, y = teams[team][climber]['x'], teams[team][climber]['y']
                current_loc = (x, y)
                current_theta = get_theta(current_loc)

                next_theta = current_theta + (50 / separation)
                next_radius = b * (next_theta - offset)
                next_loc = get_point(next_radius, next_theta)

                direction = get_direction(current_loc, next_loc)
                directives[climber] = {'direction': direction, 'speed': 50}

            while not c.next_iteration(team, directives):
                continue
        if c.is_over():
            break


def get_direction(current_loc: tuple, next_loc: tuple) -> float:
    def difference(p1: tuple, p2: tuple) -> tuple:
        return (p1[0] - p2[0], p1[1] - p2[1])
    def dot_product(v1: tuple, v2: tuple) -> float:
        return v1[0] * v2[0] + v1[1] * v2[1]
    def magnitude(v: tuple) -> float:
        return math.sqrt(v[0]**2 + v[1]**2)
    x1, x2 = current_loc[0], next_loc[0]
    y1, y2 = current_loc[1], next_loc[1]
    aux = (x2, y1)
    v1, v2 = difference(current_loc, aux), difference(current_loc, next_loc)
    theta = math.acos(dot_product(v1, v2) / (magnitude(v1) * magnitude(v2)))
    if x1 > x2:
        if y1 < y2:
            return math.pi - theta
        else:
            return math.pi + theta
    else:
        if y1 < y2:
            return theta
        else:
            return -theta

def get_theta(loc: tuple | list) -> float:
    return math.atan(loc[1] / loc[0])

def get_point(radius: float, theta: float) -> tuple:
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return (x, y)


spiral()
'''
directives = {
        'Pipe':{'direction':10,'speed':20},
        'Santi':{'direction':10,'speed':20},
        'Joaco':{'direction':10,'speed':20},
        'Gian':{'direction':10,'speed':20}
        }
c.next_iteration('Los cracks', directives)

{'Los cracks': {
    'Santi': {
        'x': 3125.632983169462,
        'y': 6949.486402873517,
        'z': 4897.121164511321,
        'inclinacion_x': -41.52367048233283,
        'inclinacion_y': -44.173850342687714,
        'cima': False},
    'Pipe': {
        'x': 3125.632983169462,
        'y': 6949.486402873517,
        'z': 4897.121164511321,
        'inclinacion_x': -41.52367048233283,
        'inclinacion_y': -44.173850342687714,
        'cima': False},
    'Gian': {
        'x': 3125.632983169462,
        'y': 6949.486402873517,
        'z': 4897.121164511321,
        'inclinacion_x': -41.52367048233283,
        'inclinacion_y': -44.173850342687714,
        'cima': False},
    'Joaco': {
        'x': 3125.632983169462,
        'y': 6949.486402873517,
        'z': 4897.121164511321,
        'inclinacion_x': -41.52367048233283,
        'inclinacion_y': -44.173850342687714,
        'cima': False}}}
'''