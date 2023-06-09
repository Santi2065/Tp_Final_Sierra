from communication.client.client import MountainClient

c = MountainClient()
c.add_team('T1', ['E1', 'E2'])
c.add_team('T2', ['E1', 'E2'])
c.finish_registration()
while not c.is_over():
    print(c.get_data())
    
    # Aca hay que hacer un algoritmo que diga si tiene que moverse, a donde y lo m,ande a next iteration.
    c.next_iteration('T1',{'E1':{'direction':10,'speed':20}})
