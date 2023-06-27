from communication.client.client import MountainClient
import random
import math
from essential_functions import difference, magnitude, distance_between, direction
VELOCIDAD_MAX = 50

class Hiker:

    """
    La clase realiza operaciones que tienen como finalidad lograr un control absoluto del escalador.

    Atributos:
        nombre (cadena) = Nombre del escalador.
        ordenes (lista) = Direccion y velocidad del escalador.
        RADIO_MONTANIA (entero) = El radio de la montania.
        comss (MountainClient) = Cliente del servidor.
        estado (cadena) = Estado actual del escalador.
        equipo (cadena) = Equipo del cual forma parte el escalador.

    Metodos:
        actual_pos(): Devuelve la poscicion actual del escalador.
        cambio_estado(): Cambia el estado actual del escalador.
        almost_out(): Detecta posible salida del mapa del escalador.
        change_direction(): Modifica la direccion del escalador.
        go_to(): Dirige al escalador a unas coordenadas especificas.
        random(): El escalador se mueve por la montania de forma aleatoria.
        stay_still(): El escalador reduce su veolcidad a valores insignificativos.
        in_summit(): Comprueba si el escalador alcanzo la cima.
        step_to_point2(): Devuelve la distancia del paso para llegar a un punto.
    """


    def __init__(self, nombre: str, equipo: str, cliente: MountainClient, ordenes: list = [0,VELOCIDAD_MAX]):

        self.nombre = nombre
        self.ordenes = {'direction':ordenes[0],'speed':ordenes[1]}
        self.RADIO_MONTANIA = 23000
        self.comms = cliente
        self.estado = 'quieto'
        self.equipo = equipo 

    def actual_pos(self)->tuple:
        '''
        Calcula la poscion actual del escalador

        Salida:
            Tupla: coordenadas (x,y,z) actuales del escalador.
        '''

        dic = self.comms.get_data()
        x =  dic[self.equipo][self.nombre]['x'] # x actual
        y =  dic[self.equipo][self.nombre]['y'] # y actual
        z =  dic[self.equipo][self.nombre]['z'] # z actual

        return (x, y, z)
    
    def cambio_estado(self, nuevo_estado:str) -> None:
        """
        Cambia el estado del escalador.
        
        Argumentos de entrada:
            nuevo_estado (cadena): nuevo estado del escalador.
        """
        self.estado = nuevo_estado
    
    def almost_out(self)-> bool:
        """
        Detecta posible salida del mapa del escalador.
        
        Salida:
            Booleano: Verdadero si se ira del mapa en la siguiente iteracion. Falso en caso contrario.
        """

        info = self.actual_pos() # guarda la poscion actual del escalador.
        x = info[0]
        y = info[1]

        norma = magnitude((x, y)) # Norma del vector

        paso_previo = 22900 # Radio del circulo menos dos pasos. Conserva margen de error.

        if norma > paso_previo: # Si la norma es mayor al paso previo, se esta por ir del mapa.
            return True
        else:
            return False

    def change_direction(self, new_direction: float|int):
        # El escalador se dirige hacia la nueva direccion (radianes)
        self.ordenes['direction'] = new_direction #Provisional, para hacer pruebas.

    def change_speed(self, new_speed: float|int):
        # Cambia la velocidad en la que el escalador se mueve (max 50)
        self.ordenes['speed'] = new_speed

    def go_to(self, objective: list[float, float]) -> None:
        '''Cambia las ordenes para que apunte y vaya al objetuvo, si el objetivo esta
        dentro del rango entonces cambia la velociadad para que quede en el objetivo'''
        x, y, z = self.actual_pos()
        hiker_coords = (x, y)
        self.ordenes = {'direction': direction(hiker_coords, objective), 'speed': self.step_to_point2(hiker_coords, objective)}
        #!self.ordenes = {'direction': direction(hiker_coords, objective), 'speed': self.step_to_point(objective)}
        # return self.ordenes     <- podria agregar esto
    
    def go_to2(self, objective: list[float, float], loc: tuple[float, float, float]) -> None:
        '''Cambia las ordenes para que apunte y vaya al objetuvo, si el objetivo esta
        dentro del rango entonces cambia la velociadad para que quede en el objetivo, no usa actual_pos'''
        x, y, z = loc
        hiker_coords = (x, y)
        self.ordenes = {'direction': direction(hiker_coords, objective), 'speed': self.step_to_point2(hiker_coords, objective)}

    def random(self)-> None:
        """ El escalador entra en un estado de aleatoriedad y se dirige a coordenads aleatorias."""
    
        x_random = random.uniform(-2500, 2500)
        y_random = random.uniform(-2500, 2500)

        # Se usa en combinacion con el almost_out. elije un punto random, sigue de largo, llega al borde, repite.

        self.go_to((x_random, y_random))

    def stay_still(self)->None:
        """ Recuce la velocidad del personaje a valores insignificativos."""

        self.change_speed(0.0000000000001) # Que se mueva a esta velocidad es practcamente igual a que este quieto.
        self.estado = 'quieto'

    def in_summit(self) -> bool:
        '''
        Comprueba si el escalador alcanzo la cima
        
        Salida:
            booleano: Verdadero si alcanzo la cima. Falso en caso contrario.

        '''
        return self.comms.get_data()[self.equipo][self.nombre]['cima']


    def step_to_point2(self, poscicion: tuple|list, objetivo: tuple|list) -> float|int:
        '''
        Devuelve la distancia del paso que tiene que hacer hiker para llegar de un punto a otro.
        
        Argumentos de entrada:
            poscicion(tupla|lista): coordenadas (x,y) del punto de partida.
            objetivo (tupla|lista): coordenadas (x,y) del destino.
        
        Salida:
            Flotante|entero: distancia de paso.
        '''


        distance = distance_between(poscicion, objetivo) # distancia entre pos actual y destino
        if distance < 50: # Si el punto esta dentro del rango, el escalador puede ir directamente (no se pasa)
            return distance 
        return 50 # Si esta mas lejos, que se mueva lo mas rapido posible.
