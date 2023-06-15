from communication.client.client import MountainClient
import random
import math
import time

c = MountainClient("10.42.0.1",8888)

class Hiker:
    def __init__(self,ordenes: list):
        self.ordenes = ordenes # Es una lista así lo puedo modiciar en el marco global. Lo uso como diccionario.
        self.direccion = self.ordenes[0]['Gian']['direction']
        self.velocidad = self.ordenes[0]['Gian']['speed']
        self.radio_montania = 23000
        self.team = 'Los cracks' # Hacer esto automaticamente
        self.nombre = 'Gian' # Hacer esto automaticamente


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
        

        next_x = x + self.velocidad * math.cos(self.direccion) # pos actual post iteracion (trigonometria)
        next_y = y + self.velocidad *math.sin(self.direccion) # pos actual post iteracion (trigonometria)

        afuera = math.sqrt(pow(next_x,2) + pow(next_y,2)) # si esto es mas chico que el radio, estoy dentro de la montaña.

        if afuera < self.radio_montania:
            return  False # Para el random, corregir --> que devuelva ((next_x , next_y),false)
        else:
            return True # Para el random

    def change_direction(self,new_direction:float|int):
        # El escalador se dirige hacia la nueva direccion (radianes)
        self.ordenes[0]['Gian']['direction'] = new_direction #Provisional, para hacer pruebas.

    def change_speed(self,new_speed:float|int):
        # Cambia la velocidad en la que el escalador se mueve (max 50)
        self.ordenes[0]['Gian']['speed'] = new_speed

    def go_to(self,coordenadas:tuple) -> float|int:
        # Devuelve el angulo nesceario para ir desde posicion actual --> coordenadas ingresadas (x,y)
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x'] # pos actual
        y =  dic[self.team][self.nombre]['y'] # pos actual
        
        x_destino = (coordenadas[0]) # pos destino
        y_destino = (coordenadas[1]) # pos destino

        angulo = math.atan2(y_destino-y,x_destino-x) # angulo para ir desde pos hasta destino. El orden es importante.

        return angulo # Devuelve el angulo
  
    def random(self):
        # El hiker entra en un estado de aleatoriedad y rebota por todo el mapa.
        # Se eligen de fomra aleatoria dos coordenadas por el centro del mapa --> sigue de largo, repite.

        x_random = random.uniform(-1000,1000)
        y_random = random.uniform(-1000,1000)

        self.change_direction(self.go_to((x_random,y_random)))

    def stay_still(self):
        # Recuce la velocidad del personaje a valores insignificativos.
        self.change_speed(0.0000000000001)




    



c.add_team('Los cracks', ['Gian'])
c.finish_registration()

directives = [{'Gian':{'direction':0,'speed':50}}] # Lo paso como lista para modificarlo en el marco global
gian = Hiker(directives)

while not c.is_over():

    print(c.get_data())
    c.next_iteration('Los cracks', directives[0])
    if gian.almost_out() is True:
        gian.random()

 
    time.sleep(0.2) # Para que no colapse el server
    







    

        


