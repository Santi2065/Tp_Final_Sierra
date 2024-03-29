from communication.client.client import MountainClient
from tpf_Montana_hikers import Hiker
import math, time
from tpf_Montana_essential_functions import distance_between, check_hiker_in_summit

class Team(Hiker):

    """
    La clase realiza operaciones que tienen como finalidad controlar todos los aspectos e integrantes de un equipo.

    Atributos:
        nombre (cadena): Nombre del equipo.
        hikers (lista): Lista con los escaladores del equipo.
        comms (MountainClient): Cliente del servidor.
    
    Metodos:
        face_out(): Ordena a los escaladores darse la espalda entre ellos.
        move_all(): Dirige a los escaladores hacia la direccion ordenada por la estrategia implementada.
        move_all_spiral(): Dirige a los escaladores hacia la direccion ordenada por la estrategia implementada solo si esta fue actualizada.
        all_go_to_point(): Direcciona a todos los integrantes del equipo hacia una poscicion especifica.
        separacion(): Los escaladores adoptan una poscion dandose la espalda entre ellos y se mueven una cantidad de pasos especifica.
    """

    def __init__(self, nombre: str, hikers: list[Hiker], c: MountainClient) -> None:
        self.nombre = nombre # Del equipo
        self.hikers = hikers
        self.comms = c # accede a las comunicaciones con el servidor

    def face_out(self)-> None:
        """
        Los escaladores adoptan una poscicion de espaldas unos a otros.
        """

        direction = 0 # Todos mirando hacia la misma direccion
        for hiker in self.hikers:
            hiker.change_direction(direction)
            direction += math.pi/2 # Separacion de pi/2 entre cada hiker. Logra que todos se den la espalda.

    def move_all(self) -> None:
        """
        Dirige a los escaladores hacia la direccion ordenada por la estrategia implementada.
        """

        directives = {hiker.nombre: hiker.ordenes for hiker in self.hikers} # Almacena la direccion y velocidad de cada escalador.
        self.comms.next_iteration(self.nombre, directives) # Manda al servidor las nuevas ordenes de los escaladores

        for hiker in self.hikers: # previene que el hiker no se vaya del mapa
            if hiker.almost_out(): 
                hiker.random()

    def move_all_spiral(self) -> None:
        """
        Dirige a los escaladores hacia la direccion ordenada por la estrategia implementada solo si esta fue actualizada.
        """
        prev_data = self.comms.get_data() # Diccionario con la informacion de todos los jugadores del server previo a la iteracion

        directives = {hiker.nombre: hiker.ordenes for hiker in self.hikers} # Ordenes de los jugadores
        self.comms.next_iteration(self.nombre, directives) # Manda las nuevas ordenes al servidor

        while prev_data == self.comms.get_data(): # Mientras no se haya actualizado las ordenes, espera.
            time.sleep(0.01)

        for hiker in self.hikers: # Previene que el hiker no se vaya del mapa.
            if hiker.almost_out():
                hiker.random()

    def all_go_to_point(self, punto: tuple[float, float], going_to_summit=False) -> None:
        """
        Hace que todos los escaladores vayan al punto dado

        Argumento de entrada:
            punto (tupla): Coordenadas (x,y) del vector destino.
        """
        close_to_point = {}

        # Hace un diccionario que dice si el escalador esta cerca del punto o no
        for hiker in self.hikers:
            distance_to_point = distance_between(hiker.actual_pos(), punto)
            close_to_point[hiker.nombre] = distance_to_point < 0.005 or hiker.in_summit()

        # Corre hasta que todos los escaladores esten cerca del punto
        while False in close_to_point.values():
            for hiker in self.hikers:
                summit_loc = check_hiker_in_summit(self.comms)
                if summit_loc and not going_to_summit:
                    self.all_go_to_point(summit_loc, True)
                    break
                distance_to_point = distance_between(hiker.actual_pos(), punto)
                close_to_point[hiker.nombre] = distance_to_point < 0.005 or hiker.in_summit()

                if close_to_point[hiker.nombre]:
                    hiker.ordenes = {'direction': 0, 'speed': 1}
                    continue

                hiker.go_to(punto)
               

            self.move_all()


    def separacion(self,pasos:int):
        """
        Los escaladores adoptan una poscion dandose la espalda entre ellos y se mueven una cantidad de pasos especifica.

        Argumento de entrada:
            paso (entero): la cantidad de pasos que los escaladores se moveran.
        """

        self.face_out()
        hikers_buscando = self.hikers # Lista con todos los hikers
        for i in range(pasos):
            self.move_all()
            for hiker in hikers_buscando:
                if hiker.in_summit():  # Mientras que los escaladores se mueven, verifica si pasan por la cima.

                    hiker.stay_still()
                    hiker.cambio_estado('quieto') # Llegue a la cima, me quedo aca.

                    hikers_buscando.remove(hiker) # El hiker que llego, no esta buscando mas.
                    info = self.comms.get_data() # Busco las coordenadas de la cima.
                    flag = (info[self.nombre][hiker.nombre]['x'],info[self.nombre][hiker.nombre]['y']) # Guarda (x,y) de la cima.

                    self.all_go_to_point(flag, True) # Dirige al resto de escaladores hacia la cima.
                    break
                # Si sale del loop anterior con un break, hace otro break si no continue
            else:
                continue
            break