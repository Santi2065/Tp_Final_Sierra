COLORES = ["#FF0000", "#0000FF", "#FFFF00", "#00FF00", "#FFA500", "#FFC0CB", "#800080", "#00FFFF"]

def colores(numero: int):
    """Starts returning 1, increases it value 1 by 1 in range 0 to 7."""
    numero += 1
    numero = numero % 8
    return numero



