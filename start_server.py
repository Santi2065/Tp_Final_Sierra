from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain
from communication.server.mountain.mccormick_mountain import McCormickMountain
from communication.server.mountain.mishra_mountain import MishraBirdMountain
from communication.server.mountain.rastrigin_mountain import RastriginMountain
from communication.server.mountain.sinosidal_mountain import SinosidalMountain
from communication.server.mountain.ackley_mountain import AckleyMountain
from communication.server.mountain.easom_mountain import EasomMountain

#s = MountainServer(EasyMountain(50, 23000), (-10000, 14000), 50)
s = MountainServer(EasomMountain(50, 10000), (0, 0), 50)
s.start()