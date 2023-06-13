from communication.client.client import MountainClient

c = MountainClient()
c.add_team('Los cracks', ['Santi', 'Pipe', 'Gian', 'Joaco'])
c.finish_registration()

while not c.is_over():
    print(c.get_data())
    
    directives = {
        'Pipe':{'direction':10,'speed':20},
        'Santi':{'direction':10,'speed':20},
        'Joaco':{'direction':10,'speed':20},
        'Gian':{'direction':10,'speed':20}
        }
    while(not c.next_iteration('Los cracks', directives)):
        continue
        
