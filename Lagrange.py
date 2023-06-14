from scipy.interpolate import lagrange
RADIO_MONTANA = 23000

def estimate_max_height(points):
    x = [point[0] for point in points]
    z = [point[1] for point in points]
    
    # Estimar la curva utilizando la interpolación de Lagrange
    poly = lagrange(x, z)
    
    # Encontrar el valor máximo de z en el rango de x
    x_new = np.linspace(-RADIO_MONTANA, RADIO_MONTANA, num=1000)
    z_new = poly(x_new)
    max_height = max(z_new)
    index = z_new.index(max_height)
    coordenadas = (x_new[index], max_height, index)
    return coordenadas