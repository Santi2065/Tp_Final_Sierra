from communication.client.client import MountainClient
from test_hiker import Hiker
import time

c = MountainClient()
class leader_board:

    def __init__(self) :
        self.contador_racha = 0
        self.anterior_top1 = None
 
    def graficar(self):

        diccionario = c.get_data()
        jugador_max = None # Chequear si cambian de algo
        altura_max = None
        lista= []
        aux_racha = []
        top_1 = None
        corto_racha = False


        for equipo, jugadores in diccionario.items():
            jugador_max,altura_max= max(jugadores.items(),key=lambda item:item[1]['z'])
            lista.append([jugador_max,altura_max['z'],equipo]) # [nombre,z,equipo]

        ordenar_lista = sorted(lista,key=lambda x:-x[1]) # De mas alto a mas chico, puse el '-' pq si no me la ordenaba al reves
        
        top_1 = ordenar_lista[0][0]
        aux_racha.append(top_1) # El jugador top 1

        for x in aux_racha:
            if x != top_1:
                corto_racha = True
                self.contador_racha = 0
                aux_racha.clear()

        if corto_racha is False and (self.anterior_top1 == None or self.anterior_top1 == top_1):
            self.contador_racha += 1
        else:
            self.contador_racha = 0

        self.anterior_top1 = top_1

        for i in range(len(ordenar_lista)):
            if self.contador_racha > 4 and i == 0:
                print(f"🔥{i+1} -> {ordenar_lista[i][2]} | {ordenar_lista[i][0]} | {round(ordenar_lista[i][1],3)}")
            else:
                print(f"{i+1} -> {ordenar_lista[i][2]} | {ordenar_lista[i][0]} | {round(ordenar_lista[i][1],3)}")

        lista.clear() # limpia listas para no interferir con las nuevas listas



c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.add_team('puto', ['esc1','esc2','esc3','esc4'])
c.finish_registration()

directives = {'Gian':{'direction':6,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}

ord = {'esc1':{'direction':0,'speed':50}, 'esc2':{'direction':50,'speed':50},'esc3':{'direction':95,'speed':50},'esc4':{'direction':31,'speed':50}}


hikers = [] # Esta es la lista que se le pasa a la clase graficos.
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))

escala = []
escala.append(Hiker(ord['esc1'],'esc1'))
escala.append(Hiker(ord['esc2'],'esc2'))
escala.append(Hiker(ord['esc3'],'esc3'))
escala.append(Hiker(ord['esc4'],'esc4'))



leader = leader_board()

while not c.is_over():

    leader.graficar()

    c.next_iteration('Los cracks', {h.nombre: h.ordenes for h in hikers})
    c.next_iteration('puto',{i.nombre: i.ordenes for i in escala})
    if hikers[0].almost_out() is True:
        hikers[0].random()
    if hikers[1].almost_out() is True:
        hikers[1].random()
    if hikers[2].almost_out() is True:
        hikers[2].random()
    if hikers[3].almost_out() is True:
        hikers[3].random()
        


    time.sleep(0.5) # Para que no colapse el server