colores = ["#FF0000", "#0000FF", "#FFFF00", "#00FF00", "#FFA500", "#FFC0CB", "#800080", "#00FFFF"]

numero = [0]
def colores(numero:list):
    """Starts returning 1, increases it value 1 by 1 in range 0 to 7."""
    numero[0] += 1
    numero[0] = numero[0] % 8
    return (numero[0])


