from communication.client.client import MountainClient
from HIKERS import Hiker
from test_hiker import Grafico_2d_equipo
from essential_functions import magnitude, dot_product, difference, distance_between
import matplotlib.pyplot as plt
import time
import math

#TODO Hacer q no pase esto: 
#TODO WARNING: 2023-06-21 16:21:33,173 - The competition is not in the waiting_for_directions state. Current state: moving

def spiral():
    # Define y registra en el servidor el equipo
    names = ['Santi', 'Joaco', 'Gian', 'Pipe']
    c = register(names)

    hikers = [Hiker(name, c) for name in names]

    coords = {hiker.nombre: {'x': [], 'y': [], 'z': []} for hiker in hikers}
    update_coords(coords, hikers)
    graf = Grafico_2d_equipo(coords)

    # Se dirige al origen
    all_go_to_point(hikers, c, (0, 0), graf, coords)

    ##print('llegue')

    # Angulos iniciales para que queden separados uniformemente
    offsets = [(2*math.pi / len(names)) * i for i in range(len(names))]

    # Theta de cada escalador, va creciendo a medida que pasa el tiempo
    hikers_thetas = {hiker.nombre: offset for hiker, offset in zip(hikers, offsets)}

    directives = {}
    separation = (2 * 50) * len(names)
    b = separation / (2 * math.pi)
    all_in_summit = False

    iteration_time = []

    i = 0
    # Comienza el proceso de ir en espiral
    while not c.is_over():
        #*s = time.time()
        #  cada cuanto    desde cual iteracion
        #      v               v
        if i % 20 == 0 and i >= 0:
            #*start = time.time()
            graf.coordenadas2()
            #*print(f'graf: {time.time() - start}-------------------------------------------------------')

        if i % 400 == 0 and i >= 10000000:
            graf.heat_map()

        previous_hikers_thetas = hikers_thetas.copy()
        determine_next_thetas(hikers_thetas, b)

        #TODO: convertir este for en una funcion, ademas poner si uno llego al borde
        for hiker, offset in zip(hikers, offsets):
            current_theta = previous_hikers_thetas[hiker.nombre]

            next_theta = hikers_thetas[hiker.nombre]
            next_radius = b * (next_theta - offset)
            next_loc = get_point(next_radius, next_theta)

            hiker.go_to(next_loc)

            directives[hiker.nombre] = hiker.ordenes

            #print(f'{hiker.nombre:6s}: x={x:8.1f} y={y:8.1f} θ1={current_theta:6.2f} θ2={next_theta:6.2f} Δθ:{next_theta-current_theta:11.9f} rev:{current_theta/(2*math.pi):.2f} dir:{directives[hiker.nombre]["direction"]:5.2f} sp:{directives[hiker.nombre]["speed"]:.3f}')
            ##print(f'{hiker.nombre:6s}: θ1={current_theta:6.2f} θ2={next_theta:6.2f} Δθ:{next_theta-current_theta:11.9f} rev:{min(hikers_thetas.values())/(2*math.pi):.2f} dir:{directives[hiker.nombre]["direction"]:5.2f} sp:{directives[hiker.nombre]["speed"]:.3f}')


        
        #*iteration_time += [time.time() - s]
        #*print(f'Iteracion entera: {sum(iteration_time)/len(iteration_time)}')

        previous_coords = all_hiker_coords(c, 'Los cracks')

        c.next_iteration('Los cracks', directives)

        # Espera hasta que el servidor haya actualizado las posiciones
        while previous_coords == all_hiker_coords(c, 'Los cracks'):
            continue


        # Se fija si hay un escalador (de cualquier equipo) que llego a la cima
        summit_loc = check_hiker_in_summit(c)
        if summit_loc:
            all_go_to_point(hikers, c, summit_loc, graf, coords)
            all_in_summit = True

        update_coords(coords, hikers)


        i += 1

    ##print('Todos estamos en la cima :)')



def register(names: list[str]) -> MountainClient:
    ##print('Conectando a servidor...')
    #c = MountainClient("10.42.0.1", 8888)
    c = MountainClient()
    c.add_team('Los cracks', names)
    c.finish_registration()
    while c.is_registering_teams():
        continue
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
            graf.coordenadas2()

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

            ##print(f'{hiker.nombre}: x={hiker.actual_pos()[0]:8.1f}, y={hiker.actual_pos()[1]:8.1f} yendo a {point}, dir:{directives[hiker.nombre]["direction"]}')

        c.next_iteration('Los cracks', directives)
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
    '''Calcula la diferencia de theta1 y theta2 para recorrer una
    distancia por el espiral y se lo aplica a todos los escaladores'''
    distance = 49.8

    # El escalador con menor theta es el del espiral sin offset.
    theta1 = min(hikers_thetas.values())
    theta2 = estimate_theta2(theta1, b, distance)

    delta_theta = theta2 - theta1

    for hiker_name in hikers_thetas:
        hikers_thetas[hiker_name] += delta_theta

def spiral_move_all(c: MountainClient, directives: dict[str, float]):
    '''Mueve todos los escaladores'''
    previous_coords = all_hiker_coords(c, 'Los cracks')
    c.next_iteration('Los cracks', directives)

    # Espera hasta que el servidor haya actualizado las posiciones
    while previous_coords == all_hiker_coords(c, 'Los cracks'):
        continue

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

def check_hiker_in_summit(c: MountainClient) -> tuple|None:
    '''Checks if any hiker of any team reached the summit, if there is it returns its location'''
    info = c.get_data()
    for team in info.values():
        for hiker_data in team.values():
            if hiker_data['cima']:
                x = hiker_data['x']
                y = hiker_data['y']
                return (x, y)


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


if __name__ == '__main__':
    spiral()
