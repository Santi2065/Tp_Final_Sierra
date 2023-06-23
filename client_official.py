from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
from estrategias.empinado import empinado as estrategia

def main():

    c = MountainClient()

    team_name = 'Los cracks'
    jugador_1 = Hiker('Gian', c)
    jugador_2 = Hiker('Pipe', c)
    jugador_3 = Hiker('Santi', c)
    jugador_4 = Hiker('Joaco', c)
    hikers = [jugador_1,jugador_2,jugador_3,jugador_4]
    hikers_names = [jugador_1.nombre,jugador_2.nombre,jugador_3.nombre,jugador_4.nombre]
    team = Team(team_name,hikers,c)
    
    c.add_team(team.nombre, hikers_names)
    c.finish_registration()
    while c.is_registering_teams():
        continue

    estrategia(team)

    
if __name__ == "__main__":
    main()
