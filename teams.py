from communication.client.client import MountainClient
from HIKERS import Hiker
import math

class Team(Hiker):
    def __init__(self,nombre:str,hikers:list,c:MountainClient) -> None:
        self.nombre = nombre
        self.hikers = hikers
        self.comms = c

    def face_out(self):
        direction=0
        for hiker in self.hikers:
            hiker.change_direction(direction)
            direction += math.pi/2

    def move_all(self) -> None:
        self.comms.next_iteration(self.nombre, {h.nombre: h.ordenes for h in self.hikers})
        for hiker in self.hikers:
            if hiker.almost_out():
                hiker.random()

    def go_center(self):
        #apuntan al centro
        for hiker in self.hikers:
            hiker.go_to([0,0])

        #se mueven hasta que llegan
        llegada = {x : 0 for x in self.hikers}
        no_llegaron = True
        while no_llegaron:
            self.move_all()
            info = self.comms.get_data()
            for hiker in self.hikers:
                x =  info[self.nombre][hiker.nombre]['x']
                y =  info[self.nombre][hiker.nombre]['y']
                if -1 < x < 1 and -1 < y < 1:
                    llegada[hiker] = 1
                    hiker.stay_still()
            no_llegaron = False
            for x in llegada.values():
                if x == 0:
                    no_llegaron = True
        print("En el centro")