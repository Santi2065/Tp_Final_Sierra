from communication.client.client import MountainClient
from test_hiker import Hiker
import matplotlib.pyplot as plt
import time
import matplotlib.image as mpimg

c = MountainClient()



class Grafico_2d_equipo: # anda, pero hay que automatizar para que funcione con los jugadores que quieras
    def __init__(self, hikers: list[Hiker]):
        self.hikers = hikers

        
        self.fig, self.ax = plt.subplots()
        self.labels = []
        #nombres = [self.hiker1.nombre,self.hiker2.nombre,self.hiker3.nombre,self.hiker4.nombre] # esto es lo de automatizar
        nombres = [hiker.nombre for hiker in hikers]
        for i in range(len(hikers)):
            label = self.ax.text(0, 0, nombres[i], ha='center', va='bottom')
            self.labels.append(label)

        self.imagen = mpimg.imread('fondo.jpeg') # Fondo del grafico 

    def coordenadas(self):
        '''co_h1 = self.hiker1.actual_pos()
        co_h2 = self.hiker2.actual_pos() # automatizar esto
        co_h3 = self.hiker3.actual_pos()
        co_h4 = self.hiker4.actual_pos()'''

        coords = [hiker.actual_pos() for hiker in self.hikers]

        x =[coord[0] for coord in coords]
        y =[coord[1] for coord in coords]

        #plt.xlim(-23000,23000)
        #plt.ylim(-23000,23000)
        size = 1500
        plt.xlim(-size, size)
        plt.ylim(-size, size)
        plt.xticks([])
        plt.yticks([])
        #self.ax.imshow(self.imagen, extent=[-23000, 23000, -23000, 23000], aspect='auto')
        self.ax.imshow(self.imagen, extent=[-size, size, -size, size], aspect='auto') # Que la imagen cunpla con los limites

        for i in range(len(x)):
            self.labels[i].set_position((x[i], y[i]))
        

        plt.scatter(x,y,c='c')
        plt.show(block=False)
        plt.pause(0.005)


c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.finish_registration()

directives = {'Gian':{'direction':0,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}



hikers = [] # Esta es la lista que se le pasa a la clase graficos.
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))



grafico2d = Grafico_2d_equipo(hikers)

while not c.is_over():

    print(c.get_data())
    grafico2d.coordenadas()

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