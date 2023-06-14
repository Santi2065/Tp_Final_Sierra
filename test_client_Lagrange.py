from communication.client.client import MountainClient
import Lagrange_walk
import math
import Lagrange
CANTIDAD_DE_PUNTOS = 15

def lagrange_walk(team:str,hiker:str,d_inicial:float,ray_number:int):
    direccion = d_inicial
    maximos = []
    
    for rayo in range(ray_number):
        puntos = []
        for punto in range(CANTIDAD_DE_PUNTOS):
            c.next_iteration(team,{hiker:{'direction':direccion,'speed':20}})
            dic = c.get_data()
            puntos[0].append(((dic[team][hiker]["x"]**2)+(dic[team][hiker]["y"]**2))**1/2)
            puntos[1].append(dic[team][hiker]["z"])
        c.next_iteration(team,{hiker:{'direction':direccion+(math.pi/2),'speed':20}})
        direccion += rayo * (math.pi/4)/ray_number
        maximos.append(estimate_max_height(puntos))
        
    return maximos
    
def __main__():
    c = MountainClient()
    c.add_team('Los cracks', ['Santi'])
    c.finish_registration()
    
    maximos = Lagrange_walk.lagrange_walk('Los cracks','Santi',0,10)
    
    
    while not c.is_over():
        while(not c.next_iteration('Los cracks', directives)):
            continue
        print(c.get_data())