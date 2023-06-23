import tkinter
import tkinter.messagebox
import customtkinter
import time
import os
import threading
import pyfiglet
import matplotlib
from PIL import Image
from test_hiker import Grafico_2d_equipo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from communication.client.client import MountainClient
#from LEADERBOARD import leader_board

# Esto lo que hace es darnos la herramienta para poder pasar de light a dark.
customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")


# Se define una clase para poder hacer el dashboard.

class Dashboard(customtkinter.CTk):
    # Uso el constructor como se me da en la info que tengo.
    def __init__(self, client: MountainClient):
        super().__init__()
        self.time_step = 50 # ms
        self.client = client
        self.data = client.get_data()
        self.team = list(self.data.keys())
        self.hikers = list(self.data[self.team[0]].keys())
        self.hikers_cima = [False for i in self.hikers]
        self.coords = {hiker: {'x': [], 'y': [], 'z': []} for hiker in self.hikers}
        self.update_coords()
        self.graph = Grafico_2d_equipo(self.coords)
        self.cima = False
        


        # Una vez tenido eso, arranco con la configuracion de la ventana.
        # Defino el titulo.
        
        self.title("Mountain Dashboard")

        #leader = leader_board()
        # Largo y alto de la ventana.

        self.geometry("800x600")

        # Establezco el color de fondo de la ventana
        
        self.configure(bg_color = "#000000")
        # Defino la lista de colores que se pueden cambiar para cada jugador

        self.colors = ["#FFB6C1", "#FFA500", "#00FFFF", "#FF69B4", "#FFFF00", "#00FF00", "#9400D3", "#FF1493"]
        self.colores_id = [0, 1, 2, 3]
        
        # Creo marcos para las ventanas cuadradas pequeñas de las esquinas. 
        # Configuro cada una de ellas con su respectivo color y ademas les agrego su titulo.
        # Les agrego a cada uno de ellos su respectiva posicion, altura y velocidad en tiempo real
        #-----------------------------------------------------------------------------------------------------------------------------------------------      
        self.marco_sup_izquierdo = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[0]])
        self.marco_sup_izquierdo.place(x = 10, y = 11)

        self.titulo_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = self.hikers[0], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Posicion: x: {self.coords[self.hikers[0]]['x'][-1]:8.1f}\n         y: {self.coords[self.hikers[0]]['y'][-1]:8.1f}", font = ("Verdana", 12, "bold"),   text_color = "#000000")
        self.posicion_sup_izquierdo.place(relx = 0.05, rely = 0.35, anchor = "w")

        self.altura_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Altura: {self.coords[self.hikers[0]]['z'][-1]:8.1f}", font = ("Verdana", 12, "bold"), text_color = "#000000")
        self.altura_sup_izquierdo.place(relx = 0.05, rely = 0.55, anchor = "w")

        self.velocidad_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = f"Cima: {self.hikers_cima[0]}", font = ("Verdana", 12, "bold"), text_color = "#000000")
        self.velocidad_sup_izquierdo.place(relx = 0.05, rely = 0.75, anchor = "w")
        #----------------------------------------------------------------------------------------------------------------------------------------------- 
        self.marco_sup_derecho = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[1]])
        self.marco_sup_derecho.place(x = 609, y = 11)

        self.titulo_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = self.hikers[1], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Posicion: x: {self.coords[self.hikers[1]]['x'][-1]:8.1f}\n         y: {self.coords[self.hikers[1]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_sup_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Altura: {self.coords[self.hikers[1]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_sup_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = f"Cima: {self.hikers_cima[1]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.velocidad_sup_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_izquierdo = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[2]])
        self.marco_inf_izquierdo.place(x = 10, y = 409)

        self.titulo_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = self.hikers[2], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Posicion: x: {self.coords[self.hikers[2]]['x'][-1]:8.1f}\n         y: {self.coords[self.hikers[2]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_inf_izquierdo.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Altura: {self.coords[self.hikers[2]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_inf_izquierdo.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = f"Cima: {self.hikers_cima[2]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.velocidad_inf_izquierdo.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_derecho = customtkinter.CTkFrame(self, width = 185, height = 185, corner_radius = 10, fg_color = self.colors[self.colores_id[3]])
        self.marco_inf_derecho.place(x = 609, y = 409)

        self.titulo_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = self.hikers[3], text_color = "#000000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Posicion: x: {self.coords[self.hikers[3]]['x'][-1]:8.1f}\n         y: {self.coords[self.hikers[3]]['y'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.posicion_inf_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Altura: {self.coords[self.hikers[3]]['z'][-1]:8.1f}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.altura_inf_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = f"Cima: {self.hikers_cima[3]}", font = ("Verdana", 14, "bold"), text_color = "#000000")
        self.velocidad_inf_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Creo el rectangulo del medio donde iran los graficos

        #self.rectangulo_fondo = customtkinter.CTkLabel(self, width = 400, height = 300, bg_color = "#111111")
        #self.rectangulo_fondo.place(x = 200, y = 150)
        self.graph.coordenadas2()
        self.graph.fig.set_size_inches(4.05,3)
        
        self.mountain_image = FigureCanvasTkAgg(self.graph.fig,master = self)
        #self.mountain_image_label = customtkinter.CTkLabel(self.rectangulo, image = self.mountain_image, text = "")
        #self.mountain_image_label.place(relx = 0.5, rely = 0.5, anchor = "center")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Creo un timer que se va a ubicar en la parte superior del rectangulo.

        self.timer = customtkinter.CTkLabel(self, text = "00:00:00", text_color = "#FFFFFF", font = ("Impact", 40, "bold"), anchor = "center")
        self.timer.place(x = 400, y = 80, anchor = "center")
        self.start_time = time.time()
        self.update_timer()

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Debajo del rectangulo, agrego mas datos a tiempo real.

        self.altura_max = customtkinter.CTkLabel(self, text = "FLAG: ", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.altura_max.place(x = 220, y = 480, anchor = "w")

        self.altura_promedio = customtkinter.CTkLabel(self, text = "ALTURA PROMEDIO: ", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.altura_promedio.place(x = 220, y = 520, anchor = "w")

        self.terminado = customtkinter.CTkLabel(self, text = "PICO MAXIMO: ", text_color = "#FFFFFF", font = ("Verdana", 16, "bold"), anchor = "center")
        self.terminado.place(x = 220, y = 560, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Coloco un cartel del estado del server.

        self.estado = customtkinter.CTkLabel(self, text = "STATUS: ", text_color = "#FFFFFF", font = ("Impact", 20, "bold"), anchor = "center")
        self.estado.place(x = 425, y = 123, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Agrego una etiqueta entre los cuadrantes de la izquierda donde habra una animacion ascii

        self.animacion_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111", text = "")
        self.animacion_fondo.place(x = 0, y = 200)

        self.animacion_et = customtkinter.CTkLabel(self.animacion_fondo, text = "", text_color = "#FFFFFF", font = ("Verdana", 12, "bold"), anchor = "nw")
        self.animacion_et.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        #self.leaderboard_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111", text = "")
        #self.leaderboard_fondo.place(x = 609, y = 200)

        #self.leaderboard = customtkinter.CTkLabel(self.leaderboard_fondo, text = "", text_color = "FFFFFF", font = ("Verdana", 12, "bold"), anchor = "nw")
        #self.leaderboard.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        #self.leaderboard.configure(text = self.generar_leader())
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Barra deslizadora
        self.brillo_slider = customtkinter.CTkSlider(self, from_ = 0, to = 255, orientation = "vertical", button_length = 20, button_color = "#FFFFFF", button_corner_radius = 1)
        self.brillo_slider.place(x = 780, y = 200)
        self.brillo_slider.set(50)

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Hago los bordes modernos

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

        self.teams = customtkinter.CTkComboBox(self, values=["pipe1", "pipe2",])
        self.teams.place(x = 350, y = 14)

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.boton_colores1 = customtkinter.CTkButton(self.marco_sup_izquierdo, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(0))
        self.boton_colores1.place(x = 160, y = 160)

        self.boton_colores2 = customtkinter.CTkButton(self.marco_sup_derecho, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(1))
        self.boton_colores2.place(x = 160, y = 160)

        self.boton_colores3 = customtkinter.CTkButton(self.marco_inf_izquierdo, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(2))
        self.boton_colores3.place(x = 160, y = 160)

        self.boton_colores4 = customtkinter.CTkButton(self.marco_inf_derecho, height = 20, width = 20, corner_radius = 5, text = "", fg_color = "#000000", command = lambda : self.colores(3))
        self.boton_colores4.place(x = 160, y = 160)
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Defino un metodo que permite actualizar el timer y comenzar cada vez que se abre la ventana
    # Ademas import el modulo time para poder hacerlo.
    def update_timer(self):
        if self.cima is True:
            return
        tiempo_transcurrido = int(time.time() - self.start_time)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        string_tiempo = f"{horas:02d} : {minutos:02d} : {segundos:02d}"
        self.timer.configure(text = f"TIMER = {string_tiempo}")
        self.timer.after(1000, self.update_timer)

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    def colores(self, numero:int):
        """Starts returning 1, increases it value 1 by 1 in range 0 to 7."""
        self.colores_id[numero] += 1
        self.colores_id[numero] = self.colores_id[numero] % 8
        self.marco_sup_izquierdo.configure(fg_color = self.colors[self.colores_id[0]])
        self.marco_sup_derecho.configure(fg_color = self.colors[self.colores_id[1]])
        self.marco_inf_izquierdo.configure(fg_color = self.colors[self.colores_id[2]])
        self.marco_inf_derecho.configure(fg_color = self.colors[self.colores_id[3]])

    #-----------------------------------------------------------------------------------------------------------------------------------------------
    def check_cima(self):
        all_cima = True
        for idx,hiker in enumerate(self.hikers):
            self.hikers_cima[idx] = self.data[self.team[0]][hiker]['cima']
            if not self.hikers_cima[idx]:
                all_cima = False
        self.cima = all_cima
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Defino un metodo que permite hacer una animacion ascii en el costado izquierdo.
    # Import el modulo threading y art, ademas de tambien utilizar el modulo time.
    def generar_ascii(self):
        '''animacion = [
' __\n ║║▄▄▄███▄▄▄   ▄▄▄███\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║▀▀▀   ▀▀▀███▀▀▀   \n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
' __\n ║║   ▄▄▄███▄▄▄   ▄▄▄\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║███▀▀▀   ▀▀▀███▀▀▀\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
' __\n ║║▄▄▄   ▄▄▄███▄▄▄   \n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║▀▀▀███▀▀▀   ▀▀▀███\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n',
' __\n ║║███▄▄▄   ▄▄▄███▄▄▄\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║██████████████████\n ║║   ▀▀▀███▀▀▀   ▀▀▀\n ║║\n ║║\n ║║\n ║║\n ║║\n####\n'
]'''

        animacion = [
            "    O\n   /|\\\n    |\n   / \\",
            "   \\O/\n    |\n   /|\\\n   / \\",
            "    |\\\n   \\O/\n   /|\\\n   / \\",
            "   / \\\n    |\\\n   \\O/\n   /|\\",
        ]
        animacion_generada = [pyfiglet.figlet_format(frame, font = "small") for frame in animacion]
        return animacion_generada
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    def animacion_ascii(self):
        animacion_generada = self.generar_ascii()

        while True:
            for frame in animacion_generada:
                self.animacion_et.configure(text = frame)
                self.update_idletasks()
                time.sleep(0.5) 
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # Este metodo inicializara la animacion en un hilo separado, es decir al mismo tiempo que otro programa.
    # Modulo threading
    def comienzo_animacion(self):
        threading.Thread(target = self.animacion_ascii).start()

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    '''def generar_leader(self):
        leader = leader_board().graficar()
        self.leaderboard.configure(text = leader)
        pass'''

    def update_coords(self) -> None:
        #coords = {nombre1: {'x': [], 'y': [], 'z': []}}
        
        for hiker in self.hikers:
            self.coords[hiker]['x'] += [self.data[self.team[0]][hiker]['x']]
            self.coords[hiker]['y'] += [self.data[self.team[0]][hiker]['y']]
            self.coords[hiker]['z'] += [self.data[self.team[0]][hiker]['z']]
        
    def start(self):
        # No modificar
        t = threading.Thread(target=self.update_data)
        t.start()
        self.mainloop()  

    def update_data(self):
        # No modificar
        while not self.client.is_over():
            self.data = self.client.get_data()
            self.check_cima()
            time.sleep(self.time_step/1000)
            #self.graph.ax.cla()
            self.graph.coordenadas2()
            self.mountain_image.draw()
            self.update_coords()
            self.mountain_image.get_tk_widget().place(x=201, y=150)
            
            self.posicion_sup_izquierdo.configure(text = f"Posicion: x: {self.coords[self.hikers[0]]['x'][-1]:8.1f}\n               y: {self.coords[self.hikers[0]]['y'][-1]:8.1f}")
            self.altura_sup_izquierdo.configure(text = f"Altura: {self.coords[self.hikers[0]]['z'][-1]:8.1f}")

            self.posicion_sup_derecho.configure(text = f"Posicion: x: {self.coords[self.hikers[1]]['x'][-1]:8.1f}\n               y: {self.coords[self.hikers[1]]['y'][-1]:8.1f}")
            self.altura_sup_derecho.configure(text = f"Altura: {self.coords[self.hikers[1]]['z'][-1]:8.1f}")
            
            self.posicion_inf_izquierdo.configure(text = f"Posicion: x: {self.coords[self.hikers[2]]['x'][-1]:8.1f}\n               y: {self.coords[self.hikers[2]]['y'][-1]:8.1f}")
            self.altura_inf_izquierdo.configure(text = f"Altura: {self.coords[self.hikers[2]]['z'][-1]:8.1f}")

            self.posicion_inf_derecho.configure(text = f"Posicion: x: {self.coords[self.hikers[3]]['x'][-1]:8.1f}\n               y: {self.coords[self.hikers[3]]['y'][-1]:8.1f}")
            self.altura_inf_derecho.configure(text = f"Altura: {self.coords[self.hikers[3]]['z'][-1]:8.1f}")


if __name__ == "__main__":
    client = MountainClient()
    mountain_dash = Dashboard(client)
    mountain_dash.comienzo_animacion()
    mountain_dash.start()




    #mountain_dash.leader_leader()