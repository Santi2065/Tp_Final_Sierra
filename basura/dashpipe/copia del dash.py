import tkinter
import tkinter.messagebox
import customtkinter
import time
import os
import threading
import pyfiglet
from PIL import Image

# Esto lo que hace es darnos la herramienta para poder pasar de light a dark.
customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")

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
        self.marco_sup_izquierdo_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111")
        self.marco_sup_izquierdo_fondo.place(x = 0, y = 0)
        
        self.marco_sup_izquierdo = customtkinter.CTkFrame(self, width = 200, height = 200)
        self.marco_sup_izquierdo.place(x = 0, y = 0)

        self.titulo_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Felipe", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.titulo_sup_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Posicion: ", font = ("Arial", 12, "bold"),   text_color = "#FFFFFF")
        self.posicion_sup_izquierdo.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Altura: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.altura_sup_izquierdo.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_sup_izquierdo = customtkinter.CTkLabel(self.marco_sup_izquierdo, text = "Velocidad: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.velocidad_sup_izquierdo.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_sup_derecho_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111")
        self.marco_sup_derecho_fondo.place(x = 600, y = 0)
        
        self.marco_sup_derecho = customtkinter.CTkFrame(self, width = 200, height = 200)
        self.marco_sup_derecho.place(x = 600, y = 0)

        self.titulo_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Gianluca", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.titulo_sup_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Posicion: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.posicion_sup_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Altura: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.altura_sup_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_sup_derecho = customtkinter.CTkLabel(self.marco_sup_derecho, text = "Velocidad: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.velocidad_sup_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_izquierdo_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111")
        self.marco_inf_izquierdo_fondo.place(x = 0, y = 400)

        self.marco_inf_izquierdo = customtkinter.CTkFrame(self, width = 200, height = 200)
        self.marco_inf_izquierdo.place(x = 0, y = 400)

        self.titulo_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Joaco", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.titulo_inf_izquierdo.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Posicion: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.posicion_inf_izquierdo.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Altura: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.altura_inf_izquierdo.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_izquierdo = customtkinter.CTkLabel(self.marco_inf_izquierdo, text = "Velocidad: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.velocidad_inf_izquierdo.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.marco_inf_derecho_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111")
        self.marco_inf_derecho_fondo.place(x = 600, y = 400)
        
        self.marco_inf_derecho = customtkinter.CTkFrame(self, width = 200, height = 200)
        self.marco_inf_derecho.place(x = 600, y = 400)

        self.titulo_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Santi", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.titulo_inf_derecho.place(relx = 0.5, rely = 0.1, anchor = "center")

        self.posicion_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Posicion: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.posicion_inf_derecho.place(relx = 0.1, rely = 0.35, anchor = "w")

        self.altura_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Altura: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.altura_inf_derecho.place(relx = 0.1, rely = 0.55, anchor = "w")

        self.velocidad_inf_derecho = customtkinter.CTkLabel(self.marco_inf_derecho, text = "Velocidad: ", font = ("Arial", 12, "bold"), text_color = "#FFFFFF")
        self.velocidad_inf_derecho.place(relx = 0.1, rely = 0.75, anchor = "w")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Creo el rectangulo del medio donde iran los graficos

        self.rectangulo_fondo = customtkinter.CTkLabel(self, width = 400, height = 300, bg_color = "#111111")
        self.rectangulo_fondo.place(x = 200, y = 150)

        self.rectangulo = customtkinter.CTkFrame(self, width = 400, height = 300)
        self.rectangulo.place(x = 200, y = 150)

        self.imagen_ancho = 400
        self.imagen_largo = 300
        self.image_path = "Felipeviaggio//Documents//Mis-Proyectos//Dashboard//Mountain.PNG"
        self.mountain_image = customtkinter.CTkImage(light_image = Image.open(os.path.join(self.image_path)), size = (self.imagen_ancho, self.imagen_largo))
        self.mountain_image_label = customtkinter.CTkLabel(self.rectangulo, image = self.mountain_image, text = "")
        self.mountain_image_label.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.titulo_rect = customtkinter.CTkLabel(self.rectangulo, text = "Graficos", anchor = "center", font = ("Arial", 16, "bold"), text_color = "#000000", bg_color = "#FFFFFF")
        self.titulo_rect.place(relx = 0.2, rely = 0.1, anchor = "center")
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Creo un timer que se va a ubicar en la parte superior del rectangulo.

        self.timer = customtkinter.CTkLabel(self, text = "00:00:00", text_color = "#FFFFFF", font = ("Arial", 35, "bold"), anchor = "center")
        self.timer.place(x = 400, y = 80, anchor = "center")
        self.start_time = time.time()
        self.update_timer()

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Debajo del rectangulo, agrego mas datos a tiempo real.

        self.altura_max = customtkinter.CTkLabel(self, text = "Altura maxima descubierta: ", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.altura_max.place(x = 220, y = 480, anchor = "w")

        self.altura_promedio = customtkinter.CTkLabel(self, text = "Altura promedio: ", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.altura_promedio.place(x = 220, y = 520, anchor = "w")

        self.terminado = customtkinter.CTkLabel(self, text = "Flag: ", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.terminado.place(x = 220, y = 560, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Coloco un cartel del estado del server.

        self.estado = customtkinter.CTkLabel(self, text = "Status: ", text_color = "#FFFFFF", font = ("Arial", 16, "bold"), anchor = "center")
        self.estado.place(x = 610, y = 300, anchor = "w")

        #-----------------------------------------------------------------------------------------------------------------------------------------------
        # Agrego una etiqueta entre los cuadrantes de la izquierda donde habra una animacion ascii

        self.animacion_fondo = customtkinter.CTkLabel(self, width = 200, height = 200, bg_color = "#111111", text = "")
        self.animacion_fondo.place(x = 0, y = 200)

        self.animacion_et = customtkinter.CTkLabel(self.animacion_fondo, text = "", text_color = "#FFFFFF", font = ("Arial", 12, "bold"), anchor = "nw")
        self.animacion_et.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        

    # Defino un metodo que permite actualizar el timer y comenzar cada vez que se abre la ventana
    # Ademas import el modulo time para poder hacerlo.
    def update_timer(self):
        tiempo_transcurrido = int(time.time() - self.start_time)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        string_tiempo = f"{horas : 02d} : {minutos : 02d} : {segundos : 02d}"
        self.timer.configure(text = f"Timer = {string_tiempo}")
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





if __name__ == "__main__":
    mountain_dash = Dashboard()
    mountain_dash.comienzo_animacion()
    mountain_dash.mainloop()