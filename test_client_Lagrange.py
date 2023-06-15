from communication.client.client import MountainClient
import math
import Lagrange
CANTIDAD_DE_PUNTOS = 150
MAX_SPEED = 50

def ang(hiker: list, flag: list):
    dx = flag[0] - hiker[0]
    dy = flag[1] - hiker[1]
    return math.atan2(dy, dx)

def go_to_goal(coords, team, hiker, c):
    dic = c.get_data()
    hiker_loc = [dic[team][hiker]["x"],dic[team][hiker]["y"]]
    distancia = math.sqrt(((hiker_loc[0]-coords[0])**2)+(hiker_loc[1]-coords[1])**2)
    angulo = ang(hiker_loc, coords)
    pasos = int(distancia//MAX_SPEED)
    for paso in range(pasos):
        while (not c.next_iteration(team,{hiker:{'direction':angulo,'speed':MAX_SPEED}})):
            continue
        

def lagrange_walk(team:str,hiker:list,ray_number:int, c):
    direccion = 0
    maximos = []
    
    for rayo in range(ray_number):
        puntos = [[],[]]
        angulo = rayo * (math.pi/4)/ray_number
        dic = {}
        for player in hiker:
            dic[player]={'direction':direccion,'speed':MAX_SPEED}
            direccion += math.pi/4
        for player in hiker:
            for punto in range(CANTIDAD_DE_PUNTOS):
                for i in range(50):
                    while (not c.next_iteration(team,dic)):
                        continue
                dic = c.get_data()
                mountain_limit = int(25000/math.cos(angulo))
                puntos[0].append(dic[team][player]["x"]/math.cos(angulo))
                puntos[1].append(dic[team][player]["z"])
            maximos.append(Lagrange.estimate_max_height_v2(puntos,500000))
            #aca deje la expancion para meter mas hikers
            for player in hiker:
                direccion += (math.pi/4)/rayo
                dic[player]={'direction':direccion,'speed':MAX_SPEED}
        while (not c.next_iteration(team,{hiker:{'direction':direccion+(math.pi/2),'speed':MAX_SPEED}})):
            continue
        direccion += rayo * (math.pi/4)/ray_number
        maximos.append(Lagrange.estimate_max_height_v2(puntos,500000))
        
    return maximos
    
def __main__():
    team = "Los cracks"
    hikers = ["Santi","Pipe","Joaco","Gian"]
    c = MountainClient()
    c.add_team(team, hikers)
    c.finish_registration()
    
    #dic = c.get_data()
    #direction = ang([dic["Los cracks"]["Santi"]["x"],dic["Los cracks"]["Santi"]["y"]],[0,0] )
    #print(direction)
    #
    #while not -10 < dic["Los cracks"]["Santi"]["x"] < 10 and  not -10 < dic[team]["Santi"]["y"] < 10:
    #    while (not c.next_iteration(team,{"Santi":{'direction':direction,'speed':MAX_SPEED}})):
    #            continue
    #    dic = c.get_data()
    #print("llegue")
    rayos_max=10
    maximos = lagrange_walk(team,hikers,rayos_max, c)
    max = 0
    x = 0
    index= -1
    print(maximos)
    for z in range(len(maximos)):
        if maximos[z][1]>max:
            x = maximos[z][0]
            max_z = maximos[z][1]
            index = z
    angulo = index*(math.pi/4)/rayos_max
    print(f"{max_z},{x}")
    coordenadas = [x * math.cos(angulo), x * math.sin(angulo)]
    print(coordenadas)
    go_to_goal(coordenadas, team, "Santi", c)
        
if __name__ == "__main__":
    __main__()