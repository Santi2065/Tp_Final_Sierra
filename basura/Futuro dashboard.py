from communication.client.client import MountainClient
import tkinter as tk
import time

c = MountainClient()
c.add_team('Los cracks', ['Santi', 'Pipe'])
c.add_team('Los lentos', ['Gian', 'Joaco'])
c.finish_registration()

root = tk.Tk()
root.title("MountainClient")

while not c.is_over():
    
    # Obtener los datos de MountainClient
    data = c.get_data()
    
    # Actualizar las etiquetas de Tkinter
    column = 0
    for team, hikers in data.items():
        for hiker, values in hikers.items():
            team_label = tk.Label(root, text=f"Team: {team}")
            hiker_label = tk.Label(root, text=f"Hiker: {hiker}")
            x_label = tk.Label(root, text=f"x: {values['x']}")
            y_label = tk.Label(root, text=f"y: {values['y']}")
            z_label = tk.Label(root, text=f"z: {values['z']}")
            inclinacion_x_label = tk.Label(root, text=f"inclinacion_x: {values['inclinacion_x']}")
            inclinacion_y_label = tk.Label(root, text=f"inclinacion_y: {values['inclinacion_y']}")
            cima_label = tk.Label(root, text=f"cima: {values['cima']}")
            
            team_label.grid(row=0, column=column)
            hiker_label.grid(row=1, column=column)
            x_label.grid(row=2, column=column)
            y_label.grid(row=3, column=column)
            z_label.grid(row=4, column=column)
            inclinacion_x_label.grid(row=5, column=column)
            inclinacion_y_label.grid(row=6, column=column)
            cima_label.grid(row=7, column=column)
            
            column += 1
    
    
    while(not c.next_iteration('Los lentos', directives2)):
        continue
    # Actualizar los datos cada segundo
    root.update()
    
    # Start the event loop
    root.mainloop()
