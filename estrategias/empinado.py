from teams import Team
from HIKERS import Hiker
import math

def empinado(team:Team[Hiker]):

    hikers_buscando = team.hikers

    #Etapa de separacion
    team.face_out()
    team.separacion(1000)

    #comienzo de estrategia
    searching = True
    info = team.comms.get_data()
    for hiker in team.hikers:

        direction = pendiente_max(info)

        hiker.change_direction(direction)
        hiker.cambio_estado('subiendo')

    while searching:
        
        info = team.comms.get_data()

        for hiker in team.hikers:

            inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x']
            inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']

            direccion_x = math.cos(hiker.ordenes['direction'])
            direccion_y = math.sin(hiker.ordenes['direction'])

            producto_punto = inclinacion_x * direccion_x + inclinacion_y * direccion_y
            
            if hiker.estado == 'subiendo':

                if  producto_punto > 0:
                    #el arcotangente al cuadrado de (inclinacion_y, inclinacion_x) me devuelve el angulo en radianes de la direccion donde se maximiza la pendiente.
                    direction = pendiente_max(info)
                    hiker.change_direction(direction)

                else:

                    if info[team.nombre][hiker.nombre]['cima'] == False:
                        # Si el escalador llega a un pico donde cima es False, baja de la montaña
                        hiker.cambio_estado('bajando')

            elif hiker.estado == 'bajando':

                if  producto_punto >= 0:

                    # Si el escalador ha terminado de bajar
                    hiker.cambio_estado('subiendo')

            if hiker.in_summit():

                hiker.stay_still()
                hiker.cambio_estado('quieto')

                hikers_buscando.remove(hiker)

                flag = (info[team.nombre][hiker.nombre]['x'],info[team.nombre][hiker.nombre]['y'])

        team.move_all()

    team.all_go_to_point(flag)
    
    def pendiente_max(info:dict):
        
        inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x']
        inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']
        
        direccion_x = math.cos(hiker.ordenes['direction'])
        direccion_y = math.sin(hiker.ordenes['direction'])
        
        return math.atan2(inclinacion_y, inclinacion_x)