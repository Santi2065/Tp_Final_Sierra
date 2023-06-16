from HIKERS import Hiker
import math

class Team:
    def __init__(self,nombre,hikers,c) -> None:
        self.nombre = nombre
        self.hikers = hikers
        self.comms = c

    def face_out(self):
        direction=0
        for hiker in self.hikers:
            hiker.change_direction(direction)
            direction += math.pi/2

    def move_all(self,hikers,c) -> None:
        self.comms.next_iteration(self.nombre, {h.nombre: h.ordenes for h in hikers})
        for hiker in hikers:
            if hiker.almost_out():
                hiker.random()