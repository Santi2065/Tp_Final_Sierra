from test_hiker import Hiker

from communication.client.client import MountainClient
from test_hiker import Hiker
import time
import essential_functions as ef

c = MountainClient()

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



lista_max = []

while not c.is_over():
    diccionario = c.get_data()

    print(ef.leaderboard(diccionario))
   
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