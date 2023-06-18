from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain
from communication.server.mountain.mccormick_mountain import McCormickMountain
from communication.server.mountain.mishra_mountain import MishraBirdMountain

#s = MountainServer(EasyMountain(50, 23000), (14000, 14000), 50)
s = MountainServer(EasyMountain(50, 10000), (200, 200), 50)
s.start()