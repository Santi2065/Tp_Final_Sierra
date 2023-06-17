from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team


def go_center(team,c):
    #apuntan al centro
    for hiker in team.hikers:
        hiker.go_to([0,0])

    #se mueven hasta que llegan
    llegada = {x : 0 for x in team.hikers}
    no_llegaron = True
    while no_llegaron:
        team.move_all(team.hikers,c)
        info = c.get_data()
        for hiker in team.hikers:
            x =  info[team.nombre][hiker.nombre]['x']
            y =  info[team.nombre][hiker.nombre]['y']
            if -1 < x < 1 and -1 < y < 1:
                llegada[hiker] = 1
                hiker.stay_still()
        no_llegaron = False
        for x in llegada:
            if x == 0:
                no_llegaron = True
    print("En el centro")

def start_search():
    pass

def main():

    c = MountainClient()

    team_name = 'Los cracks'
    jugador_1 = Hiker('Gian',c)
    jugador_2 = Hiker('Pipe',c)
    jugador_3 = Hiker('Santi',c)
    jugador_4 = Hiker('Joaco',c)
    hikers = [jugador_1,jugador_2,jugador_3,jugador_4]
    hikers_names = [jugador_1.nombre,jugador_2.nombre,jugador_3.nombre,jugador_4.nombre]
    team = Team(team_name,hikers,c)
    
    c.add_team(team.nombre, hikers_names)
    c.finish_registration()

    go_center(team,c)

    
if __name__ == "__main__":
    main()
