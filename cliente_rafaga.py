import socket
import time

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.0.3.1", 8080))  # Proxy en sdist0

    mensajes = ["HOLA", "MUNDO", "ESTO", "ES", "UN", "STREAM"]
    print("Enviando ráfaga de mensajes seguidos por la misma conexión TCP...")

    for msg in mensajes:
        sock.sendall(msg.encode("utf-8"))
        # Sin sleep o con delay ínfimo para forzar que salgan pegados
    
    time.sleep(0.5)
    sock.close()
    print("Ráfaga finalizada.")

if __name__ == "__main__":
    main()