from communication.client.client import MountainClient

import math
import time

c = MountainClient()

class Hiker:
    def __init__(self,ordenes: dict):
        self.ordenes = ordenes #
        self.direccion = self.ordenes['Gian']['direction']
        self.velocidad = self.ordenes['Gian']['speed']
        self.radio_montania = 23000
        self.team = 'Los cracks' # Hacer esto automatico
        self.nombre = 'Gian' # Hacer esto automatico


    def almost_out(self)-> bool:
        """Devuelve verdadero si el escalador se ira del mapa en la siguiente iteracion. Falso en caso contrario."""
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x']
        y =  dic[self.team][self.nombre]['y']

        norma = math.sqrt(math.pow(x,2) + math.pow(y,2))
        paso_previo = 22950 # Radio del circulo menos dos pasos , chequear que este bien

        if norma > paso_previo:
            return True
        else:
            return False
        
    def next_step(self)-> tuple:
        dic = c.get_data()
        x =  dic[self.team][self.nombre]['x']
        y =  dic[self.team][self.nombre]['y']
        

        next_x = x + self.velocidad * math.cos(self.direccion)
        next_y = y + self.velocidad *math.sin(self.direccion)

        afuera = math.sqrt(pow(next_x,2) + pow(next_y,2))

        if afuera < self.radio_montania:
            return  (next_x , next_y), False # [0] = x post iteracion , [1] = y post iteracion. # Falso si se fue
        else:
            return True

    def change_direction(self,new_direction):
        # Cambia la direccion (en rad) del escalador
        self.ordenes['Gian']['direction'] = new_direction + self.direccion #Provisional, para hacer pruebas.



    def change_speed(self,new_speed):
        self.ordenes['Gian']['speed'] = new_speed

  


    

direccion_inicial = 0 # direccion

c.add_team('Los cracks', ['Gian'])
c.finish_registration()

directives = {'Gian':{'direction':direccion_inicial,'speed':50}}
gian = Hiker(directives)

while not c.is_over():

    print(c.get_data())
    c.next_iteration('Los cracks', directives)
    print(gian.almost_out())
    if gian.almost_out() is True:
        gian.change_direction(math.pi)
   

    time.sleep(0.2) # Para que no colapse el server
    







    

        


