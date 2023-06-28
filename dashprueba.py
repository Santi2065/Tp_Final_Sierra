import tkinter
import tkinter.messagebox
import customtkinter
import time
import os
import threading
import pyfiglet
import matplotlib
from copy import deepcopy
from PIL import Image
from test_hiker import Graficador
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from communication.client.client import MountainClient
import essential_functions as ef
#from LEADERBOARD import leader_board

# Esto lo que hace es darnos la herramienta para poder pasar de light a dark.
customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("dark-blue")


class Dashboard(customtkinter.CTk):


    """ 
    La clase crea una interfaz en tiempo real con los datos actualizados de la partida en curso.

    Argumento de entrada:
        customtkinter.Ctk: Modulo de una libereia basada en tkinter
        cliente (MountainClient): Cliente del servidor.

    Metodos:
        update_timer(): Actualiza el cronometro de la interfaz.
        colores(): Devuelve enteros en un rango de 0 al largo de la lista que contiene los colores.
        cambiar_estado_graf(): Permite una rotacion de graficos en la interfaz.
        change_team(): Permite una rotacion en los equipos sobre la lista dezplegable.
        check_cima(): Verifica si cada uno de los escaladores llego a la cima.
        animacion_ascii(): Dezpliega la animacion ascii en la interfaz.
        comienzo_anmiacion(): Inicializa la animacion ascii al mismo tiempo que se inicializa la inetrfaz.
        update_coords(): Actualiza las coordenadas (x,y,z) de cada escalador.
        start(): Permite que la interfaz se ejecute en simultaneo al servidor.
        leaderboard_general(): Devuelve una cadena ordenada ascendentemente (respecto a la altura) de todos los escaladores.
        update_data(): Actualiza en tiempo real los datos proporcionados a la interfaz.
    """





    def __init__(self, client: MountainClient):
        super().__init__()
        self.data = client.get_data()
        self.time_step = 10 # ms
        self.client = client
        self.team = list(self.data.keys())
        self.actual_team = self.team[0]
        self.hikers = list(self.data[self.actual_team].keys())
        self.hikers_cima = [False for i in self.hikers]
        
        self.coords = {}
        for team_name in self.data:
            self.coords[team_name] = {hiker: {'x': [], 'y': [], 'z': []} for hiker in self.data[team_name]}

        self.update_coords()
        self.graph = Graficador(self.coords)
        self.cima = False
        self.status = "Buscando bandera..."

        # Falta configurar !!!!
        self.altura_promedio = None
        self.altura_maxima = None
        
        # Configuracion general de la pagina.
        
        self.title("Mountain Dashboard")
        self.geometry("800x600")
        self.configure(bg_color = "#000000")

        # Lista de colores que se pueden cambiar para cada jugador.
        self.colors = [
            "#FF8080", "#FFA080", "#FFC080", "#FFDC80", "#FFFF80",
            "#D0FF80", "#A0FF80", "#80FF80", "#80FFA0", "#80FFC0",
            "#80FFDC", "#80FFFF", "#80D0FF", "#80A0FF", "#8080FF",
            "#A080FF", "#C080FF", "#DC80FF", "#FF80FF", "#FF80DC",
            "#FF80C0", "#FF80A0", "#FF8080", "#FFA080", "#FFC080"
        ]
        self.colores_id = [0, 1, 2, 3]
        
        # Interfaz: 
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # A- Se crea la animacion ascii y se configura.
        
        #self.animacion_et = customtkinter.CTkLabel(self, text = "", text_color = "#FFFFFF", font = ("Verdana", 8, "bold"), anchor = "nw")
        self.animacion_et = customtkinter.CTkLabel(self, text = "", text_color = "#FFFFFF", font = ("Monospace", 9), justify='left', anchor="w")
        self.animacion_et.place(x = 40, y = 240)
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # B- Para cada jugador del equipo, se crea un recuadro con sus respectivos datos (Nombre, posicion, altura y cima) a tiempo real.      

        self.marco_sup_izquierdo = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[0]])
        self.marco_sup_izquierdo.place(x = 10, y = 11)

        self.titulo_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = self.hikers[0], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[0]]['x'][-1]:8.1f}\n         y: {self.coords[self.actual_team][self.hikers[0]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"),   text_color = "#000000")
        self.posicion_sup_izquierdo.place(relx = 0.05, rely = 0.35, anchor = "w")

        self.altura_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Altura: {self.coords[self.actual_team][self.hikers[0]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_sup_izquierdo.place(relx = 0.05, rely = 0.55, anchor = "w")

        self.cima_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Cima: {self.hikers_cima[0]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.cima_sup_izquierdo.place(relx = 0.05, rely = 0.75, anchor = "w")

        #----------------------------------------------------------------------------------------------------------------------------------------------- 
        
        self.marco_sup_derecho = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[1]])
        self.marco_sup_derecho.place(x = 609, y = 11)

        self.titulo_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = self.hikers[1], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[1]]['x'][-1]:8.1f}\n         y: {self.coords[self.actual_team][self.hikers[1]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_sup_derecho.place(relx = 0.05, rely = 0.35, anchor = "w")

        self.altura_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Altura: {self.coords[self.actual_team][self.hikers[1]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_sup_derecho.place(relx = 0.05, rely = 0.55, anchor = "w")

        self.cima_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Cima: {self.hikers_cima[1]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.cima_sup_derecho.place(relx = 0.05, rely = 0.75, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        
        self.marco_inf_izquierdo = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[2]])
        self.marco_inf_izquierdo.place(x = 10, y = 409)

        self.titulo_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = self.hikers[2], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[2]]['x'][-1]:8.1f}\n         y: {self.coords[self.actual_team][self.hikers[2]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_inf_izquierdo.place(relx = 0.05, rely = 0.35, anchor = "w")

        self.altura_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Altura: {self.coords[self.actual_team][self.hikers[2]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_inf_izquierdo.place(relx = 0.05, rely = 0.55, anchor = "w")

        self.cima_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Cima: {self.hikers_cima[2]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.cima_inf_izquierdo.place(relx = 0.05, rely = 0.75, anchor = "w")
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        
        self.marco_inf_derecho = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[3]])
        self.marco_inf_derecho.place(x = 609, y = 409)

        self.titulo_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = self.hikers[3], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[3]]['x'][-1]:8.1f}\n         y: {self.coords[self.actual_team][self.hikers[3]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_inf_derecho.place(relx = 0.05, rely = 0.35, anchor = "w")

        self.altura_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Altura: {self.coords[self.actual_team][self.hikers[3]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_inf_derecho.place(relx = 0.05, rely = 0.55, anchor = "w")

        self.cima_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Cima: {self.hikers_cima[3]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.cima_inf_derecho.place(relx = 0.05, rely = 0.75, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # C- Se crea, guarda y configura un espacio donde va el leaderboard en la interfaz.
        
        self.leaderboard = customtkinter.CTkLabel(self, width = 200, height = 200, text = "")
        self.leaderboard.place(x = 600, y = 200) 
        self.titulo_leader = customtkinter.CTkLabel(self, text = "LEADERBOARD", text_color = "#FF80FF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_leader.place(x = 700, y = 220, anchor = "center")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # D- Se crea el primer grafico que se ve, y se configura el tamaño de cada uno de ellos.(2D, 3D, Heat Map)
        
        self.estado_grafico = "2D"
        hiker_colors = (self.colors[0],self.colors[1],self.colors[2],self.colors[3])
        self.graph.coordenadas2(self.actual_team, hiker_colors)
        self.graph.fig1.set_size_inches(4.05,3)
        self.graph.fig2.set_size_inches(4.05,3)
        self.graph.fig3.set_size_inches(4.05,3)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # E- Lugar y texto del timer al comenzar la interfaz. Ademas, se actualiza con el metodo 'update_timer()'.
        
        self.timer = customtkinter.CTkLabel(self, text = "00:00:00", text_color = "#FFFFFF", font = ("Impact", 40, "bold"), anchor = "center")
        self.timer.place(x = 400, y = 80, anchor = "center")
        self.start_time = time.time()
        self.update_timer()
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # F- Se crea en la parte inferior de la interfaz, una serie de datos que se actualizan en tiempo real. (Flag, Altura Promedio, Pico Maximo)

        self.altura_max = customtkinter.CTkLabel(self, text = f"FLAG: {self.status}", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.altura_max.place(x = 220, y = 480, anchor = "w")

        self.altura_promedio = customtkinter.CTkLabel(self, text = "ALTURA PROMEDIO: ", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.altura_promedio.place(x = 220, y = 520, anchor = "w")

        self.terminado = customtkinter.CTkLabel(self, text = "PICO MAXIMO: ", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.terminado.place(x = 220, y = 560, anchor = "w")
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # G- Se crea y configura una barra deslizadora.
        
        self.barra_deslizadora = customtkinter.CTkSlider(self, from_ = 0, to = 255, orientation = "vertical", button_length = 20, button_color = "#FFFFFF", button_corner_radius = 1)
        self.barra_deslizadora.place(x = 770, y = 200)
        self.barra_deslizadora.set(50)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # H- Se agrega para cada borde del marco de la pestaña, una barra dinamica.

        self.borde_inferior = customtkinter.CTkProgressBar(self, width = 800)
        self.borde_inferior.place(x = 0, y = 593)

        self.borde_inferior.configure(mode = "indeterminnate")
        self.borde_inferior.start()

        self.borde_superior = customtkinter.CTkProgressBar(self, width = 800)
        self.borde_superior.place(x = 0, y = 3)

        self.borde_superior.configure(mode = "indeterminnate")
        self.borde_superior.start()

        self.borde_izquierdo = customtkinter.CTkProgressBar(self, height = 600, orientation = "vertical")
        self.borde_izquierdo.place(x = 0, y = 3)

        self.borde_izquierdo.configure(mode = "indeterminnate")
        self.borde_izquierdo.start()

        self.borde_derecho = customtkinter.CTkProgressBar(self, height = 600, orientation = "vertical")
        self.borde_derecho.place(x = 793, y = 3)

        self.borde_derecho.configure(mode = "indeterminnate")
        self.borde_derecho.start()
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # I- Se define una lista desplgable en la parte superior de la interfaz, que permite seleccionar el equipo para cambiar los datos mostrados.

        self.teams = customtkinter.CTkComboBox(self, values = self.team, command = self.change_team)
        self.teams.place(x = 350, y = 14)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # J- Para cada recuadro del jugador, se le crea un boton que permite cambiar el color de su respectivo recuadro. 

        self.boton_colores1 = customtkinter.CTkButton(self.marco_sup_izquierdo, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(0))
        self.boton_colores1.place(x = 160, y = 160)

        self.boton_colores2 = customtkinter.CTkButton(self.marco_sup_derecho, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(1))
        self.boton_colores2.place(x = 160, y = 160)

        self.boton_colores3 = customtkinter.CTkButton(self.marco_inf_izquierdo, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(2))
        self.boton_colores3.place(x = 160, y = 160)

        self.boton_colores4 = customtkinter.CTkButton(self.marco_inf_derecho, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(3))
        self.boton_colores4.place(x = 160, y = 160)
    
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # K- Se crean 3 botones para poder elegir el grafico que se ve.

        self.cambiador2d = customtkinter.CTkButton(self, height = 30, width = 40, corner_radius = 5, text = "Grafico 2D", fg_color = "#181818", font = ("Verdana", 11, "bold"), command = lambda : self.cambiar_estado_graf("2D"))
        self.cambiador2d.place(x = 288, y = 110)

        self.cambiador3d = customtkinter.CTkButton(self, height = 30, width = 40, corner_radius = 5, text = "Grafico 3D", fg_color = "#181818", font = ("Verdana", 11, "bold"), command = lambda : self.cambiar_estado_graf("3D"))
        self.cambiador3d.place(x = 372, y = 110)

        self.cambiadorheat = customtkinter.CTkButton(self, height = 30, width = 40, corner_radius = 5, text = "Heat Map", fg_color = "#181818", font = ("Verdana", 11, "bold"), command = lambda : self.cambiar_estado_graf("Heat"))
        self.cambiadorheat.place(x = 458, y = 110)
        
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def update_timer(self)->None:
        """ 
        Crea un temporizador que arranca en 00:00:00 (horas,minutos,segundos) e incrementa de a 1 segundo. 
        Permite actualizar en tiempo real el temporizador de la interfaz.
        """
        if self.cima is True:
            self.status = "Encontrada"
            return
        tiempo_transcurrido = int(time.time() - self.start_time)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        string_tiempo = f"{horas:02d} : {minutos:02d} : {segundos:02d}"
        self.timer.configure(text = f"TIMER = {string_tiempo}")
        self.timer.after(1000, self.update_timer)

    #----------------------------------------------------------------------------------------------------------------------------------------------------
    def colores(self, numero:int)->None:
        """
        Incrementa de a 1 unidad el valor ingresado. en caso de que el numero sea mayor al largo de la lista, comenzara el
        ciclo nuevamente desde 0. Permite configurar aspectos esteticos de la interfaz. 

        Argumento de entrada:
            numero (entero): numero inicial al cual se le ira sumando.
        """

        self.colores_id[numero] += 1
        self.colores_id[numero] = self.colores_id[numero] % len(self.colors)

        self.marco_sup_izquierdo.configure(fg_color = self.colors[self.colores_id[0]])
        self.marco_sup_derecho.configure(fg_color = self.colors[self.colores_id[1]])
        self.marco_inf_izquierdo.configure(fg_color = self.colors[self.colores_id[2]])
        self.marco_inf_derecho.configure(fg_color = self.colors[self.colores_id[3]])
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def cambiar_estado_graf(self, modo: str):
        """
        Cambia el estado del grafico de la interfaz.

        Argumento de entrada:
            modo (cadena): Inidica el nuevo estado del grafico.
        """
        self.estado_grafico = modo
        print(f"me cambie a {modo}")
        
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    def change_team(self, value:str)->None:
        """
        Permite modificar la lista dezplegable para mostrar en la interfaz los valores del equipo ingresado.

        Argumento de entrada:
            value (cadena): nombre del equipo seleccionado.
        """
        info = deepcopy(self.data)
        self.actual_team = value
        self.hikers = list(info[self.actual_team].keys())
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    def check_cima(self)->None:
        """
        Verifica si cada escalador esta en la cima. 
        """

        all_cima = True
        for idx, hiker in enumerate(self.hikers):
            self.hikers_cima[idx] = self.data[self.actual_team][hiker]['cima']
            if not self.hikers_cima[idx]:
                all_cima = False
        self.cima = all_cima
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def generar_ascii(self)->None:
        """
        Formatea y prepara la animacion ascii para poder dezplegarla en la interfaz.
        """
        b = "" # "\033[31m"
        e = "" # "\033[0m"
        animacion = [
f' __{e}\n ║║{b}▄▄██▄▄    ▄▄██ {e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}▀▀    ▀▀██▀▀  {e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}    ▄▄██▄▄    ▄▄{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}██▀▀    ▀▀██▀▀{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}▄▄    ▄▄██▄▄   {e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}▀▀██▀▀    ▀▀██{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}██▄▄    ▄▄██▄▄ {e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}████████████{e}\n ║║{b}    ▀▀██▀▀    ▀▀{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n'
]
        animacion2 = [
f' __{e}\n ║║{b}▄▄██▄▄    ▄▄██▄▄{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}▀▀  ▀▀████▀▀  ▀▀{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}  ▄▄██▄▄    ▄▄██{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}██▀▀  ▀▀████▀▀  {e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}    ▄▄██▄▄    ▄▄{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████▀▀  ▀▀████▀▀{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}▄▄    ▄▄██▄▄    {e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}  ▀▀██▀▀  ▀▀████{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
f' __{e}\n ║║{b}██▄▄    ▄▄██▄▄  {e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}████████████████{e}\n ║║{b}▀▀  ▀▀██▀▀  ▀▀██{e}\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n'
]
        '''animacion = [
            "    O\n   /|\\\n    |\n   / \\",
            "   \\O/\n    |\n   /|\\\n   / \\",
            "    |\\\n   \\O/\n   /|\\\n   / \\",
            "   / \\\n    |\\\n   \\O/\n   /|\\",
        ]'''
        return animacion
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def animacion_ascii(self)->None:
        """
        Actualiza la animacion ascii en la interfaz para lograr el efecto de dinamismo.
        """

        animacion_generada = self.generar_ascii()

        while True:
            for frame in animacion_generada:
                self.animacion_et.configure(text = frame)
                self.update_idletasks()
                time.sleep(0.5) 
    #----------------------------------------------------------------------------------------------------------------------------------------------------


    def comienzo_animacion(self)-> None:
        """
        Inicializa la animacion ascii en un hilo separado. 
        """
        threading.Thread(target = self.animacion_ascii).start()

    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def update_coords(self) -> None:
        """
        Actualiza las coordenadas (x,y,z) de cada escalador por iteracion.
        """

        for team_name in self.coords:
            for hiker in self.coords[team_name]:
                self.coords[team_name][hiker]['x'] += [self.data[team_name][hiker]['x']]
                self.coords[team_name][hiker]['y'] += [self.data[team_name][hiker]['y']]
                self.coords[team_name][hiker]['z'] += [self.data[team_name][hiker]['z']]
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def start(self)-> None:
        """
        Inicializa el server en simultaneo al dasboard.
        """

        # No modificar
        t = threading.Thread(target=self.update_data)
        t.start()
        self.mainloop()  

    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def leaderboard_general(self, diccionario:dict)->str:
        """
        Cadena de jugadores ordenados por altura.
        
        Argumento de entrada:
            diccionario: Diccionario que contiene los datos de todos los jugadores.

        Salida:
            cadena con los jugadores ordenados ascendentemente respecto a su altura.
        """

        jugadores_ordenados = []
        for equipo, jugadores in diccionario.items():
            for jugador, variables in jugadores.items():
                altura = variables.get("z", 0)
                jugadores_ordenados.append((equipo, jugador, altura))

        """Insertion sort"""
        n = len(jugadores_ordenados)
        for i in range(1, n):
            actual = jugadores_ordenados[i]
            j = i - 1
            while j >= 0 and actual[2] > jugadores_ordenados[j][2]:
                jugadores_ordenados[j + 1] = jugadores_ordenados[j]
                j -= 1
            jugadores_ordenados[j + 1] = actual

        lista_ordenada = []
        for idx, player in enumerate(jugadores_ordenados, 1):
            lista_ordenada.append(f"{idx}- {player[1]} de {player[0]}")

        return "\n".join(lista_ordenada)
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    
    def clear_canvas(canvas: FigureCanvasTkAgg):
        pass
    
    def update_data(self)-> None:
        """
        Actualiza al instante los datos suministrados en la interfaz.
        """
        grafico_heat = FigureCanvasTkAgg(self.graph.fig2, master = self)
        grafico_2d = FigureCanvasTkAgg(self.graph.fig1, master = self)
        grafico_3d = FigureCanvasTkAgg(self.graph.fig3, master = self)

        grafico_heat_2 = FigureCanvasTkAgg(self.graph.fig2, master = self)
        grafico_2d_2 = FigureCanvasTkAgg(self.graph.fig1, master = self)
        grafico_3d_2 = FigureCanvasTkAgg(self.graph.fig3, master = self)

        # No modificar
        i = 0
        while not self.client.is_over():
            self.data = self.client.get_data()
            self.check_cima()
            time.sleep(self.time_step/1000)
            #self.graph.ax.cla()
            hiker_colors = (self.colors[self.colores_id[3]], self.colors[self.colores_id[2]],
                            self.colors[self.colores_id[1]], self.colors[self.colores_id[0]])
            
            '''self.grafico_2d.get_tk_widget().delete()
            self.grafico_3d.get_tk_widget().delete()
            self.grafico_heat.get_tk_widget().delete()'''
            

            if self.estado_grafico == "2D":
                self.graph.coordenadas2(self.actual_team, hiker_colors)
                if i % 2 == 0:
                    grafico_2d.draw()
                    grafico_2d.get_tk_widget().place(x=201, y=150)
                    time.sleep(0.01)
                    grafico_2d_2 = FigureCanvasTkAgg(self.graph.fig1,master = self)
                else:
                    grafico_2d_2.draw()
                    grafico_2d_2.get_tk_widget().place(x=201, y=150)
                    time.sleep(0.01)
                    grafico_2d = FigureCanvasTkAgg(self.graph.fig1, master = self)

            elif self.estado_grafico == "3D":
                grafico_3d = FigureCanvasTkAgg(self.graph.fig3, master = self)

                self.graph.graf_3d(self.actual_team)
                grafico_3d.draw()
                grafico_3d.get_tk_widget().place(x=201, y=150)


            elif self.estado_grafico == "Heat":
                grafico_heat = FigureCanvasTkAgg(self.graph.fig2, master = self)

                self.graph.heat_map()
                time.sleep(0.01)
                grafico_heat.draw()
                grafico_heat.get_tk_widget().place(x=201, y=150)

            i += 1

            self.update_coords()
            #self.altura_maxima = ef.altura_maxima(self.actual_team,diccionario,lista_max)
            #self.altura_promedio = ef.altura_promedio(diccionario,self.actual_team)
            self.leaderboard.configure(text = self.leaderboard_general(self.data))


            '''self.titulo_sup_izquierdo.configure(text = self.hikers[0])
            self.posicion_sup_izquierdo.configure(text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[0]]['x'][-1]:8.1f}\n               y: {self.coords[self.actual_team][self.hikers[0]]['y'][-1]:8.1f}")
            self.altura_sup_izquierdo.configure(text = f"Altura: {self.coords[self.actual_team][self.hikers[0]]['z'][-1]:8.1f}")
            self.cima_sup_izquierdo.configure(text = f"Cima: {self.hikers_cima[0]}")

            self.titulo_sup_derecho.configure(text = self.hikers[1])
            self.posicion_sup_derecho.configure(text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[1]]['x'][-1]:8.1f}\n               y: {self.coords[self.actual_team][self.hikers[1]]['y'][-1]:8.1f}")
            self.altura_sup_derecho.configure(text = f"Altura: {self.coords[self.actual_team][self.hikers[1]]['z'][-1]:8.1f}")
            self.cima_sup_derecho.configure(text = f"Cima: {self.hikers_cima[1]}")
            
            self.titulo_inf_izquierdo.configure(text = self.hikers[2])
            self.posicion_inf_izquierdo.configure(text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[2]]['x'][-1]:8.1f}\n               y: {self.coords[self.actual_team][self.hikers[2]]['y'][-1]:8.1f}")
            self.altura_inf_izquierdo.configure(text = f"Altura: {self.coords[self.actual_team][self.hikers[2]]['z'][-1]:8.1f}")
            self.cima_inf_izquierdo.configure(text = f"Cima: {self.hikers_cima[2]}")

            self.titulo_inf_derecho.configure(text = self.hikers[3])
            self.posicion_inf_derecho.configure(text = f"Posicion: x: {self.coords[self.actual_team][self.hikers[3]]['x'][-1]:8.1f}\n               y: {self.coords[self.actual_team][self.hikers[3]]['y'][-1]:8.1f}")
            self.altura_inf_derecho.configure(text = f"Altura: {self.coords[self.actual_team][self.hikers[3]]['z'][-1]:8.1f}")
            self.cima_inf_derecho.configure(text = f"Cima: {self.hikers_cima[3]}")'''


            team_name = self.actual_team
            team_data = deepcopy(self.data[team_name]) # {'nombre1': {x:[],y:[],z:[]}, ...}
            
            titulos = [self.titulo_inf_derecho, self.titulo_inf_izquierdo,
                       self.titulo_sup_derecho, self.titulo_sup_izquierdo]
            posiciones = [self.posicion_inf_derecho, self.posicion_inf_izquierdo,
                          self.posicion_sup_derecho, self.posicion_sup_izquierdo]
            alturas = [self.altura_inf_derecho, self.altura_inf_izquierdo,
                       self.altura_sup_derecho, self.altura_sup_izquierdo]
            cimas = [self.cima_inf_derecho, self.cima_inf_izquierdo,
                     self.cima_sup_derecho, self.cima_sup_izquierdo]

            for hiker, titulo, pos, altura, cima in zip(team_data, titulos, posiciones, alturas, cimas):
                titulo.configure(text = hiker)
                pos.configure(text = f"Posicion: x: {self.coords[team_name][hiker]['x'][-1]:8.1f}\n               y: {self.coords[team_name][hiker]['y'][-1]:8.1f}")
                altura.configure(text = f"Altura: {self.coords[team_name][hiker]['z'][-1]:8.1f}")
                cima.configure(text = f"Cima: {self.data[team_name][hiker]['cima']}")

            
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    client = MountainClient()
    #client = MountainClient("10.42.0.1", 8888)

    while client.is_registering_teams():
        time.sleep(0.1)

    print('Iniciando dashboard...')
    lista_max = []
    mountain_dash = Dashboard(client)
    mountain_dash.comienzo_animacion()
    mountain_dash.start()
    diccionario = client.get_data()




    #mountain_dash.leader_leader()