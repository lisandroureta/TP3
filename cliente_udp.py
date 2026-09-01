import sys
import socket

# Servidores con las IPs reales de tus VMs y los puertos del TP
SERVIDORES = [
    ("10.0.3.1", 5001),  # sdist0
    ("10.0.3.2", 5002),  # sdist1
    ("10.0.3.3", 5003)   # sdist2
]

def main():
    # Si pasás argumento (ej: python3 cliente_udp.py 1), usa "cliente 1"
    num = sys.argv[1] if len(sys.argv) > 1 else "1"
    client_id = f"cliente {num}"
    mensaje = f"Hola desde el {client_id}"
    
    # Socket UDP (SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"[{client_id}] Enviando mensaje a todos los servidores...")
    for ip, puerto in SERVIDORES:
        try:
            sock.sendto(mensaje.encode("utf-8"), (ip, puerto))
            print(f" -> Datagrama enviado a {ip}:{puerto}")
        except Exception as e:
            print(f" -> Error hacia {ip}:{puerto}: {e}")
            
    sock.close()

if __name__ == "__main__":
    main()