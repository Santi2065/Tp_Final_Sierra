import os
import platform
import time

files = ['start_server.py', 'dashprueba.py', 'client_official.py', 'client_official2.py']

for file in files:
    time.sleep(1.5)
    if platform.system() == 'Windows':
        os.system(f'start cmd /k python {file}')
    else:
        os.system(f'gnome-terminal -- python3 {file}')
