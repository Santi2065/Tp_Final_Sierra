from communication.client.client import MountainClient
from HIKERS import Hiker
import matplotlib.pyplot as plt
import time

c = MountainClient()
class leader_board:

    def __init__(self) :
        pass
 
    def graficar(self):

        diccionario = c.get_data()
        jugador_max = None # Chequear si cambian de algo
        altura_max = None
        lista= []


        for equipo, jugadores in diccionario.items():
            jugador_max,altura_max= max(jugadores.items(),key=lambda item:item[1]['z'])
            lista.append([jugador_max,altura_max['z']]) # [nombre,z]

        ordenar_lista = sorted(lista,key=lambda x:x[1]) # De mas alto a mas chico
        


       
        print("*** Leader per team ***")
        print("Position | player | z")
        for i in range(len(ordenar_lista)):
            print(f"{i+1}: {ordenar_lista[i][0]} | {round(ordenar_lista[i][1],3)}")


        lista.clear() # limpia listas para no interferir con las nuevas listas



c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.finish_registration()

directives = {'Gian':{'direction':0,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}



hikers = [] # Esta es la lista que se le pasa a la clase graficos.
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))



leader = leader_board()

while not c.is_over():

    print(c.get_data())
    leader.graficar()

    c.next_iteration('Los cracks', {h.nombre: h.ordenes for h in hikers})
    if hikers[0].almost_out() is True:
        hikers[0].random()
    if hikers[1].almost_out() is True:
        hikers[1].random()
    if hikers[2].almost_out() is True:
        hikers[2].random()
    if hikers[3].almost_out() is True:
        hikers[3].random()


    time.sleep(0.5) # Para que no colapse el server