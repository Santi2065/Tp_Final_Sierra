import os
import platform
import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help = "ingrese el ip con el puerto ej:192.168.1.1:8080", type = str)
    args = parser.parse_args()
    if args.ip:
        ip,puerto = args.ip.split(":")   
        files = [f'dashprueba.py --ip {ip}:{puerto}', f'client_official.py --ip {ip}:{puerto}', f'client_official2.py --ip {ip}:{puerto}']
    else:
        files = [f'dashprueba.py', f'client_official.py', f'client_official2.py']

    for file in files:
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.system(f'start cmd /k python {file}')
        elif platform.system() == 'Darwin':
            os.system(f"osascript -e 'tell application \"Terminal\" to do script \"python3 {file}\"'")
        else:
            os.system(f'gnome-terminal -- python3 {file}')

if __name__ == "__main__":
    main()
