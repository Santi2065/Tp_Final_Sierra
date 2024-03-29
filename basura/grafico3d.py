from communication.client.client import MountainClient
import random, math, time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import numpy as np
import pandas as pd
from copy import deepcopy
from tpf_Montana_essential_functions import difference, magnitude
from tpf_Montana_graficos import Hiker
import matplotlib.animation as animation


class Grafico3D:
    def __init__(self,):
        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111,projection='3d')
        self.angulo = 0 % 360

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


        z_promedio = (max(cz) + min(cz)) /2 # para usos esteticos
        


        colores = []
        for i in range(len(cz)):
            if cz[i] <= (min(cz) + z_promedio) /2:
                colores.append('#B57C00') # amarillo oscuro
            elif cz[i] > (min(cz) + z_promedio) / 2 and cz[i] <= (z_promedio + max(cz)) / 2:
                colores.append('#D85716') # naranje oscuro
            else:
                colores.append('#8B0000') # rojo oscuro
        

        (self.ax).set_facecolor('lightgray')

        (self.ax).scatter(cx,cy,cz,c=colores)









        (self.ax).set_xlim(min(cx),max(cx))
        (self.ax).set_ylim(min(cy),max(cy))
        (self.ax).set_zlim(min(cz),max(cz))
        

        (self.ax).set_xticks([])
        (self.ax).set_yticks([])
        (self.ax).set_zticks([])

       
        
        colores.clear()
        self.ax.view_init(elev=10, azim=self.angulo)
        self.angulo += 2.5 # Grados que rote
  
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