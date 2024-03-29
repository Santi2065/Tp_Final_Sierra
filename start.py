import os
import platform
import time
import argparse

def main():
    # Acepta direccion de ip, si no se ingresa ninguna se intenta conectar al servidor local
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help = "Ingrese el ip con el puerto ej: 192.168.1.1:8080\nPara acceder al servidor local, no ingrese ningun argumento", type = str)
    args = parser.parse_args()

    if args.ip:
        ip, puerto = args.ip.split(":")
        files = [f'tpf_Montana_dashboard.py --ip {ip}:{puerto}', f'tpf_Montana_cliente.py --ip {ip}:{puerto}', f'tpf_Montana_cliente.py --ip {ip}:{puerto}']
    else:
        files = ['start_server.py','tpf_Montana_dashboard.py', 'tpf_Montana_cliente.py','tpf_Montana_cliente2.py']

    for file in files:
        time.sleep(2)
        if platform.system() == 'Windows':
            os.system(f'start cmd /k python {file}')
        elif platform.system() == 'Darwin':
            script_directory = 'users/gianlucamusmarra/Dekstop/primer semestre 2023/Pensamiento computacional/Python/Tp_final_Sierra/'
            os.system(f"osascript -e 'tell application \"Terminal\" to do script \"cd \"{script_directory}\" && python3 {file}\"'")
        else:
            os.system(f'gnome-terminal -- python3 {file}')

if __name__ == "__main__":
    main()
