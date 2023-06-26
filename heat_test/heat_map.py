import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from sample_data import samples

fig, ax = plt.subplots()
ax.set_title("Map shape")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')

data = samples(7)

z_max = float('-inf')
z_min = float('inf')
points = []
'''for name in data:
    for i in range(len(data[name]['x'])):
        x = data[name]['x'][i]
        y = data[name]['y'][i]
        z = data[name]['z'][i]
        points += [[x, y, z]]
        
        z_max = z if z > z_max else z_max
        z_min = z if z < z_min else z_min'''

lx, ly, lz = [], [], []
for name in data:
    lx += data[name]['x']
    ly += data[name]['y']
    lz += data[name]['z']

    z = data[name]['z']
    z_max = max(z) if max(z) > z_max else z_max
    z_min = min(z) if min(z) < z_min else z_min


#df= pd.DataFrame(points, columns=list('XYZ'))

#tpc = ax.tripcolor(df["X"], df["Y"], df["Z"], shading='flat', cmap='hot', clim=[z_min, z_max])
#tpc = ax.tripcolor(df["X"], df["Y"], df["Z"], shading='gouraud', cmap='hot', clim=[z_min, z_max])
#print(f'len lx: {len(lx)}')
tpc = ax.tripcolor(lx, ly, lz, shading='gouraud', cmap='hot', clim=[z_min, z_max])
colorbar = fig.colorbar(tpc)
colorbar.ax.set_ylim(z_min, z_max)
colorbar.ax.set_title('height', fontsize=9)


plt.show()

