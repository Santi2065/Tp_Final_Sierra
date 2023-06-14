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
            puntos.append(((dic[team][hiker]["x"]**2)+(dic[team][hiker]["y"]**2))**1/2,dic[team][hiker]["z"])
        c.next_iteration(team,{hiker:{'direction':direccion+(math.pi/2),'speed':20}})
        direccion += rayo * (math.pi/4)/ray_number
        maximos.append(estimate_max_height(puntos))
        
    return maximos
    