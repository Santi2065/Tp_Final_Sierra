from communication.client.client import MountainClient
import random, math, time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import numpy as np
from copy import deepcopy
from essential_functions import difference, magnitude

#c = MountainClient("10.42.0.1", 8888)
c = MountainClient()

class Graficador:
    '''Objeto que hace graficas de posicion y altura
    \ndata: {'nombre1': {'x': [], 'y': [], 'z': []}, ...}'''
    #def __init__(self, hikers: list[Hiker]):
    def __init__(self, data: dict[str, dict[str, list[float]]]):
        matplotlib.use('agg')
        #self.hikers = hikers
        self.data = data

        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig3 = plt.figure()
        self.ax3 = self.fig3.add_subplot(111, projection='3d')

        self.ax1.set_aspect('equal')
        self.ax2.set_aspect('equal')
        self.ax3.set_aspect('equal')

        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')

        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')

        self.ax3.set_xlabel('X')
        self.ax3.set_ylabel('Y')
        self.ax3.set_zlabel('Z')

        self.last_index = 0
        self.imagen = mpimg.imread('fondo.jpeg') # Fondo del grafico
        self.angulo = 0 % 359

    def coordenadas(self):
        coords = [hiker.actual_pos() for hiker in self.hikers]

        x =[coord[0] for coord in coords]
        y =[coord[1] for coord in coords]

        #plt.xlim(-23000,23000)
        #plt.ylim(-23000,23000)
        size = 1000
        plt.xlim(-size, size)
        plt.ylim(-size, size)
        plt.xticks([])
        plt.yticks([])
        #self.ax.imshow(self.imagen, extent=[-23000, 23000, -23000, 23000], aspect='auto')
        self.ax.imshow(self.imagen, extent=[-size, size, -size, size], aspect='auto') # Que la imagen cunpla con los limites

        for i in range(len(x)):
            self.labels[i].set_position((x[i], y[i]))
        

        plt.scatter(x, y, c='c', s=10)
        plt.show(block=False)
        plt.pause(0.005)


    def coordenadas2(self, team_name: str, colors=('#d11141', '#00b159', '#00aedb', '#f37735', '#ffc425')) -> None:
        '''
        Grafico que el nombre del equipo y muestra la grafica de sus puntos.\n
        data: {'team1':
                    'nombre1': {'x': [ ], 'y': [ ], 'z': [ ]}, ...}, ...
                'team2':
                    ...}
        '''

        #plt.ion()
        colors1 = ('#e53a3a', '#ff5454', '#fdbd2e', '#a1d832', '#87be19') # red-yel-gre
        colors2 = ('#ff2500', '#ffa500', '#2986cc', '#b1ea78', '#7ddc1f') # red-blu-gre
        colors3 = ('#4deeea', '#74ee15', '#ffe700', '#f000ff', '#001eff') # neon
        colors4 = ('#ff0000', '#bf0000', '#800000', '#400000', '#000000') # red -> black
        colors5 = ('#d11141', '#00b159', '#00aedb', '#f37735', '#ffc425') # red-green-cyan-oran-yel
        colors_test = colors

        data = deepcopy(self.data[team_name])
        ax = self.ax1
        ax.cla()

        colors = colors_test

        x_max = float('-inf')
        y_max = float('-inf')

        #* Borra los nombres anteriores
        #*for text in ax.texts:
        #*    text.set_text('')

        for name, coords, colr in zip(data, data.values(), colors):
            x = np.array(coords['x'])
            y = np.array(coords['y'])

            # Encuentra los maximos en estos puntos
            x_max = max(x_max, np.max(np.abs(x)))
            y_max = max(y_max, np.max(np.abs(y)))

            # Achica el tamaño de los puntos a medida que hay mas
            num_points = len(x)
            marker_size = 10 / np.sqrt(num_points)

            #* Lista con los nuevos valores a graficar
            #*new_x = x[self.last_index:]
            #*new_y = y[self.last_index:]

            #* Grafica los nuevos puntos
            #*ax.scatter(new_x, new_y, s=marker_size, color=colr)
            ax.scatter(x, y, s=marker_size, color=colr)

            # Actualiza el indice del ultimo valor graficado
            self.last_index = len(x) - 1

            # Pone el nombre del escalador en el ultimo punto que estuvo
            last_coord = (coords['x'][-1], coords['y'][-1])
            ax.text(last_coord[0], last_coord[1], name, fontsize=9)

        #* Actualiza el indice del ultimo valor graficado
        #*for coords in data.values():
        #*    self.last_index = len(data.values()[0]['x'])

        # Encuentra el maximo de todos los valores
        limit = max(x_max, y_max)

        # Ajusta la escala a medida que crece el rango
        limit += limit/10
        ax.set_xlim(-limit, limit) 
        ax.set_ylim(-limit, limit)

        # Pone la imagen en el fondo
        ax.imshow(self.imagen, extent=[-limit, limit, -limit, limit], aspect='auto')

        # Actualiza el grafico, por performance
        #!self.fig1.canvas.draw_idle()
        #!plt.show(block=False)

        #plt.pause(0.00001)

    def heat_map(self) -> None:
        data = deepcopy(self.data)
        fig, ax = self.fig2, self.ax2

        z_max = float('-inf')
        z_min = float('inf')
        # Crea listas con todos los puntos conocidos
        lx, ly, lz = [], [], []
        for team_name in data:
            for name in data[team_name]:
                lx += data[team_name][name]['x']
                ly += data[team_name][name]['y']
                lz += data[team_name][name]['z']

                # Guarda el valor maximo y minimo global de z
                z = data[team_name][name]['z']
                z_max = max(z) if max(z) > z_max else z_max
                z_min = min(z) if min(z) < z_min else z_min

        # Si no tiene tres puntos unicos no puede graficar nada
        if len(set(lx)) < 3:
            return

        #tpc = ax.tripcolor(lx, ly, lz, shading='flat', cmap='hot', clim=[z_min, z_max])
        tpc = ax.tripcolor(lx, ly, lz, shading='gouraud', cmap='hot', clim=[z_min, z_max])

        #TODO: probar colorbar en init asi no hace uno nuevo cada vez que es llamado
        colorbar = self.fig2.colorbar(tpc)
        colorbar.ax.set_ylim(z_min, z_max)
        colorbar.ax.set_title('Height', fontsize=9)

        ax.set_title('Map shape')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_aspect('equal')
        #fig.show()
        plt.pause(0.001)
    
    def graf_3d(self, nombre_equipo: str) -> None:
        """Proyecta un grafico tridimensional actualizdo en tiempo real de la posicion actual de todos los jugadores."""

        fig, ax = self.fig3, self.ax3

        ax.cla()

        diccionario = deepcopy(self.data)
        #!
        #*diccionario = c.get_data()

        coordenadas_x = [] # todas las x de los jugadores
        coordenadas_y = [] # todas las y de los jugadores        hay relacion elemento-jugador
        coordenadas_z = [] # todas las z de los jugadores

        for nombre_escalador in diccionario[nombre_equipo]:
            x = diccionario[nombre_equipo][nombre_escalador]['x']
            y = diccionario[nombre_equipo][nombre_escalador]['y']
            z = diccionario[nombre_equipo][nombre_escalador]['z']
            #!
            coordenadas_x += x
            coordenadas_y += y
            coordenadas_z += z
            #cx.append(x)
            #cy.append(y)
            #cz.append(z)
            #!
            #*coordenadas.append([x, y, z])
            # [ [x,y,z] ,[x,y,z] ] etcetera  

        ax.set_facecolor('lightgray') # Color del fondo del grafico

        #*ax.scatter(cx, cy, cz, c=colores)
        #!
        sc = ax.scatter(coordenadas_x, coordenadas_y, coordenadas_z, c=coordenadas_z, cmap='hot')
        #!
        ax.set_xlim(min(coordenadas_x), max(coordenadas_x)) 
        ax.set_ylim(min(coordenadas_y), max(coordenadas_y))        # Los ejes en funcion del mapa descubierto
        ax.set_zlim(min(coordenadas_z), max(coordenadas_z))

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        #*ax.set_xticks([])
        #*ax.set_yticks([])
        #*ax.set_zticks([])


        #*colores.clear()
        ax.view_init(elev=10, azim=self.angulo)
        self.angulo += 2.5 # Grados de rotacion del grafico por iteracion.
  
        #plt.ion()
        #plt.show(block=False)
        plt.pause(0.001)