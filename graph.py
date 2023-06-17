from HIKERS import Hiker
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Grafico_2d_equipo: # anda, pero hay que automatizar para que funcione con los jugadores que quieras
    def __init__(self,hikers:list ):
        self.hiker1 = hikers[0]
        self.hiker2 = hikers[1]
        self.hiker3 = hikers[2]
        self.hiker4 = hikers[3]

        
        self.fig, self.ax = plt.subplots()
        self.labels = []
        nombres =[self.hiker1.nombre,self.hiker2.nombre,self.hiker3.nombre,self.hiker4.nombre] # esto es lo de automatizar
        for i in range(len(hikers)):
            label = self.ax.text(0, 0, nombres[i], ha='center', va='bottom')
            self.labels.append(label)

        self.imagen = mpimg.imread('fondo.jpeg') # Fondo del grafico 

    def coordenadas(self,hikers:list,movimiento:dict):
        
        x = []
        y = []

        for hiker in hikers:
            x.append(movimiento[hiker.team][hiker.nombre]['x'])
            y.append(movimiento[hiker.team][hiker.nombre]['y'])

        plt.xlim(-23000,23000)
        plt.ylim(-23000,23000)
        plt.xticks([])
        plt.yticks([])
        self.ax.imshow(self.imagen, extent=[-23000, 23000, -23000, 23000], aspect='auto') # Que la imagen cunpla con los limites

        
        
        for i in range(len(x)):
            self.labels[i].set_position((x[i], y[i]))
        


        plt.scatter(x,y,c='c')
        plt.show(block=False)
        plt.pause(0.01)