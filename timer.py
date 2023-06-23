
class Timer:
    def __init__(self) -> None:
        self.dias = 0
        self.horas = 0
        self.minutos = 0
        self.segundos = 0

    def iteracion(self): # 0.05s ficticios -> 1 segundo 

        self.segundos += 5

        if self.segundos == 60:
            self.minutos += 1
            self.segundos = 0

        if self.minutos == 60:
            self.horas += 1
            self.minutos = 0

        if self.horas == 24:
            self.dias += 1
            self.horas = 0


