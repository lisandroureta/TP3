import sys
import socket

def main():
    destino_ip = sys.argv[1] if len(sys.argv) > 1 else "10.0.3.1"
    destino_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    mensaje = sys.argv[3] if len(sys.argv) > 3 else "Mensaje de prueba TCP"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((destino_ip, destino_port))
        print(f"Conectado a {destino_ip}:{destino_port}")
        
        sock.sendall(mensaje.encode("utf-8"))
        print(f'Enviado: "{mensaje}"')

        # Recibir respuesta opcional
        respuesta = sock.recv(1024)
        if respuesta:
            print(f'Respuesta recibida: "{respuesta.decode("utf-8")}"')
    except Exception as e:
        print(f"Error de conexión con {destino_ip}:{destino_port}: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()