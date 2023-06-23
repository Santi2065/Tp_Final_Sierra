from teams import Team
from HIKERS import Hiker
import math
#from graph import Grafico_2d_equipo

def empinado(team:Team):

    hikers_buscando = team.hikers
    #team.go_center()
    team.face_out()

    for i in range(100):
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

                if  producto_punto > 0:

                    direction = math.atan2(inclinacion_y, inclinacion_x)
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

                flag = [info[team.nombre][hiker.nombre]['x'],info[team.nombre][hiker.nombre]['y']]
                searching = False

        team.move_all()

    for hiker in team.hikers:
        hiker.go_to(flag)

    
    while hikers_buscando:

        for hiker in hikers_buscando:

            if hiker.in_summit():
                hiker.stay_still()
                hiker.cambio_estado('quieto')
                hikers_buscando.remove(hiker)

            else:
                hiker.go_to(flag)

        team.move_all()

    print(f"fin {[h.in_summit() for h in team.hikers]}")


