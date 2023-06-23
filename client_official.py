from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
from estrategias.spiral import spiral as estrategia

def main():

    c = MountainClient()

    team_name = 'Los cracks'
    jugadores = ['Gian', 'Pipe', 'Santi', 'Joaco']
    hikers = [Hiker(name, team_name, c) for name in jugadores]
    team = Team(team_name, hikers, c)
    
    c.add_team(team.nombre, jugadores)
    c.finish_registration()
    while c.is_registering_teams():
        continue

    estrategia(team)
    while not c.is_over():
        team.move_all()

    
if __name__ == "__main__":
    main()
