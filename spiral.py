from communication.client.client import MountainClient
from HIKERS import Hiker
from test_hiker import Grafico_2d_equipo
from essential_functions import magnitude, dot_product, difference, distance_between
import matplotlib.pyplot as plt
import time
import math


def spiral():
    # Define y registra en el servidor el equipo
    names = ['Santi', 'Joaco', 'Gian ', 'Pipe ']
    c = register(names)

    hikers = [Hiker(name, c) for name in names]

    coords = {hiker.nombre: {'x': [], 'y': [], 'z': []} for hiker in hikers}
    update_coords(coords, hikers)
    graf = Grafico_2d_equipo(hikers)

    # Se dirige al origen
    all_go_to_point(hikers, c, (0, 0), graf, coords)

    print('llegue')

    # Angulos iniciales para que queden separados uniformemente
    offsets = [(2*math.pi / len(names)) * i for i in range(len(names))]

    # Theta de cada escalador, va creciendo a medida que pasa el tiempo
    hikers_thetas = {hiker.nombre: offset for hiker, offset in zip(hikers, offsets)}

    directives = {}
    separation = (2 * 50) * len(names)
    b = separation / (2 * math.pi)
    found_summit = False

    iteration_time = []

    i = 0
    # Comienza el proceso de ir en espiral
    while not found_summit:
        s = time.time()
        #  cada cuanto    desde cual iteracion
        #      v               v
        if i % 1 == 0 and i >= 0:
            start = time.time()
            graf.coordenadas2(coords)
            print(f'graf: {time.time() - start} -------------------------------------------')

        previous_hikers_thetas = hikers_thetas.copy()
        determine_next_thetas(hikers_thetas, b)

        #TODO convertir este for en una funcion, ademas poner si uno llego al borde
        for hiker, offset in zip(hikers, offsets):
            # If it is in the summit, all hikers go to the coord of the hiker in the summit
            if hiker.in_summit():
                print(f'{hiker.nombre}: Estoy en cima')
                x, y, z = hiker.actual_pos()
                summit_loc, found_summit = (x, y), True
                break

            current_theta = previous_hikers_thetas[hiker.nombre]

            next_theta = hikers_thetas[hiker.nombre]
            next_radius = b * (next_theta - offset)
            next_loc = get_point(next_radius, next_theta)

            hiker.go_to(next_loc)

            directives[hiker.nombre] = hiker.ordenes


            #print(f'{hiker.nombre:6s}: x={x:8.1f} y={y:8.1f} θ1={current_theta:.3f} θ2={next_theta:.3f} Δθ:{next_theta-current_theta:11.9f} rev:{current_theta/(2*math.pi):.2f} dir:{directives[hiker.nombre]["direction"]:5.2f} sp:{directives[hiker.nombre]["speed"]:.3f}')
            print(f'{hiker.nombre:6s}: θ1={current_theta:.3f} θ2={next_theta:.3f} Δθ:{next_theta-current_theta:11.9f} rev:{current_theta/(2*math.pi):.2f} dir:{directives[hiker.nombre]["direction"]:5.2f} sp:{directives[hiker.nombre]["speed"]:.3f}')

        if found_summit:
            all_go_to_point(hikers, c, summit_loc, graf, coords)

        i += 1
        c.next_iteration('Los cracks', directives)
        time.sleep(0.1)

        update_coords(coords, hikers)

        #TODO: fijarse si es posible conocer los minutos, sino hacer q se fije si despues 
        #TODO: de la iteracion todas las posiciones son iguales
        if c.is_over():
            break

        iteration_time += [time.time() - s]
        print(f'Iteracion entera: {sum(iteration_time)/len(iteration_time)}')

    print('Todos estamos en la cima :)')

'''
Optimizacion

con el grafico corriendo:
    grafico: 0.135s
        check_summit: 0.002 s, por cada escalador (0.008)
        go_to original: 0.003 s, por escalador (0.012)
        go_to mejorado: 0.0015 s, por cada escalador (0.006)
        total calculo para 1: 0.005s
    iteracion entera: ~0.18 (0.28 menos el time.sleep(0.1), ademas empeora con el tiempo)

sin el grafico corriendo:
        check_summit: 0.0013 s, por cada escalador (0.0052)
        go_to mejorado: 0.0013 s, por cada escalador (0.0052)
    for entero: 0.0036
    iteracion entera: 0.032 (0.132 menos el time.sleep(0.1))

conclusion: mejorar performace grafico y conocer minutos para eliminar time.sleep
'''


