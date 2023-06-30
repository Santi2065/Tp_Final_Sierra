from tpf_Montana_teams import Team
import math
from tpf_Montana_essential_functions import check_hiker_in_summit


def spiral(team: Team) -> None:
    """
    Estrategia basada en los principios del espiral de Arquimedes.
    Argumento de entrada:
        team (Team): Clase que controla los escaladores de un equipo.  
    """
    c = team.comms # Accede a las comunicaciones con el servidor.
    data = c.get_data() # Contiene los datos de todos los jugadores.

    names = list(data[team.nombre].values())
    hikers = team.hikers

    # Se dirige al origen
    team.all_go_to_point((0, 0))

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

        determine_next_thetas(hikers_thetas, b)

        # Usando el nuevo theta, calcula el proximo punto
        for hiker, offset in zip(hikers, offsets):

            next_theta = hikers_thetas[hiker.nombre]

            # Formula del espiral es r = a + b * theta, a = 0
            next_radius = b * (next_theta - offset) 
            next_loc = get_point(next_radius, next_theta)

            hiker.go_to(next_loc)


        team.move_all_spiral()

        # Se fija si hay un escalador (de cualquier equipo) que llego a la cima
        summit_loc = check_hiker_in_summit(c)
        if summit_loc:
            team.all_go_to_point(summit_loc, True)
            print('Todos estamos en la cima :)')
            all_in_summit = True

        i += 1


def get_point(radio: float, theta: float) -> tuple[float, float]:
    """
    Calcula una coordenada (x,y) basados en el radio y angulo donde el escalador esta parado.

    Argumentos de entrada:
        radio (flotante): Distancia desde el origen
        theta (flotante): Angulo (en radianes)
    Salida:
        Tupla: coordenadas (x,y).  
    """

    # Formula matematica para obtener las coordenadas.
    x = radio * math.cos(theta)
    y = radio * math.sin(theta)
    return (x, y)

def integral(theta: float, b: float) -> float:
    """
    Primitiva de la formula general para calcular arcos.

    Argumentos de entrada:
        theta (flotante): Angulo actual.
        b (flotante): Constante del espiral (separacion / 2pi)
    Salida:
        Flotante: El resultado de la primitiva evaluado en theta.
    """
    return (b * (math.log(abs(math.sqrt(theta**2 + 1) + theta)) + theta*math.sqrt(theta**2 + 1)))/2

def estimate_theta2(theta1: float, b: float, distance: float) -> float:
    """
    Estima el theta2 tal que la distancia entre theta1 y theta2 ronde la distancia dada, la
    formula de la distancia es F(theta2) - F(theta1) = distancia
    
    Argumentos de entrada:
        theta1 (flotante): El theta actual en el espiral
        b (flotante): Constante del espiral (separacion / 2pi)
        distance (flotante): Distancia a recorrer desde theta1 a theta2 sobre el espiral\n
    Salida:
        Flotante: el theta2 obtenido al recorrer la distancia desde el theta1
    """
    theta2 = theta1
    change = 0.1

    # Margen de error al estimar el theta
    lower, higher = distance - 0.05, distance + 0.05
    integral1 = integral(theta1, b)

    # Representa la mejor distancia conseguida sin pasarse del valor maximo del margen
    distance1 = 0

    if higher > integral(theta2 + change, b) - integral1 > lower:
        return theta2 + change

    # Corre mientras el valor de theta2 no este en el margen de error para la distancia
    while not (higher > distance1 > lower):
        distance2 = integral(theta2 + change, b) - integral1

        if distance2 < lower or higher > distance2 > lower:
            distance1 = distance2
            theta2 += change
        elif distance2 > higher:
            change /= 2

    return theta2

def determine_next_thetas(hikers_thetas: dict[str, float], b: float) -> None:
    """
    Calcula la diferencia de theta1 y theta2 para recorrer una distancia por
    el espiral y se lo aplica a todos los escaladores, modifica el diccionario.

    Argumentos de entrada:
        hikers_thetas (diccionario): Theta actual de cada escalador {'nombre1': float, ...}
        b (flotante): Constante de espiral (separacion / 2pi)
    """

    # Distancia a recorrer por el espiral desde el theta actual
    distance = 49.8

    # El escalador con menor theta es el del espiral sin offset.
    theta1 = min(hikers_thetas.values())
    theta2 = estimate_theta2(theta1, b, distance)

    delta_theta = theta2 - theta1

    for hiker_name in hikers_thetas:
        hikers_thetas[hiker_name] += delta_theta


# Testeos
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