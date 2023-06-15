from communication.client.client import MountainClient
import random
import math
import time
from HIKERS import Hiker
import plotly

c = MountainClient()


class Graficos:
    def __init__(self,hikers:list ):













c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.finish_registration()

directives = {'Gian':{'direction':0,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}



hikers = [] # Esta es la lista que se le pasa a la clase graficos.
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))

while not c.is_over():

    print(hikers[0].actual_pos())
    print(hikers[1].actual_pos())
    print(hikers[2].actual_pos())
    print(hikers[3].actual_pos())

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

