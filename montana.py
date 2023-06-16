import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from communication.server.mountain.easy_mountain import EasyMountain
import numpy as np

# Crear una instancia de EasyMountain
mountain = EasyMountain(50, 23000)

# Obtener los puntos de la montaña
x = np.linspace(-23000, 23000, 100)
y = np.linspace(-23000, 23000, 100)
X, Y = np.meshgrid(x, y)
Z = mountain.get_height(X, Y)

# Find the indices of the maximum value in the Z array
max_index = np.unravel_index(np.argmax(Z), Z.shape)

# Get the corresponding X and Y values
max_x = X[max_index]
max_y = Y[max_index]
max_z = Z[max_index]

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Crear una superficie 3D a partir de los puntos
ax.plot_surface(X, Y, Z)

# Add a red line on the highest part of the mountain
ax.plot([max_x], [max_y], [max_z], marker='o', markersize=10, color='red')


# Configurar los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar la figura
plt.show()

# Print the coordinates of the highest point
print(f"The highest point is at ({max_x:.2f}, {max_y:.2f}, {max_z:.2f})")