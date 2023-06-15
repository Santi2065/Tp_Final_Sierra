from communication.client.client import MountainClient
import random
import math
import time
from gianluca import Hiker
import plotly

c = MountainClient()


class Graficos:
    def __init__(self,hiker1:Hiker,hiker2:Hiker,hiker3:Hiker,hiker4:Hiker)








c.add_team('Los cracks', ['Gian','Pipe','Santi','Joaco'])
c.finish_registration()

directives_gian = [{'Gian':{'direction':0,'speed':50}}] # Lo paso como lista para modificarlo en el marco global
gian = Hiker(directives_gian,'Gian')

while not c.is_over():

    print(c.get_data())
    c.next_iteration('Los cracks', directives[0])
    if gian.almost_out() is True:
        gian.random()

 
    time.sleep(0.2) # Para que no colapse el server

