from teams import Team
from HIKERS import Hiker
import math
import random

def empinado(team:Team):
    team.go_center()
    team.face_out()
    for i in range(50):
        team.move_all()
    searching = True
    info = team.comms.get_data()
    for hiker in team.hikers:
        x = info[team.nombre][hiker.nombre]['x']
        y = info[team.nombre][hiker.nombre]['y']
        inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x']
        inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']
        direction = math.atan2(inclinacion_y, inclinacion_x)
        hiker.change_direction(direction)
        hiker.cambio_estado('subiendo')
    while searching:
        info = team.comms.get_data()
        for hiker in team.hikers:
            x = info[team.nombre][hiker.nombre]['x']
            y = info[team.nombre][hiker.nombre]['y']
            inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x']
            inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']
            direccion_x = math.cos(hiker.ordenes['direction'])
            direccion_y = math.sin(hiker.ordenes['direction'])
            producto_punto = inclinacion_x * direccion_x + inclinacion_y * direccion_y
            if hiker.estado == 'subiendo':
                if  producto_punto <= 0:
                    direction = math.atan2(inclinacion_y, inclinacion_x)
                    hiker.change_direction(direction)
                    if info[team.nombre][hiker.nombre]['cima'] == False:
                        # Si el escalador llega a un pico donde cima es False, baja de la montaña
                        hiker.cambio_estado('bajando')
                else:
                    direction = math.atan2(inclinacion_y, inclinacion_x)
                    hiker.change_direction(direction)
            elif hiker.estado == 'bajando':
                if  producto_punto >= 0:
                    # Si el escalador ha terminado de bajar
                    hiker.cambio_estado('subiendo')
            if hiker.cima():
                searching = False
        team.move_all()
        for hiker in team.hikers:
            print(hiker.estado)
