from communication.client.client import MountainClient
import random, math, time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import numpy as np
import pandas as pd
from copy import deepcopy
from essential_functions import difference, magnitude
from test_hiker import Hiker



class Grafico3D:
    def __init__(self,):
        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111,projection='3d')


    def graficar(self):
        
        diccionario = c.get_data()
       
        coordenadas = []
        cx = [] # todas las x
        cy = [] # todas las y            estan relacionadas las x,y,z de cada elemento.
        cz = [] # todas las z

        for i in diccionario:
            for x in diccionario[i]:
                coordenadas.append([diccionario[i][x]['x'],diccionario[i][x]['y'],diccionario[i][x]['z']])
                # [ [x,y,z] ,[x,y,z] ] etcetera

        for i in range(len(coordenadas)): # Se podia quizas saltear el paso de antes, pero queda ilejible.
            cx.append(coordenadas[i][0])
            cy.append(coordenadas[i][1])
            cz.append(coordenadas[i][2])
        
        (self.ax).scatter(cx,cy,cz)

        (self.ax).set_xlim(-23000,23000)
        (self.ax).set_ylim(-23000,23000)
        (self.ax).set_zlim(min(cz),max(cz))
        

        (self.ax).set_xticks([])
        (self.ax).set_yticks([])
        (self.ax).set_zticks([])

  
        plt.ion()
        plt.show()
        plt.pause(0.5)
    
        



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



grafico = Grafico3D()

while not c.is_over():

    print(c.get_data())
    grafico.graficar()


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