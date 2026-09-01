import socket
import threading
from config import load_config

def atender_cliente(conn, addr, server_id):
    try:
        while True:
            datos = conn.recv(4096)
            if not datos:
                break
            mensaje = datos.decode("utf-8")
            print(f'servidor {server_id} recibió (TCP): "{mensaje}" de {addr}')
            # Opcional: responder confirmación
            conn.sendall(b"OK")
    except Exception as e:
        print(f"Error con cliente {addr}: {e}")
    finally:
        conn.close()

def main():
    server_id, port = load_config()
    
    # Socket TCP (SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)
    print(f"Servidor {server_id} escuchando en TCP puerto {port}...")

    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=atender_cliente, args=(conn, addr, server_id))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    main()