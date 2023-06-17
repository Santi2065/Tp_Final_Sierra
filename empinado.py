from teams import Team
from HIKERS import Hiker
import math

def empinado(team:Team):
    #team.go_center()
    team.face_out()
    team.move_all()
    cima = False
    while not cima:
        info = team.comms.get_data()
        for hiker in team.hikers:
            inclinacion_x = info[team.nombre][hiker.nombre]['inclinacion_x']
            inclinacion_y = info[team.nombre][hiker.nombre]['inclinacion_y']
            direction = math.atan2(inclinacion_y, inclinacion_x)
            hiker.change_direction(direction)
        team.move_all()
        for hiker in team.hikers:
            if hiker.cima():
                cima = True
