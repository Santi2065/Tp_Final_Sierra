from communication.client.client import MountainClient
import random
import math
VELOCIDAD_MAX = 50

c = MountainClient()

class Hiker:
    
    def __init__(self, nombre:str, ordenes: list = [0,VELOCIDAD_MAX]):

        self.nombre = nombre # Hacer esto automaticamente (que no haya que pasarlo como arg de clase)
        self.ordenes = {'direction':ordenes[0],'speed':ordenes[1]} # Es una lista así lo puedo modificar en el marco global. Lo uso como diccionario.
        self.radio_montania = 23000
        self.team = 'Los cracks' # Hacer esto automaticamente

    def actual_pos(self):
        # Returns actual pos (x,y,z) of the hiker
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x'] # x actual
        y =  dic[self.team][self.nombre]['y'] # y actual
        z = dic[self.team][self.nombre]['z'] # z actual

        return (x,y,z)
    
    def almost_out(self)-> bool:
        """Devuelve verdadero si el escalador se ira del mapa en la siguiente iteracion. Falso en caso contrario."""
        info = self.actual_pos()
        x = info[0]
        y = info[1]

        norma = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        paso_previo = 22900 # Radio del circulo menos dos pasos , chequear que este bien

        if norma > paso_previo:
            return True
        else:
            return False
        
    def next_step(self)-> tuple:
        info = self.actual_pos()
        x = info[0]
        y = info[1]
        

        next_x = x + self.ordenes['speed'] * math.cos(self.ordenes['direction']) # pos actual post iteracion (trigonometria)
        next_y = y + self.ordenes['speed'] * math.sin(self.ordenes['direction']) # pos actual post iteracion (trigonometria)

        afuera = math.sqrt(pow(next_x,2) + pow(next_y,2)) # si esto es mas chico que el radio, estoy dentro de la montaña.

        return (next_x, next_y)

    def change_direction(self, new_direction: float|int):
        # El escalador se dirige hacia la nueva direccion (radianes)
        self.ordenes['direction'] = new_direction #Provisional, para hacer pruebas.

    def change_speed(self, new_speed: float|int):
        # Cambia la velocidad en la que el escalador se mueve (max 50)
        self.ordenes['speed'] = new_speed

    def go_to(self,objective:list):
        info = self.actual_pos()
        hiker_coords = [info[0],info[1]]
        self.ordenes = {'direction':direction(hiker_coords,objective),'speed':VELOCIDAD_MAX}
  
    def random(self):
        # El hiker entra en un estado de aleatoriedad y rebota por todo el mapa.
        # Se eligen de fomra aleatoria dos coordenadas por el centro del mapa --> sigue de largo, repite.

        x_random = random.uniform(-2500, 2500)
        y_random = random.uniform(-2500, 2500)

        self.change_direction(self.go_to((x_random, y_random)))

    def stay_still(self):
        # Recuce la velocidad del personaje a valores insignificativos.
        self.change_speed(0.0000000000001)
    
    def cima(self) -> bool:
        # Devuelve si esta en la cima o no
        return c.get_data()[self.team][self.nombre]['cima']
    
class Team:
    def __init__(self,nombre,hikers) -> None:
        self.nombre = nombre
        self.hikers = hikers

    def face_out(self):
        direction=0
        for hiker in self.hikers:
            hiker.change_direction(direction)
            direction += math.pi/2

    def move_all(self,hikers) -> None:
        c.next_iteration(self.nombre, {h.nombre: h.ordenes for h in hikers})
        for hiker in hikers:
            if hiker.almost_out():
                hiker.random()


def direction(hiker: list, objective: list) -> float:
    dx = objective[0] - hiker[0]
    dy = objective[1] - hiker [1]
    return math.atan2(dy,dx)

def go_center(team):
    #apuntan al centro
    for hiker in team.hikers:
        hiker.go_to([0,0])

    #se mueven hasta que llegan
    llegada = {x : 0 for x in team.hikers}
    no_llegaron = True
    while no_llegaron:
        team.move_all(team.hikers)
        info = c.get_data()
        for hiker in team.hikers:
            x =  info[team.nombre][hiker.nombre]['x']
            y =  info[team.nombre][hiker.nombre]['y']
            if -1 < x < 1 and -1 < y < 1:
                llegada[hiker] = 1
                hiker.stay_still()
        no_llegaron = False
        for x in llegada:
            if x == 0:
                no_llegaron = True
    print("En el centro")
            

def start_search():
    pass



def main():
    
    hikers_names = [Hiker('Gian').nombre,Hiker('Pipe').nombre,Hiker('Santi').nombre,Hiker('Joaco').nombre]
    hikers = [Hiker('Gian'),Hiker('Pipe'),Hiker('Santi'),Hiker('Joaco')]
    team = Team('Los cracks',hikers)
    
    c.add_team(team.nombre, hikers_names)
    c.finish_registration()

    go_center(team)

    
if __name__ == "__main__":
    main()

