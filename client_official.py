from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
import time
from estrategias.spiral import spiral as estrategia

def main():

    c = MountainClient()

    team_name = 'Los cracks'
    jugadores = ['Gian', 'Pipe', 'Santi', 'Joaco']
    hikers = [Hiker(name, team_name, c) for name in jugadores]
    team = Team(team_name, hikers, c)
    

    print('Registrando equipo...', end='\r')

    c.add_team(team.nombre, jugadores)
    c.finish_registration()

    print('Esperando a comenzar...   ', end='\r')
    while c.is_registering_teams():
        time.sleep(0.01)
        continue

    print('Haciendo estrategia              ')
    estrategia(team)
    while not c.is_over():
        team.move_all()

    
if __name__ == "__main__":
    main()
