from communication.client.client import MountainClient
from tpf_Montana_hikers import Hiker
from tpf_Montana_teams import Team
import argparse
import time
from tpf_Montana_spiral import spiral as estrategia

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help = "ingrese el ip con el puerto ej:192.168.1.1:8080", type = str)
    args = parser.parse_args()

    if args.ip:
        ip, puerto = args.ip.split(":")
        try:
            c = MountainClient(ip, int(puerto))
            c.get_data()
            print('Se establecio correctamente una conexion con el servidor.')
        except:
            print("No se pudo establecer conexion con el servidor, intente de nuevo")
            exit()
    else:
        try:
            c = MountainClient()
            c.get_data()
            print('Se establecio correctamente una conexion con el servidor local.')
        except:
            print("No se pudo establecer una conexion con el servidor local, intente de nuevo")
            exit()

    team_name = 'Los finos'
    names = ['♥', '♦', '♣', '♠']
    hikers = [Hiker(name, team_name, c) for name in names]
    team = Team(team_name, hikers, c)
    

    print('Registrando equipo...', end='\r')

    c.add_team(team.nombre, names)
    c.finish_registration()

    print('Esperando a comenzar...', end='\r')
    while c.is_registering_teams():
        time.sleep(0.01)
        continue

    print('Haciendo estrategia     ')
    estrategia(team)


if __name__ == "__main__":
    main()
