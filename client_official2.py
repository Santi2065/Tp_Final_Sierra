from communication.client.client import MountainClient
from HIKERS import Hiker
from teams import Team
import time
from estrategias.empinado import empinado as estrategia

def main():

    c = MountainClient()

    team_name = 'Los Pros'
    jugadores = ['Edgar', 'Roberto', 'Pepe', 'Pedro']
    hikers = [Hiker(name, team_name, c) for name in jugadores]
    team = Team(team_name, hikers, c)
    

    print('Registrando equipo...')

    c.add_team(team.nombre, jugadores)

    print('Esperando a comenzar...', end='\r')
    while c.is_registering_teams():
        time.sleep(0.1)
        continue

    print('Haciendo estrategia              ')
    estrategia(team)
    while not c.is_over():
        team.move_all()


if __name__ == "__main__":
    main()
