import math
contador_racha = 0
contador_racha_malo = 0
anterior_top1 = None
anterior_ultimo = None





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

def leaderboard(diccionario:dict): # El original anda (Leaderboard.py)
    ''' prints a sorted table with the highest player per team '''
    jugador_max = None # Chequear si cambian de algo
    altura_max = None
    lista= []
    aux_racha = []
    top_1 = None
    corto_racha = False


    for equipo, jugadores in diccionario.items():
        jugador_max,altura_max= max(jugadores.items(),key=lambda item:item[1]['z'])
        lista.append([jugador_max,altura_max['z'],equipo]) # [nombre,z,equipo]

    ordenar_lista = sorted(lista,key=lambda x:-x[1]) # De mas alto a mas chico, puse el '-' pq si no me la ordenaba al reves
    
    top_1 = ordenar_lista[0][0]
    top_ultimo = ordenar_lista[len(lista)-1][0] # ojo que si la lista tiene cero elemento puede llegar a tirar error?


    if anterior_top1 == None or anterior_top1 == top_1:
        contador_racha += 1
    else:
        contador_racha = 0

    if anterior_ultimo == None or anterior_ultimo == top_ultimo:
        contador_racha_malo += 1
    else:
        contador_racha_malo = 0
    
    anterior_top1 = top_1 

    for i in range(len(ordenar_lista)):
        if contador_racha > 10 and i == 0:
            print(f"Top {'{:<5}'.format(i+1)}🔥|{'{:20}'.format(ordenar_lista[i][2])}|{'{:20}'.format(ordenar_lista[i][0])}|{round(ordenar_lista[i][1],3)} ")
        elif contador_racha_malo > 10 and ordenar_lista[i][0] == top_ultimo and i!=0 :
            print(f"Top {'{:<5}'.format(i+1)}🐢|{'{:20}'.format(ordenar_lista[i][2])}|{'{:20}'.format(ordenar_lista[i][0])}|{round(ordenar_lista[i][1],3)}")
        else:
            print(f"Top {'{:<5}'.format(i+1)}{chr(32)} |{'{:20}'.format(ordenar_lista[i][2])}|{'{:20}'.format(ordenar_lista[i][0])}|{round(ordenar_lista[i][1],3)}")

    lista.clear() # limpia listas para no interferir con las nuevas listas

def altura_maxima(equipo:list, diccionario:dict): 
    """ Prints the highest z reached by the inserted team. """
    lista_aux = [] # va a guardar las alturas por iteracion de cada integrante del equipo
    lista_max = [] # Va guardando todos los picos maximos por iteracion

    for i in diccionario[equipo]:
        lista_aux.append(diccionario[equipo][i]['z'])

    maximo = max(lista_aux)
    lista_max.append(maximo)

    lista_aux.clear()
    return (max(lista_max)) # santi no llores
    