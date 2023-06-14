from communication.client.client import MountainClient
import math
import Lagrange
CANTIDAD_DE_PUNTOS = 50
MAX_SPEED = 50

def ang(hiker: list, flag: list):
    v1 = []
    v2 = []
    aux = []
    if hiker[1] > flag[1]:
        aux.append(flag[0])
        aux.append(hiker[1])
        for i in range(2):
            v1 += [flag[i] - hiker[i]]
            v2 += [aux[i] - hiker[i]]
    else:
        aux.append(hiker[0])
        aux.append(flag[1])
        for i in range(2):
            v1 += [hiker[i] - flag[i]]
            v2 += [aux[i] - flag[i]]
    
    product = v1[0] * v2[0] + v1[1] * v2[1]
    norm1 = math.sqrt((v1[0]**2)+(v1[1]**2))
    norm2 = math.sqrt((v2[0]**2)+(v2[1]**2))
    return math.acos(product / (norm1 * norm2))

def go_to_goal(coords, team, hiker, c):
    dic = c.get_data()
    hiker_loc = [dic[team][hiker]["x"],dic[team][hiker]["y"]]
    distancia = math.sqrt(((hiker_loc[0]-coords[0])**2)+(hiker_loc[1]-coords[1])**2)
    angulo = ang(hiker_loc, coords)
    pasos = int(distancia//MAX_SPEED)
    for paso in range(pasos):
        while (not c.next_iteration(team,{hiker:{'direction':angulo,'speed':MAX_SPEED}})):
            continue
        

def lagrange_walk(team:str,hiker:str,d_inicial:float,ray_number:int, c):
    direccion = d_inicial
    maximos = []
    
    for rayo in range(ray_number):
        puntos = [[],[]]
        angulo = rayo * (math.pi/4)/ray_number
        for punto in range(CANTIDAD_DE_PUNTOS):
            for i in range(100):
                while (not c.next_iteration(team,{hiker:{'direction':direccion,'speed':MAX_SPEED}})):
                    continue
            dic = c.get_data()
            puntos[0].append(dic[team][hiker]["x"]/math.cos(angulo))
            puntos[1].append(dic[team][hiker]["z"])
        while (not c.next_iteration(team,{hiker:{'direction':direccion+(math.pi/2),'speed':MAX_SPEED}})):
            continue
        direccion += rayo * (math.pi/4)/ray_number
        maximos.append(Lagrange.estimate_max_height(puntos))
        
    return maximos
    
def __main__():
    team = "Los cracks"
    hikers = []
    c = MountainClient()
    c.add_team(team, ["Santi"])
    c.finish_registration()
    
    dic = c.get_data()
    direction = -0.78539
    print(direction)
    
    while dic["Los cracks"]["Santi"]["x"] != 0 and dic[team]["Santi"]["y"] != 0:
        while (not c.next_iteration(team,{"Santi":{'direction':direction,'speed':MAX_SPEED}})):
                continue
        dic = c.get_data()
    print("llegue")
    rayos_max=10
    maximos = lagrange_walk(team,"Santi",math.pi,rayos_max, c)
    max = 0
    x = 0
    index= -1
    for z in range(len(maximos)):
        if maximos[z][1]>max:
            x = maximos[z][0]
            max_z = maximos[z][1]
            index = z
    angulo = index*(math.pi/4)/rayos_max
    coordenadas = [x * math.cos(angulo), x * math.sin(angulo)]
    print(coordenadas)
    go_to_goal(coordenadas, team, "Santi", c)
        
if __name__ == "__main__":
    __main__()