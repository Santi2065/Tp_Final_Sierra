from scipy.interpolate import lagrange
import numpy as np
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