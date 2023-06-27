from communication.client.client import MountainClient
import essential_functions
from HIKERS import Hiker
import math, time

class Team(Hiker):
    def __init__(self, nombre: str, hikers: list[Hiker], c: MountainClient) -> None:
        self.nombre = nombre
        self.hikers = hikers
        self.comms = c

    def face_out(self):
        direction = 0
        for hiker in self.hikers:
            hiker.change_direction(direction)
            direction += math.pi/2

    def move_all(self) -> None:
        directives = {hiker.nombre: hiker.ordenes for hiker in self.hikers}
        self.comms.next_iteration(self.nombre, directives)

        for hiker in self.hikers:
            if hiker.almost_out():
                hiker.random()
    
    def move_all_spiral(self) -> None:
        prev_data = self.comms.get_data()

        directives = {hiker.nombre: hiker.ordenes for hiker in self.hikers}
        self.comms.next_iteration(self.nombre, directives)

        while prev_data == self.comms.get_data():
            time.sleep(0.01)

        for hiker in self.hikers:
            if hiker.almost_out():
                hiker.random()

    def go_center(self):
        #apuntan al centro
        for hiker in self.hikers:
            hiker.go_to([0, 0])

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
            no_llegaron = False          #! Raro, creo q va adentro del if
            for x in llegada.values():
                if x == 0:
                    no_llegaron = True
        #! Habria q poner un go_to por cada iteracion, o cambiar el margen de error,
        #! sino se puede pasar y seguir de largo
        print("En el centro")

    def all_go_to_point(self, point: tuple[float, float]) -> None:
        '''
        Hace que todos los escaladores vayan al punto dado

        Arguments:
        hikers: lista con los escaladores\n
        point: (x, y) o (x, y, z), ignora z
        '''
        close_to_point = {}

        # Hace un diccionario que dice si el escalador esta cerca del punto o no
        for hiker in self.hikers:
            distance_to_point = essential_functions.distance_between(hiker.actual_pos(), point)
            close_to_point[hiker.nombre] = distance_to_point < 0.05 or hiker.in_summit()
        i = 0

        # Corre hasta que todos los escaladores esten cerca del punto
        while False in close_to_point.values():
            #TODO hacer q use 1 o 2 get_data por iteracion (go_to2 tal vez)
            for hiker in self.hikers:
                distance_to_point = essential_functions.distance_between(hiker.actual_pos(), point)
                close_to_point[hiker.nombre] = distance_to_point < 0.05 or hiker.in_summit()

                if close_to_point[hiker.nombre]:
                    hiker.stay_still()
                    continue

                hiker.go_to(point)
                #print(f'{hiker.nombre}: x={hiker.actual_pos()[0]:8.1f}, y={hiker.actual_pos()[1]:8.1f} yendo a {point}')

            self.move_all()

            #*i += 1