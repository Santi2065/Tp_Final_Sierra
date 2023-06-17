from communication.client.client import MountainClient
from test_hiker import Hiker, Grafico_2d_equipo
from essential_functions import magnitude, dot_product, difference
import time
import math

def register(names: list[str]):
    print('Conectando a servidor...')
    #c = MountainClient("10.42.0.1", 8888)
    c = MountainClient()
    c.add_team('Los cracks', names)
    c.finish_registration()
    return c

def all_go_to_point(hikers: list[Hiker], c: MountainClient, point: tuple[float, float], graf: Grafico_2d_equipo) -> None:
    # Makes all hikers to go to the desired point
    directives = {}
    close_to_point = {hiker.nombre: magnitude(difference(hiker.actual_pos(), point)) < 30 for hiker in hikers}
    i = 0
    while False in close_to_point.values():
        for hiker in hikers:
            if i % 50 == 0 and i >= 100000:
                graf.coordenadas()
            print(f'{hiker.nombre}: x={hiker.actual_pos()[0]:8.1f}, y={hiker.actual_pos()[1]:8.1f} yendo a {point}')

            if close_to_point[hiker.nombre]:
                hiker.change_direction(0)
                hiker.change_speed(0)
                directives[hiker.nombre] = hiker.ordenes
                continue

            distance = magnitude(difference(hiker.actual_pos(), point))
            hiker.change_direction(hiker.go_to(point))
            hiker.change_speed(hiker.step_to_point(point))
            directives[hiker.nombre] = hiker.ordenes
            close_to_point[hiker.nombre] = distance < 30 or hiker.in_summit()

        c.next_iteration('Los cracks', directives)
        i += 1
    return True

def spiral():
    names = ['Santi', 'Joaco', 'Gian ', 'Pipe ']
    c = register(names)

    directives = {name: {'speed': 50, 'direction': 0} for name in names}
    hikers = [Hiker(directives[name], name) for name in names]
    graf = Grafico_2d_equipo(hikers)

    # Se dirige al origen
    all_go_to_point(hikers, c, (0, 0), graf)

    print('llegue')

    # Angulos iniciales para que queden separados uniformemente
    offsets = [(2*math.pi / len(names)) * i for i in range(len(names))]

    for hiker, offset in zip(hikers, offsets):
        directives[hiker.nombre] = {'speed': 5, 'direction': offset}

    graf.coordenadas()

    c.next_iteration('Los cracks', directives)
    #time.sleep(.04)'

    separation = 100 * len(names)
    b = separation / (2 * math.pi)
    hikers_thetas = {hiker.nombre: offset for hiker, offset in zip(hikers, offsets)}
    found_summit = False

    i = 0
    # Comienza el proceso de ir en espiral
    while not found_summit:
        #  cada cuanto     desde donde
        #      v                v
        if i % 100 == 0 and i >= 100000:
            graf.coordenadas()

        for hiker, offset in zip(hikers, offsets):
            x, y = hiker.actual_pos()[0], hiker.actual_pos()[1]
            current_loc = (x, y)
            current_theta = hikers_thetas[hiker.nombre]

            if hiker.in_summit():
                print(f'{hiker.nombre}: Estoy en cima')
                summit_loc, found_summit = current_loc, True
                break

            next_theta = estimate_theta2(current_theta, b)        
            hikers_thetas[hiker.nombre] = next_theta
            next_radius = b * (next_theta - offset)
            next_loc = get_point(next_radius, next_theta)

            direction = get_direction(current_loc, next_loc)
            #direction = hiker.go_to(next_loc)
            hiker.change_speed(hiker.step_to_point(next_loc))
            hiker.change_direction(direction)
            directives[hiker.nombre] = hiker.ordenes

            print(f'{hiker.nombre}: x={x:8.1f} y={y:8.2f} θ1={current_theta:.3f} θ2={next_theta:.3f} Δθ:{next_theta-current_theta:.18f} rev:{current_theta/(2*math.pi):.2f} dir:{directives[hiker.nombre]["direction"]:5.2f} sp:{directives[hiker.nombre]["speed"]:.3f}')

        if found_summit:
            all_go_to_point(hikers, c, summit_loc, graf)
        i += 1
        c.next_iteration('Los cracks', directives)
        time.sleep(0.05)
        if c.is_over():
            break



def get_direction(current_loc: tuple, next_loc: tuple) -> float:
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
    if loc[0] == 0:
        return math.pi/2 if loc[1] > 0 else (3*math.pi)/2
    return math.atan2(loc[1], loc[0])

def get_point(radius: float, theta: float) -> tuple[float, float]:
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return (x, y)

def integral(theta: float, b: float):
    return (b * (math.log(abs(math.sqrt(theta**2 + 1) + theta)) + theta*math.sqrt(theta**2 + 1)))/2

def estimate_theta2(theta1: float, b: float) -> float:
    theta2 = theta1
    change = 0.1
    lower, higher = 49.5, 50.5
    distance1 = 0

    if higher > integral(theta2 + change, b) - integral(theta1, b) > lower:
        return theta2 + change

    while not (higher > distance1 > lower):
        distance2 = integral(theta2 + change, b) - integral(theta1, b)
        #print(f'distance1: {distance1}, distance2: {distance2}, theta2:{theta2}, change:{change}')
        if distance2 < lower or higher > distance2 > lower:
            distance1 = distance2
            theta2 += change
        elif distance2 > higher:
            change /= 2
            #print(f'cambie change: {change}')

    return theta2


def test_gets():
    def test_get_point():
        print(f'get_point(10, pi/2):  {get_point(10, math.pi/2)}')
        print(f'get_point(10, pi):    {get_point(10, math.pi)}')
        print(f'get_point(10, 3pi/2): {get_point(10, 3*math.pi/2)}')
        print(f'get_point(10, 2pi):   {get_point(10, 2*math.pi)}')
        print(f'get_point(10, 5pi/2): {get_point(10, 5*math.pi/2)}')
        print(f'get_point(10, -pi/2): {get_point(10, -math.pi/2)}')
        print(f'get_point(10, -pi): {get_point(10, -math.pi)}')
        print(f'get_point(10, 0): {get_point(10, 0)}')
    test_get_point()


#test_gets()
if __name__ == '__main__':
    #print(estimate_theta2(61.54999999999904, 100/(2*math.pi)))
    spiral()
'''

hikers = []
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))

while not c.is_over():

    print(hikers[2].actual_pos())
    c.next_iteration('Los cracks', {h.nombre: h.ordenes for h in hikers})
    if hikers[0].almost_out() is True:
        hikers[0].random()
    if hikers[1].almost_out() is True:
        hikers[1].random()
    if hikers[2].almost_out() is True:
        hikers[2].random()
    if hikers[3].almost_out() is True:
        hikers[3].random()

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