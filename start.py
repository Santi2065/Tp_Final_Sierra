import os
import platform
import time

files = ['start_server.py','client_official.py', 'dashprueba.py']

for file in files:
    if platform.system() == 'Windows':
        os.system(f'start cmd /k python {file}')
    else:
        os.system(f'gnome-terminal -- python3 {file}')
