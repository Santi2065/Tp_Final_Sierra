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
    """
    Grafica de diversas formas las posciciones de los escaladores durante la partida en curso.

    Argumentos de entrada:
        data (diccionario): Contiene todas las coordenadas (x,y,z) de todos los escaladores. 

    Metodos:
        graf_2d(): Grafico bidimensional de las posciones de los escaldaores de un equipo.
        heat_map(): Grafico bidimenisonal de calor respecto a la altura alcanzada por los escaladores.
        graf_3d(): Grafico tridimensional de las posciones de los escaldaores de un equipo.
    """
    def __init__(self, data: dict[str, dict[str, list[float]]]):
        matplotlib.use('agg') # Recurso utilizado para no crear muchas ventanas.
        
        self.data = data # Contiene todas las coordenadas.
        """ data: {'team1':
            'nombre1': {'x': [ ], 'y': [ ], 'z': [ ]}, ...}, ...
            'team2':
                ...} """


        # Inicializa los graficos

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
        self.angulo = 0  # Rotacion del grafico


    def graf_2d(self, nombre_equipo: str, colores=('#d11141', '#00b159', '#00aedb', '#f37735', '#ffc425')) -> None:
        """ 
        Proyecta en una interfaz un graficio bidimensional actualizado en tiempo
        real sobre las coordendas (x,y) de todos los escaladores de un equipo.

        Argumentos de entrada:
            nombre_equipo (cadena): Nombre del equipo sobre el cual se graficara.
            colores (tupla): Los colores que se usaran para graficar.
        """

        # Opcional - cambia la paleta de colores para los escaladores.
        colors1 = ('#e53a3a', '#ff5454', '#fdbd2e', '#a1d832', '#87be19') # rojo - amarillo - verde
        colors2 = ('#ff2500', '#ffa500', '#2986cc', '#b1ea78', '#7ddc1f') # rojo - azul - verde
        colors3 = ('#4deeea', '#74ee15', '#ffe700', '#f000ff', '#001eff') # neon
        colors4 = ('#ff0000', '#bf0000', '#800000', '#400000', '#000000') # rojo -> negro  (escala)
        colors5 = ('#d11141', '#00b159', '#00aedb', '#f37735', '#ffc425') # rojo - verde - cian - naranja - amarillo
        

        data = deepcopy(self.data[nombre_equipo]) # Previene errores de indice. 
        ax = self.ax1
        ax.cla() # Borra lo viejo y grafica todo de nuevo.

        
        # Para buscar los (x,y) maximos
        x_max = float('-inf') 
        y_max = float('-inf')


        for name, coords, colr in zip(data, data.values(), colores): # Grafica las coordenadas con su respectivo color.
            x = np.array(coords['x'])
            y = np.array(coords['y'])

            # Encuentra los maximos en estos puntos.
            x_max = max(x_max, np.max(np.abs(x)))
            y_max = max(y_max, np.max(np.abs(y)))

            # Achica el tamaño de los puntos a medida que hay mas.
            num_points = len(x)
            marker_size = 10 / np.sqrt(num_points)

            # Grafica los nuevos puntos.
            ax.scatter(x, y, s=marker_size, color=colr)

            # Pone el nombre del escalador en el ultimo punto que estuvo.
            last_coord = (coords['x'][-1], coords['y'][-1])
            ax.text(last_coord[0], last_coord[1], name, fontsize=9)


        # Encuentra el maximo de todos los valores.
        limit = max(x_max, y_max)

        # Ajusta la escala a medida que crece el rango.
        limit *= 1.1
        ax.set_xlim(-limit, limit) 
        ax.set_ylim(-limit, limit)

        # Pone la imagen en el fondo (estetica)
        ax.imshow(self.imagen, extent=[-limit, limit, -limit, limit], aspect='auto')

        

    def heat_map(self) -> None:
        """
        Grafico bidimenisonal de calor respecto a la altura alcanzada por los escaladores.
        """

        data = deepcopy(self.data)
        fig, ax = self.fig2, self.ax2 

        z_max = float('-inf')
        z_min = float('inf')

        # Crea listas con todos los puntos conocidos
        lx, ly, lz = [], [], [] # contiene todos los (x,y,z): lista x, lista y, lista z.
        for team_name in data:
            for name in data[team_name]:
                # Junta todas las coordenadas (x,y,z) en sus respectivas listas.
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


        ax.tripcolor(lx, ly, lz, shading='flat', cmap='hot', clim=[z_min, z_max]) # Grafica


        # Rotulos
        ax.set_title('Heat map')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')        
    
    def graf_3d(self, nombre_equipo: str) -> None:
        """
        Proyecta un grafico tridimensional actualizdo en tiempo real de la posicion actual de todos los jugadores.
        
        Argumento de entrada:
            nombre_equipo (cadena): Nombre del equipo sobre el cual se graficara.
        """

        fig, ax = self.fig3, self.ax3


        side = ((4.05 - 3) / 2) / 4.05

        fig.subplots_adjust(top=1.03, bottom=0.03, left=side, right=(1-side))

        ax.cla()

        info = deepcopy(self.data)


        coordenadas_x = [] # todas las x de los jugadores
        coordenadas_y = [] # todas las y de los jugadores        hay relacion elemento-jugador
        coordenadas_z = [] # todas las z de los jugadores

        for nombre_escalador in info[nombre_equipo]:
            x = info[nombre_equipo][nombre_escalador]['x']
            y = info[nombre_equipo][nombre_escalador]['y']
            z = info[nombre_equipo][nombre_escalador]['z']
            
            coordenadas_x += x
            coordenadas_y += y
            coordenadas_z += z

            ultima_coord = [info[nombre_equipo][nombre_escalador]['x'][-1],
                            info[nombre_equipo][nombre_escalador]['y'][-1],
                            info[nombre_equipo][nombre_escalador]['z'][-1]]

            ax.text(ultima_coord[0], ultima_coord[1], ultima_coord[2], nombre_escalador, fontsize=8)
           
        ax.scatter(coordenadas_x, coordenadas_y, coordenadas_z, c=coordenadas_z, cmap='hot') # Grafica
        
        # Estetica
        ax.set_xlim(min(coordenadas_x), max(coordenadas_x)) 
        ax.set_ylim(min(coordenadas_y), max(coordenadas_y)) # Los ejes en funcion del mapa descubierto
        ax.set_zlim(min(coordenadas_z), max(coordenadas_z))

        # Rotulos
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        ax.view_init(elev=10, azim=self.angulo)
        self.angulo += 2.5 # Grados de rotacion del grafico por iteracion.
    
  
                      