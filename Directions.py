from communication.client.client import MountainClient

# Crear una instancia de MountainClient
c = MountainClient()

# Agregar un equipo llamado "Los cracks" con cuatro jugadores
c.add_team('Los cracks', ['Santi', 'Pipe', 'Gian', 'Joaco'])

# Finalizar el registro del equipo
c.finish_registration()

# Mientras el juego no haya terminado
while not c.is_over():
    # Imprimir la información recibida del servidor
    print(c.get_data())
    
    # Definir las directivas para cada jugador del equipo "Los cracks"
    directives = {
        'Pipe':{'direction':10,'speed':20},
        'Santi':{'direction':10,'speed':20},
        'Joaco':{'direction':10,'speed':20},
        'Gian':{'direction':10,'speed':20}
        }
    
    # Enviar las directivas al servidor y avanzar al siguiente turno del juego
    while(not c.next_iteration('Los cracks', directives)):
        continue