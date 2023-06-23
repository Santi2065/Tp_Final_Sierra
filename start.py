import os
import platform
import time

files = ['start_server.py', 'client_official2.py', 'dashprueba.py', 'client_official.py']

for file in files:
    if platform.system() == 'Windows':
        os.system(f'start cmd /k python3 {file}')
        time.sleep(0.5)
    else:
        os.system(f'gnome-terminal -- python3 {file}')
