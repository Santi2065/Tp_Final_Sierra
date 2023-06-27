import math

def difference(vector1: tuple|list, vector2: tuple|list) -> tuple:
    """
    Calcula las coordenadas en R^2 del vector dezplazamiento entre dos vectores.

    Argumentos de entrada: 
        vector1 (tupla|lista): Coordenadas (x,y) del primer vector.
        vector2 (tupla|lista): Coordenadas (x,y) del segundo vector.

    Salida:
        Tupla: Coordenadas (x,y) del vector desplazamiento.
    """
    return (vector1[0] - vector2[0], vector1[1] - vector2[1])

def dot_product(vector1: tuple|list, vector2: tuple|list) -> float:
    """
    Calcula el producto interno entre dos vectores de R^2.

    Argumentos de entrada:
        vector1 (tupla|lista): Coordenadas (x,y) del primer vector.
        vector2 (tupla|lista): Coordenadas (x,y) del segundo vector.

    Salida:
        Flotante: Resultado del producto interno entre ambos vectores.
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def magnitude(vector: tuple[float, float]) -> float:
    """
    Calcula la magnitud de un vector de R^2.

    Argumento de entrada:
        vector (tupla): Coordenadas (x,y) del vector.

    Salida:
        Flotante: Magnitud del vector.
    """
    return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

def distance_between(vector1: tuple[float, float, float]|tuple[float, float], vector2: tuple[float, float, float]|tuple[float, float]) -> float:
    """
    Calcula la distancia entre dos vectores de R^2.
    
    Argumentos de entrada:
        vector1 (tupla): Coordenadas (x,y) del primer vector.
        vector2 (tupla): Coordenadas (x,y) del segundo vector.

    Salida:
        Flotante: Distancia entre el vector 1 y el vector 2.
    """
    v = difference(vector1, vector2)
    return magnitude(v)

def direction(coordenadas_iniciales: list|tuple[float, float], coordenadas_finales: list|tuple[float, float]) -> float:
    """
    Calcula el angulo necesario a seguir para ir de un punto inicial a un punto final.

    Argumentos de entrada:
        coordenadas_iniciales (tupla|lista): coordenadas (x,y) del punto de partida.
        coordenadas_finales (tupla|lista): coordenadas (x,y) del destino.

    Salida:
        Flotante: Angulo en radianes (-pi, pi] necesario para ir del punto de partida al destino.
    """
    distancia_x, distancia_y = difference(coordenadas_finales, coordenadas_iniciales)
    return math.atan2(distancia_y, distancia_x)


def altura_maxima(equipo:str, diccionario: dict, lista_max: list) -> float: 
    """
    Calcula la altura maxima alcanzada por un equipo. 
    
    Argumentos de entrada:
        equipo (cadena): Nombre del equipo.
        diccionario (diccionario): Diccionario con los datos de todos los jugadores.
        lista_max (lista): Almacena las alturas maximas por iteracion del equipo.

    Salida:
        Flotante: Altura maxima global alcanzada por el equipo.
    """

    lista_auxiliar = [] # Almacena momentaneamente todas las alturas del equipo.

    for i in diccionario[equipo]:
        lista_auxiliar.append(diccionario[equipo][i]['z'])

    maximo = max(lista_auxiliar) # Busca el valor maximo de la iteracion actual
    lista_max.append(maximo) # Almacena todos los maximos de cada iteracion.

    return (max(lista_max)) # devuelve el maximo global

def altura_promedio(diccionario:dict,equipo:str) -> float:
    """
    Calcula la altura promedio de todos los jugadores de un equipo por iteracion.
     
    Argumentos de salida:
        diccionario (diccionario) : Diccionario con los datos de todos los jugadores.
        equipo (cadena) : Nombre del equipo.

    Salida:
        Flotante: Altura promedio local alcanzada por el equipo redondeada a dos decimales.
    """
    lista_altura = [] # Almacena momeneamente las alturas de todos los integrantes del equipo.

    for x in diccionario[equipo]:
        lista_altura.append(diccionario[equipo][x]['z'])

    promedio = sum(lista_altura) / len(lista_altura) # Calcula la altura promedio.

    return round(promedio,2) 

