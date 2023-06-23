from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
from estrategias.empinado import empinado as estrategia

def main():

    c = MountainClient()

    team_name = 'Los Pros'
    jugadores = ['Edgar', 'Roberto', 'Pepe', 'Pedro']
    hikers = [Hiker(name, team_name, c) for name in jugadores]
    
    team = Team(team_name, hikers, c)
    c.add_team(team.nombre, jugadores)
    
    while c.is_registering_teams():
        continue

    estrategia(team)
    while not c.is_over():
        team.move_all()

if __name__ == "__main__":
    main()
