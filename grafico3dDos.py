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
import matplotlib.animation as animation

def update_coords(coords: dict[str, dict[str, list[float]]], c: MountainClient) -> None:
    '''Actualiza la historia de coordenadas de todos los escaladores de un equipo'''
    data = c.get_data()
    for team_name in data:
        for name in data[team_name]:
            x = data[team_name][name]['x']
            y = data[team_name][name]['y']
            z = data[team_name][name]['z']
            coords[team_name][name]['x'] += [x]
            coords[team_name][name]['y'] += [y]
            coords[team_name][name]['z'] += [z]

class Grafico3D:
    #*def __init__(self):
    def __init__(self, coords: dict[str, dict[str, dict[str, list[float]]]]):
        '''Arguments:
        coords: {'team1': {'hiker1': {'x': [],'y': [],'z': []}}}'''
        self.coords = coords
        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111, projection='3d')
        self.angulo = 0 % 360

    def graficar(self):
        #!
        fig, ax = self.figura, self.ax

        ax.cla()

        diccionario = deepcopy(self.coords)
        #!
        #*diccionario = c.get_data()
       
        #*coordenadas = []
        cx = [] # todas las x
        cy = [] # todas las y            estan relacionadas las x,y,z de cada elemento.
        cz = [] # todas las z

        for team_name in diccionario:
            for hiker in diccionario[team_name]:
                x = diccionario[team_name][hiker]['x']
                y = diccionario[team_name][hiker]['y']
                z = diccionario[team_name][hiker]['z']
                #!
                cx += x
                cy += y
                cz += z
                #cx.append(x)
                #cy.append(y)
                #cz.append(z)
                #!
                #*coordenadas.append([x, y, z])
                # [ [x,y,z] ,[x,y,z] ] etcetera

        #*for i in range(len(coordenadas)): # Se podia quizas saltear el paso de antes, pero queda ilejible.
        #*    cx.append(coordenadas[i][0])
        #*    cy.append(coordenadas[i][1])
        #*    cz.append(coordenadas[i][2])


        '''z_promedio = (max(cz) + min(cz)) /2 # para usos esteticos


        colores = []
        for i in range(len(cz)):
            if cz[i] <= (min(cz) + z_promedio) /2:
                colores.append('#B57C00') # amarillo oscuro
            elif cz[i] > (min(cz) + z_promedio) / 2 and cz[i] <= (z_promedio + max(cz)) / 2:
                colores.append('#D85716') # naranje oscuro
            else:
                colores.append('#8B0000') # rojo oscuro'''
        

        ax.set_facecolor('lightgray')

        #*ax.scatter(cx, cy, cz, c=colores)
        #!
        sc = ax.scatter(cx, cy, cz, c=cz, cmap='hot')


        #print(f'cx: {cx}, len={len(cx)}')
        #print(f'cy: {cy}, len={len(cy)}')
        #print(f'cz: {cz}, len={len(cz)}')
        #!
        ax.set_xlim(min(cx), max(cx))
        ax.set_ylim(min(cy), max(cy))
        ax.set_zlim(min(cz), max(cz))

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        

        #*ax.set_xticks([])
        #*ax.set_yticks([])
        #*ax.set_zticks([])

       
        
        #*colores.clear()
        ax.view_init(elev=10, azim=self.angulo)
        self.angulo += 2.5 # Grados que rote
  
        #*plt.ion()
        #plt.show(block=False)
        plt.pause(0.01)
    
        



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

data = c.get_data()

#!
coords = {team_name:
                {hiker:
                        {'x': [data[team_name][hiker]['x']],
                         'y': [data[team_name][hiker]['y']],
                         'z': [data[team_name][hiker]['z']]}
                for hiker in data[team_name]}
          for team_name in data}
#!

grafico = Grafico3D(coords)

i = 0
while not c.is_over():

    #grafico.graficar()


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
    
    #!
    update_coords(coords, c)
    if i % 1 == 0:
        grafico.graficar()
    i += 1
    #!


    time.sleep(0.05) # Para que no colapse el server