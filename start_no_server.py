import os
import platform
import time

files = ['dashprueba.py', 'client_official2.py', 'client_official.py']

for file in files:
    time.sleep(2)
    if platform.system() == 'Windows':
        os.system(f'start cmd /k python {file}')
    else:
        os.system(f'gnome-terminal -- python3 {file}')
