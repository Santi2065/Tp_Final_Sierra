import tkinter
import tkinter.messagebox
import customtkinter
import time
import os
import threading
import pyfiglet
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from communication.client.client import MountainClient
from tpf_Montana_graficos import Hiker

# Esto lo que hace es darnos la herramienta para poder pasar de light a dark.
customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")

#-----------------------------------------------------------------------------------------------------------------------------------------------

c = MountainClient()



class Grafico_2d_equipo: # anda, pero hay que automatizar para que funcione con los jugadores que quieras
    def __init__(self, hikers: list[Hiker]):
        self.hikers = hikers

        
        self.fig, self.ax = plt.subplots()
        self.labels = []
        #nombres = [self.hiker1.nombre,self.hiker2.nombre,self.hiker3.nombre,self.hiker4.nombre] # esto es lo de automatizar
        nombres = [hiker.nombre for hiker in hikers]
        for i in range(len(hikers)):
            label = self.ax.text(0, 0, nombres[i], ha='center', va='bottom')
            self.labels.append(label)

        self.imagen = mpimg.imread('fondo.jpeg') # Fondo del grafico 

    def coordenadas(self):
        '''co_h1 = self.hiker1.actual_pos()
        co_h2 = self.hiker2.actual_pos() # automatizar esto
        co_h3 = self.hiker3.actual_pos()
        co_h4 = self.hiker4.actual_pos()'''

        coords = [hiker.actual_pos() for hiker in self.hikers]

        x =[coord[0] for coord in coords]
        y =[coord[1] for coord in coords]

        #plt.xlim(-23000,23000)
        #plt.ylim(-23000,23000)
        size = 1500
        plt.xlim(-size, size)
        plt.ylim(-size, size)
        plt.xticks([])
        plt.yticks([])
        #self.ax.imshow(self.imagen, extent=[-23000, 23000, -23000, 23000], aspect='auto')
        self.ax.imshow(self.imagen, extent=[-size, size, -size, size], aspect='auto') # Que la imagen cunpla con los limites

        for i in range(len(x)):
            self.labels[i].set_position((x[i], y[i]))
        

        plt.scatter(x,y,c='c')
        plt.show(block=False)
        plt.pause(0.005)


c.add_team('Los cracks', ['Gian','Gian2','Gian3','Gian4'])
c.finish_registration()

directives = {'Gian':{'direction':0,'speed':50}, 'Gian2':{'direction':10,'speed':50},'Gian3':{'direction':5,'speed':50},'Gian4':{'direction':3,'speed':50}}



hikers = [] # Esta es la lista que se le pasa a la clase graficos.
hikers.append(Hiker(directives['Gian'],'Gian'))
hikers.append(Hiker(directives['Gian2'],'Gian2'))
hikers.append(Hiker(directives['Gian3'],'Gian3'))
hikers.append(Hiker(directives['Gian4'],'Gian4'))



grafico2d = Grafico_2d_equipo(hikers)


#-----------------------------------------------------------------------------------------------------------------------------------------------
# Se define una clase para poder hacer el dashboard.

