from scipy.interpolate import lagrange
import numpy as np
import matplotlib.pyplot as plt
RADIO_MONTANA = 23000

def estimate_max_height(points):
    x = [point[0] for point in points]
    z = [point[1] for point in points]
    
    # Estimar la curva utilizando la interpolación de Lagrange
    poly = lagrange(x, z)
    
    # Encontrar el valor máximo de z en el rango de x
    x_new = np.linspace(-RADIO_MONTANA, RADIO_MONTANA, num=1000)
    z_new = poly(x_new)
    index_max = np.argmax(z_new)
    x_max = x_new[index_max]
    max_height = max(z_new)
    coordenadas = [x_max, max_height]
    return coordenadas

def estimate_max_height_v2(points, mountain_limit):
    x = [point[0] for point in points]
    z = [point[1] for point in points]
    
    # Estimate the curve using Lagrange interpolation
    n = len(x)
    poly = [0] * n
    for j in range(n):
        p = [(z[j] if k == j else z[j] / (x[j] - x[k])) for k in range(n)]
        poly = [poly[k] + p[k] for k in range(n)]
    
    # Find the maximum value of z and its corresponding x
    x_new = list(range(int(-mountain_limit), int(mountain_limit+1), 45))
    z_new = [sum(poly[k] * (x_new[i] ** (n - k - 1)) for k in range(n)) for i in range(len(x_new))]
    index_max = z_new.index(max(z_new))
    x_max = x_new[index_max]
    max_height = max(z_new)
    coordenadas = [x_max, max_height]
    
    
    x = [point[0] for point in points]
    z = [point[1] for point in points]
    plt.plot(x, z, 'ro', label='Data points')
    x_new = list(range(int(min(x)), int(max(x))+1))
    z_new = [sum(poly[k] * (x_new[i] ** (len(poly) - k - 1)) for k in range(len(poly))) for i in range(len(x_new))]
    plt.plot(x_new, z_new, label='Lagrange approximation')
    plt.xlabel('x')
    plt.ylabel('z')
    plt.legend()
    plt.show()
    
    return coordenadas