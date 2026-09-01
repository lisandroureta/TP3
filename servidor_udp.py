import socket
from config import load_config

def main():
    # 1. Cargamos configuración del entorno (.env)
    server_id, port = load_config()
    
    # 2. Creamos socket UDP (SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 3. Asociamos el socket a todas las interfaces en el puerto configurado
    sock.bind(("0.0.0.0", port))
    print(f"Servidor {server_id} escuchando en UDP puerto {port}...")

    # 4. Bucle infinito para recibir datagramas
    while True:
        datos, addr = sock.recvfrom(4096)
        mensaje = datos.decode("utf-8")
        print(f'servidor {server_id} recibió: "{mensaje}"')

if __name__ == "__main__":
    main()