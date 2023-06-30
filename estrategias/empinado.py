from teams import Team
from hikers import Hiker
import math

def empinado(team:Team):
    """
    Algortimo que busca constantemente escalar la montania hasta encontrar el maximo global.
    
    Artributo:
        team (Team): equipo donde se implementara el algoritmo.
    """


    #Etapa de separacion 
    team.separacion(100) # los escaladores se dan la espalda y se alejan 1000 pasos entre ellos.

    #comienzo de estrategia

    searching = True 
    info = team.comms.get_data() # diccionario con todos los datos.

    for hiker in team.hikers: # Los escaladores apuntan a la penidente creciente mas cercana.

        hiker.change_direction(pendiente_max(hiker, info))
        hiker.cambio_estado('subiendo') # estan subiendo.

    while searching:
        
        info = team.comms.get_data() 

        for hiker in team.hikers:

            inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x'] # guardo la pendiente de cada escalador.
            inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']

            direccion_x = math.cos(hiker.ordenes['direction']) 
            direccion_y = math.sin(hiker.ordenes['direction'])
            # descompongo la direccion en una direccion de x , y mediante trigonometria.

            producto_punto = inclinacion_x * direccion_x + inclinacion_y * direccion_y # Indica si esta subiendo o bajando.
            
            if hiker.estado == 'subiendo': 

                if  producto_punto > 0: # esta subiendo.

                    #el arcotangente al cuadrado de (inclinacion_y, inclinacion_x) me devuelve el angulo en radianes de la direccion donde se maximiza la pendiente.
                    hiker.change_direction(pendiente_max(hiker,info)) # cambio la direccion del escalador a la pendiente maxima

                else: # llego a un pico.

                    if info[team.nombre][hiker.nombre]['cima'] == False: # verifico si no esta la bandera.

                        # Si el escalador llega a un pico donde cima es False, baja de la montaña.
                        hiker.cambio_estado('bajando')

            elif hiker.estado == 'bajando': 

                if  producto_punto >= 0: 

                    # Si el escalador ha terminado de bajar.
                    hiker.cambio_estado('subiendo')

            if hiker.in_summit(): # alcanzo la cima.

                hiker.cambio_estado('quieto')

                flag = (info[team.nombre][hiker.nombre]['x'],info[team.nombre][hiker.nombre]['y'])
                # Guardo la ubicacion (x,y,z) de la bandera,
                searching = False

        team.move_all() # Todos avanzan.

    team.all_go_to_point(flag) # Todos van hacia la bandera.
    # Hasta que no termine, caminan hasta el pico
    while not team.comms.is_over():
        info = team.comms.get_data()
        for hiker in team.hikers:
            hiker.change_direction(pendiente_max(hiker, info)) # cambio la direccion del escalador a la pendiente maxima
        team.move_all()


            
    
def pendiente_max(hiker:Hiker,info:dict) -> float:
    """
    Indica en que direccion se encuentra la pendiente maxima que el escalador puede alcanzar.
    
    
    Argumentos de entrada: 
        hiker (Hiker): Escalador donde se buscara la inclinacion maxima mas cercana.
        info(diccionario): Diccionario con los datos de todos los jugadores.

    Salida:
        Flotante: direccion donde se encunetra la pendiente maxima mas cercana.
    """
    
    inclinacion_x = info[hiker.equipo][hiker.nombre]['inclinacion_x']
    inclinacion_y = info[hiker.equipo][hiker.nombre]['inclinacion_y']
    

    return math.atan2(inclinacion_y, inclinacion_x)