class Dashboard(customtkinter.CTk):
    # Uso el constructor como se me da en la info que tengo.
    def __init__(self):
        super().__init__() 

        # Una vez tenido eso, arranco con la configuracion de la ventana.
        # Defino el titulo.
        
        self.title("Mountain Dashboard")

        # Largo y alto de la ventana.

        self.geometry("800x600")

        # Establezco el color de fondo de la ventana
        
        self.configure(bg_color = "#000000")

        # Creo marcos para las ventanas cuadradas pequeñas de las esquinas. 
        # Configuro cada una de ellas con su respectivo color y ademas les agrego su titulo.
        # Les agrego a cada uno de ellos su respectiva posicion, altura y velocidad en tiempo real
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_sup_izquierdo_borde = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#2196F3", text = "")
        self.marco_sup_izquierdo_borde.place(x = 0, y = 0)       

        self.marco_sup_izquierdo_fondo = customtkinter.CTkLabel(self, width = 195, height = 195, bg_color = "#000000")
        self.marco_sup_izquierdo_fondo.place(x = 0, y = 0)
        
        self.marco_sup_izquierdo = customtkinter.CTkFrame(self, width = 195, height = 195)
        self.marco_sup_izquierdo.place(x = 0, y = 0)

        self.titulo_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "FELIPE", text_color = "#2196F3", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Posicion: ", font = ("Verdana", 14, "bold"),   text_color = "#2196F3")
        self.posicion_sup_izquierdo.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Altura: ", font = ("Verdana", 14, "bold"), text_color = "#2196F3")
        self.altura_sup_izquierdo.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Velocidad: ", font = ("Verdana", 14, "bold"), text_color = "#2196F3")
        self.velocidad_sup_izquierdo.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_sup_derecho_borde = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#FF0000", text = "")
        self.marco_sup_derecho_borde.place(x = 600, y = 0)
        
        self.marco_sup_derecho_fondo = customtkinter.CTkLabel(self, width = 195, height = 195, bg_color = "#000000")
        self.marco_sup_derecho_fondo.place(x = 605, y = 0)
        
        self.marco_sup_derecho = customtkinter.CTkFrame(self, width = 195, height = 195)
        self.marco_sup_derecho.place(x = 605, y = 0)

        self.titulo_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "GIANLUCA", text_color = "#FF0000", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_sup_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Posicion: ", font = ("Verdana", 14, "bold"), text_color = "#FF0000")
        self.posicion_sup_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Altura: ", font = ("Verdana", 14, "bold"), text_color = "#FF0000")
        self.altura_sup_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Velocidad: ", font = ("Verdana", 14, "bold"), text_color = "#FF0000")
        self.velocidad_sup_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_izquierdo_borde = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#FFFF00", text = "")
        self.marco_inf_izquierdo_borde.place(x = 0, y = 400)
        
        self.marco_inf_izquierdo_fondo = customtkinter.CTkLabel(self, width = 195, height = 195, bg_color = "#000000")
        self.marco_inf_izquierdo_fondo.place(x = 0, y = 405)

        self.marco_inf_izquierdo = customtkinter.CTkFrame(self, width = 195, height = 195)
        self.marco_inf_izquierdo.place(x = 0, y = 405)

        self.titulo_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "JOACO", text_color = "#FFFF00", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Posicion: ", font = ("Verdana", 14, "bold"), text_color = "#FFFF00")
        self.posicion_inf_izquierdo.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Altura: ", font = ("Verdana", 14, "bold"), text_color = "#FFFF00")
        self.altura_inf_izquierdo.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Velocidad: ", font = ("Verdana", 14, "bold"), text_color = "#FFFF00")
        self.velocidad_inf_izquierdo.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_derecho_borde = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#00FF00", text = "")
        self.marco_inf_derecho_borde.place(x = 600, y = 400)
        
        self.marco_inf_derecho_fondo = customtkinter.CTkLabel(self, width = 195, height = 195, bg_color = "#000000")
        self.marco_inf_derecho_fondo.place(x = 605, y = 405)
        
        self.marco_inf_derecho = customtkinter.CTkFrame(self, width = 195, height = 195)
        self.marco_inf_derecho.place(x = 605, y = 405)

        self.titulo_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "SANTI", text_color = "#00FF00", font = ("Verdana", 16, "bold"), anchor = "center")
        self.titulo_inf_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Posicion: ", font = ("Verdana", 14, "bold"), text_color = "#00FF00")
        self.posicion_inf_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Altura: ", font = ("Verdana", 14, "bold"), text_color = "#00FF00")
        self.altura_inf_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Velocidad: ", font = ("Verdana", 14, "bold"), text_color = "#00FF00")
        self.velocidad_inf_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Creo el rectangulo del medio donde iran los graficos

        self.rectangulo_fondo = customtkinter.CTkLabel(self, width = 400, height = 300, bg_color = "#111111")
        self.rectangulo_fondo.place(x = 200, y = 150)

        self.rectangulo = customtkinter.CTkFrame(self, width = 400, height = 300)
        self.rectangulo.place(x = 200, y = 150)

        self.imagen_ancho = 400
        self.imagen_largo = 300
        self.image_path = "C://Users//Felipe//Documents//Proyectos//Dashboard//Mountain.PNG"
        self.mountain_image = customtkinter.CTkImage(light_image = Image.open(os.path.join(self.image_path)), size = (self.imagen_ancho, self.imagen_largo))
        self.mountain_image_label = customtkinter.CTkLabel(self.rectangulo, image = self.mountain_image, text = "")
        self.mountain_image_label.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.titulo_rect = customtkinter.CTkLabel(self.rectangulo, text = "Graficos", anchor = "center", font = ("Verdana", 16, "bold"), text_color = "#000000", bg_color = "#FFFFFF")
        self.titulo_rect.place(relx = 0.2, rely = 0.1, anchor = "center")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.rectangulo)
        self.canvas.get_tk_widget().place(relx = 0.5, rely = 0.5, anchor = "center")

        self.update_graph()
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
        # brillo


        self.brillo_slider = customtkinter.CTkSlider(self, from_ = 0, to = 255, orientation = "vertical", button_length = 20, button_color = "#FFFFFF", button_corner_radius = 1)
        self.brillo_slider.place(x = 780, y = 200)
        self.brillo_slider.set(50)
        

    def update_graph(self):
        self.ax.clear()
        while not c.is_over():
            print(c.get_data())
            grafico2d.coordenadas()
            c.next_iteration('Los cracks', {h.nombre: h.ordenes for h in hikers})
            if hikers[0].almost_out() is True:
                hikers[0].random()
            if hikers[1].almost_out() is True:
                hikers[1].random()
            if hikers[2].almost_out() is True:
                hikers[2].random()
            if hikers[3].almost_out() is True:
                hikers[3].random()
            time.sleep(0.5) # Para que no colapse el server

    # Defino un metodo que permite actualizar el timer y comenzar cada vez que se abre la ventana
    # Ademas import el modulo time para poder hacerlo.
    def update_timer(self):
        tiempo_transcurrido = int(time.time() - self.start_time)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        string_tiempo = f"{horas :02d} : {minutos :02d} : {segundos : 02d}"
        self.timer.configure(text = f"TIMER = {string_tiempo}")
        self.timer.after(1000, self.update_timer)

    # Defino un metodo que permite hacer una animacion ascii en el costado izquierdo.
    # Import el modulo threading y art, ademas de tambien utilizar el modulo time.
    

    def generar_ascii(self):
        animacion = [
            "    O\n   /|\\\n    |\n   / \\",
            "   \\O/\n    |\n   /|\\\n   / \\",
            "    |\\\n   \\O/\n   /|\\\n   / \\",
            "   / \\\n    |\\\n   \\O/\n   /|\\",
        ]
        animacion_generada = [pyfiglet.figlet_format(frame, font = "small") for frame in animacion]
        return animacion_generada

    def animacion_ascii(self):
        animacion_generada = self.generar_ascii()

        while True:
            for frame in animacion_generada:
                self.animacion_et.configure(text = frame)
                self.update_idletasks()
                time.sleep(0.5) 
                

    # Este metodo inicializara la animacion en un hilo separado, es decir al mismo tiempo que otro programa.
    # Modulo threading

    def comienzo_animacion(self):
        threading.Thread(target = self.animacion_ascii).start()

    # Defino una funcion para poder actualizar el valor del brillo del dashboard.
    




if __name__ == "__main__":
    mountain_dash = Dashboard()
    mountain_dash.comienzo_animacion()
    mountain_dash.mainloop()