# Librerias
import os
import argparse
import ipaddress

# Colores
class colors:
    HEADER = '\033[1;35m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKCYANL = '\033[1;36m'
    OKGREEN = '\033[92m'
    OKGREENL = '\033[1;32m'
    OKREDL = '\033[1;31m' 
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Función que determina el s.o
def detect_os(ip):
    # Enviamos un paquete ICMP al host y obtenemos su respuesta
    response = os.popen(f"/usr/bin/ping -c 1 {ip}").read()

    # Inicializamos la variable TTL
    ttl = 0

    # Analizamos la respuesta del host para obtener el valor del TTL
    for line in response.splitlines():
        if "ttl" in line:
            ttl = line.split("=")[-2]
            break
    
    # Convertimos el valor del TTL a una cadena de texto y quitamos la palabra "time"
    ttl = str(ttl).replace("time", "")

    # Convertirmos el valor del TTL a int
    ttl = int(ttl)

    # Si el valor del TTL es mayor que 0 y menor o igual a 64, entonces el host es Linux
    if ttl > 0 and ttl <= 64:
        ttl = str(ttl)
        ip = str(ip)
        print("[{}] Host: {} (TTL: {} | S.O: {})".format(colors.OKCYAN + ">" + colors.ENDC, colors.WARNING + ip + colors.ENDC, colors.OKGREEN + ttl + colors.ENDC, colors.OKREDL + "Linux" + colors.ENDC))

    # Si el valor del TTL es mayor o igual a 65 y menor o igual a 128, entonces el host es Windows
    elif ttl >= 65 and ttl <= 128:
        ttl = str(ttl)
        ip = str(ip)
        print("[{}] Host: {} (TTL: {} | S.O: {})".format(colors.OKCYAN + ">" + colors.ENDC, colors.WARNING + ip + colors.ENDC, colors.OKGREEN + ttl + colors.ENDC, colors.OKREDL + "Windows" + colors.ENDC))

    # En cualquier otro caso, no se puede determinar el sistema operativo del host
    else:
        ttl = str(ttl)
        ip = str(ip)
        print("[{}] Host: {} (TTL: {} | S.O: {})".format(colors.OKCYAN + ">" + colors.ENDC, colors.WARNING + ip + colors.ENDC, colors.OKGREEN + ttl + colors.ENDC, colors.OKREDL + "No determinado" + colors.ENDC))

# Función principal
def main():
    # Argumentos
    parser = argparse.ArgumentParser(description="wichSystem - Identifica el sistema operativo de un host a través de su TTL.")
    parser.add_argument("ip", type=str, help="Dirección IP del objetivo.")
    args = parser.parse_args()

    # La dirección IP del host se encuentra en args.ip
    ip = args.ip

    try:
        ip = ipaddress.ip_address(ip)

    except ValueError:
        print("[{}] El valor {} no es válido.".format(colors.OKREDL + "x" + colors.ENDC, colors.WARNING + ip + colors.ENDC))
        exit(1)

    if ip.version != 4:
        print("[{}] La dirección IP debe ser IPv4.".format(colors.OKREDL + "x" + colors.ENDC))
        exit(1)

    detect_os(ip)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Mensaje de interrupción
        print("[{}] Saliendo ...\n".format(colors.OKREDL + "x" + colors.ENDC))
        exit()
