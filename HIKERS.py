from communication.client.client import MountainClient
import random
import math
import time

c = MountainClient('10.42.0.1',8888)

class Hiker:
    def __init__(self,ordenes: list,nombre:str):

        self.nombre = nombre # Hacer esto automaticamente (que no haya que pasarlo como arg de clase)
        self.ordenes = ordenes # Es una lista así lo puedo modiciar en el marco global. Lo uso como diccionario.
        self.radio_montania = 23000
        self.team = 'Los cracks' # Hacer esto automaticamente
    def almost_out(self)-> bool:
        """Devuelve verdadero si el escalador se ira del mapa en la siguiente iteracion. Falso en caso contrario."""
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x']
        y =  dic[self.team][self.nombre]['y']

        norma = math.sqrt(math.pow(x,2) + math.pow(y,2))
        paso_previo = 22900 # Radio del circulo menos dos pasos , chequear que este bien

        if norma > paso_previo:
            return True
        else:
            return False
        
    def next_step(self)-> tuple:
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x'] # pos actual
        y =  dic[self.team][self.nombre]['y'] # pos actual
        

        next_x = x + self.ordenes['speed'] * math.cos(self.ordenes['direction']) # pos actual post iteracion (trigonometria)
        next_y = y + self.ordenes['speed'] *math.sin(self.ordenes['direction']) # pos actual post iteracion (trigonometria)

        afuera = math.sqrt(pow(next_x,2) + pow(next_y,2)) # si esto es mas chico que el radio, estoy dentro de la montaña.

        return (next_x,next_y)

    def change_direction(self,new_direction:float|int):
        # El escalador se dirige hacia la nueva direccion (radianes)
        self.ordenes['direction'] = new_direction #Provisional, para hacer pruebas.

    def change_speed(self,new_speed:float|int):
        # Cambia la velocidad en la que el escalador se mueve (max 50)
        self.ordenes['speed'] = new_speed

    def go_to(self,coordenadas:tuple) -> float|int:
        # Devuelve el angulo nesceario para ir desde posicion actual --> coordenadas ingresadas (x,y)
        dic = c.get_data() # Esto quiza pasarlo a un diccionario general
        x =  dic[self.team][self.nombre]['x'] # pos actual
        y =  dic[self.team][self.nombre]['y'] # pos actual
        
        x_destino = (coordenadas[0]) # pos destino
        y_destino = (coordenadas[1]) # pos destino

        angulo = math.atan2(y_destino-y,x_destino-x) # angulo para ir desde pos hasta destino. El orden es importante.

        return angulo # Devuelve el angulo
  
    def random(self):
        # El hiker entra en un estado de aleatoriedad y rebota por todo el mapa.
        # Se eligen de fomra aleatoria dos coordenadas por el centro del mapa --> sigue de largo, repite.

        x_random = random.uniform(-2500,2500)
        y_random = random.uniform(-2500,2500)

        self.change_direction(self.go_to((x_random,y_random)))

    def stay_still(self):
        # Recuce la velocidad del personaje a valores insignificativos.
        self.change_speed(0.0000000000001)

    def actual_pos (self):
        # Returns actual pos (x,y,z) of the hiker
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x'] # x actual
        y =  dic[self.team][self.nombre]['y'] # y actual
        z = dic[self.team][self.nombre]['z'] # z actual

        return (x,y,z)



c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.finish_registration()

directives = {'Gian':{'direction':0,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}



hikers = []
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))

while not c.is_over():

    print(hikers[2].actual_pos())
    c.next_iteration('Los cracks', {h.nombre: h.ordenes for h in hikers})
    if hikers[0].almost_out() is True:
        hikers[0].random()
    if hikers[1].almost_out() is True:
        hikers[1].random()
    if hikers[2].almost_out() is True:
        hikers[2].random()
    if hikers[3].almost_out() is True:
        hikers[3].random()


 
    time.sleep(0.2) # Para que no colapse el server
    

