from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
from test_hiker import Grafico_2d_equipo
from essential_functions import magnitude, dot_product, difference, distance_between
import matplotlib.pyplot as plt
import time
import math

#TODO Hacer q no pase esto: 
#TODO WARNING: 2023-06-21 16:21:33,173 - The competition is not in the waiting_for_directions state. Current state: moving

def spiral(team: Team):
    c = team.comms
    data = c.get_data()

    names = list(data[team.nombre].values())
    hikers = team.hikers

    # Se dirige al origen
    all_go_to_point(hikers, (0, 0), team)

    print('llegue a (0, 0)')

    # Angulos iniciales para que queden separados uniformemente
    offsets = [(2*math.pi / len(names)) * i for i in range(len(names))]

    # Theta de cada escalador, va creciendo a medida que pasa el tiempo
    hikers_thetas = {hiker.nombre: offset for hiker, offset in zip(hikers, offsets)}

    # Hace que entre cada nivel del espiral haya una separacion de 100
    separation = (50 * 2) * len(names)
    b = separation / (2 * math.pi)
    all_in_summit = False

    i = 0
    # Comienza el proceso de ir en espiral
    while not c.is_over():
        if all_in_summit:
            team.move_all()
            continue

        previous_hikers_thetas = hikers_thetas.copy()
        determine_next_thetas(hikers_thetas, b)

        #TODO: convertir este for en una funcion, ademas poner si uno llego al borde, tal vez poner go_to2
        for hiker, offset in zip(hikers, offsets):
            current_theta = previous_hikers_thetas[hiker.nombre]

            next_theta = hikers_thetas[hiker.nombre]
            # Formula del espiral es r = a + b * theta, a = 0
            next_radius = b * (next_theta - offset)
            next_loc = get_point(next_radius, next_theta)

            hiker.go_to(next_loc)

            #*print(f'{hiker.nombre:6s}: θ1={current_theta:6.2f} θ2={next_theta:6.2f} Δθ:{next_theta-current_theta:11.9f} rev:{min(hikers_thetas.values())/(2*math.pi):.2f} sp:{hiker.ordenes["speed"]:4.1f}')


        s = time.time()
        team.move_all_spiral()
        print(time.time() - s)

        # Se fija si hay un escalador (de cualquier equipo) que llego a la cima
        summit_loc = check_hiker_in_summit(c)
        if summit_loc:
            all_go_to_point(hikers, summit_loc, team)
            print('Todos estamos en la cima :)')
            all_in_summit = True

        i += 1

def all_go_to_point(hikers: list[Hiker], point: tuple[float, float], team: Team) -> None:
    '''
    Hace que todos los escaladores vayan al punto dado

    Arguments:
    hikers: lista con los escaladores\n
    point: (x, y) o (x, y, z), ignora z
    '''
    close_to_point = {}

    # Hace un diccionario que dice si el escalador esta cerca del punto o no
    for hiker in hikers:
        distance_to_point = distance_between(hiker.actual_pos(), point)
        close_to_point[hiker.nombre] = distance_to_point < 0.05 or hiker.in_summit()
    i = 0

    # Corre hasta que todos los escaladores esten cerca del punto
    while False in close_to_point.values():
        #TODO hacer q use 1 o 2 get_data por iteracion (go_to2 tal vez)
        for hiker in hikers:
            distance_to_point = distance_between(hiker.actual_pos(), point)
            close_to_point[hiker.nombre] = distance_to_point < 0.05 or hiker.in_summit()

            if close_to_point[hiker.nombre]:
                hiker.stay_still()
                continue

            hiker.go_to(point)
            #print(f'{hiker.nombre}: x={hiker.actual_pos()[0]:8.1f}, y={hiker.actual_pos()[1]:8.1f} yendo a {point}')

        team.move_all()
        
        #*i += 1

def get_point(radius: float, theta: float) -> tuple[float, float]:
    '''
    Devuelve coordenadas x y dado un theta y un radio
    '''
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return (x, y)

def integral(theta: float, b: float):
    '''
    Funcion usada para calcular la distancia, tal que\n
    F(theta2) - F(theta1) = distancia
    '''
    return (b * (math.log(abs(math.sqrt(theta**2 + 1) + theta)) + theta*math.sqrt(theta**2 + 1)))/2

def estimate_theta2(theta1: float, b: float, distance: float) -> float:
    '''
    Estima el theta2 tal que la distancia entre theta1 y theta2 ronde la distancia dada, la
    formula de la distancia es F(theta2) - F(theta1) = distancia\n
    Arguments:
    theta1: El theta actual en el espiral
    b: Constante del espiral (separacion / 2pi)
    distance: Distancia a recorrer desde theta1 a theta2 sobre el espiral\n
    Returns:
    theta2: el theta2 obtenido al recorrer la distancia desde el theta1
    '''
    theta2 = theta1
    change = 0.1
    # Margen de error al estimar el theta
    lower, higher = distance - 0.05, distance + 0.05
    integral1 = integral(theta1, b)

    # Representa la mejor distancia conseguida sin pasarse del valor maximo del margen
    distance1 = 0

    #! Fijarse si este if esta al pedo, tal vez distance1 tambien
    if higher > integral(theta2 + change, b) - integral1 > lower:
        return theta2 + change

    # Corre mientras el valor de theta2 no este en el margen de error para la distancia
    while not (higher > distance1 > lower):
        distance2 = integral(theta2 + change, b) - integral1
        #*print(f'distance1: {distance1}, distance2: {distance2}, theta2:{theta2}, change:{change}')

        if distance2 < lower or higher > distance2 > lower:
            distance1 = distance2
            theta2 += change
        elif distance2 > higher:
            change /= 2

    return theta2

def determine_next_thetas(hikers_thetas: dict[str, float], b: float) -> None:
    '''
    Calcula la diferencia de theta1 y theta2 para recorrer una
    distancia por el espiral y se lo aplica a todos los escaladores\n
    Arguments:
    hikers_thetas: theta actual de cada escalador {'nombre1': float, ...}
    b: constante de espiral (separacion / 2pi)
    '''
    # Distancia a recorrer por el espiral desde el theta actual
    distance = 49.8

    # El escalador con menor theta es el del espiral sin offset.
    theta1 = min(hikers_thetas.values())
    theta2 = estimate_theta2(theta1, b, distance)

    delta_theta = theta2 - theta1

    for hiker_name in hikers_thetas:
        hikers_thetas[hiker_name] += delta_theta

def check_hiker_in_summit(c: MountainClient) -> tuple|None:
    '''
    Chequea si hay un escalador (de cualquier equipo) en la cima, y si lo hay devuelve las coordenadas\n
    Returns: (x, y) o None si nadie esta en la cima
    '''
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


"""if __name__ == '__main__':
    names = ['Santi', 'Joaco', 'Gian', 'Pipe']
    team_name = 'Los cracks'
    c = MountainClient()

    hikers = [Hiker(name, team_name, c) for name in names]
    team = Team(team_name, hikers, c)
    register(names, team.nombre)

    spiral(team)"""