def register(names: list[str]) -> MountainClient:
    print('Conectando a servidor...')
    #c = MountainClient("10.42.0.1", 8888)
    c = MountainClient()
    c.add_team('Los cracks', names)
    c.finish_registration()
    return c

def all_go_to_point(hikers: list[Hiker], c: MountainClient, point: tuple[float, float], graf: Grafico_2d_equipo, coords: dict[str, dict[str, list[float]]]) -> None:
    # Makes all hikers to go to the desired point
    directives, close_to_point = {}, {}

    # Makes a dictionary that tells if hiker is near the point or not
    for hiker in hikers:
        distance_to_point = distance_between(hiker.actual_pos(), point)
        close_to_point[hiker.nombre] = distance_to_point == 0 or hiker.in_summit()
    i = 0

    # Runs until all hikers are near the point
    while False in close_to_point.values():
        if i % 1 == 0 and i >= 0:
            graf.coordenadas2(coords)

        for hiker in hikers:
            if close_to_point[hiker.nombre]:
                hiker.change_direction(0)
                hiker.change_speed(0)
                directives[hiker.nombre] = hiker.ordenes
                continue

            distance_to_point = distance_between(hiker.actual_pos(), point)

            hiker.go_to(point)

            directives[hiker.nombre] = hiker.ordenes
            close_to_point[hiker.nombre] = distance_to_point == 0 or hiker.in_summit()

            print(f'{hiker.nombre}: x={hiker.actual_pos()[0]:8.1f}, y={hiker.actual_pos()[1]:8.1f} yendo a {point}, dir:{directives[hiker.nombre]["direction"]}')

        c.next_iteration('Los cracks', directives)
        
        time.sleep(0.05)
        update_coords(coords, hikers)
        
        i += 1

def get_point(radius: float, theta: float) -> tuple[float, float]:
    '''Returns x y coords given theta and radius'''
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return (x, y)

def integral(theta: float, b: float):
    return (b * (math.log(abs(math.sqrt(theta**2 + 1) + theta)) + theta*math.sqrt(theta**2 + 1)))/2

def estimate_theta2(theta1: float, b: float, distance: float) -> float:
    '''Dado un theta inicial, constante b y distancia a recorrer estima el theta2 tal que
    la distancia entre theta1 y theta2 ronde la distancia dada'''
    theta2 = theta1
    change = 0.1
    lower, higher = distance - 0.05, distance + 0.05
    integral1 = integral(theta1, b)
    distance1 = 0

    if higher > integral(theta2 + change, b) - integral1 > lower:
        return theta2 + change

    while not (higher > distance1 > lower):
        distance2 = integral(theta2 + change, b) - integral1
        #print(f'distance1: {distance1}, distance2: {distance2}, theta2:{theta2}, change:{change}')

        if distance2 < lower or higher > distance2 > lower:
            distance1 = distance2
            theta2 += change
        elif distance2 > higher:
            change /= 2

    return theta2

def update_coords(coords: dict[str, dict[str, list[float]]], hikers: list[Hiker]) -> None:
    '''Actualiza la historia de coordenadas de todos los escaladores de un equipo'''
    for hiker in hikers:
        x, y, z = hiker.actual_pos()
        coords[hiker.nombre]['x'] += [x]
        coords[hiker.nombre]['y'] += [y]
        coords[hiker.nombre]['z'] += [z]

def update_coords2(coords: dict[str, dict[str, list[float]]], c: MountainClient) -> None:
    '''Actualiza la historia de coordenadas de todos los escaladores de un
    equipo, pero usa un get_data en vez de la cantidad de escaladores'''
    team_name = 'Los cracks'
    hikers_locs = all_hiker_coords(c, team_name)

    for name in hikers_locs:
        x, y, z = hikers_locs[name]
        coords[name]['x'] += [x]
        coords[name]['y'] += [y]
        coords[name]['z'] += [z]

def determine_next_thetas(hikers_thetas: dict[str, float], b: float) -> None:

    distance = 49.8

    # El escalador con menor theta es el del espiral sin offset.
    theta1 = min(hikers_thetas.values())
    theta2 = estimate_theta2(theta1, b, distance)

    delta_theta = theta2 - theta1

    for hiker_name in hikers_thetas:
        hikers_thetas[hiker_name] += delta_theta

def spiral_move_all():
    pass

def all_hiker_coords(c: MountainClient, team_name: str):
    '''Devuelve diccionario con la posicion de todos los escaladores, un get_data'''
    team_info = c.get_data()[team_name]
    hiker_coords = {}
    for name in team_info:
        x = team_info[name]['x']
        y = team_info[name]['y']
        z = team_info[name]['z']
        hiker_coords[name] = (x, y, z)
    return hiker_coords

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