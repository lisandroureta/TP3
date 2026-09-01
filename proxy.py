import socket
import threading
import argparse

def parse_backend(backend_str):
    host, port = backend_str.split(":")
    return (host, int(port))

class Proxy:
    def __init__(self, listen_port, backends, is_balancer):
        self.listen_port = listen_port
        self.backends = [parse_backend(b) for b in backends]
        self.is_balancer = is_balancer
        self.current_idx = 0
        self.lock = threading.Lock()

    def get_next_backend(self):
        if not self.is_balancer or len(self.backends) == 1:
            return self.backends[0]
        with self.lock:
            backend = self.backends[self.current_idx]
            self.current_idx = (self.current_idx + 1) % len(self.backends)
            return backend

    def copiar(self, origen, destino, sentido):
        total_bytes = 0
        try:
            while True:
                datos = origen.recv(4096)
                if not datos:
                    break
                destino.sendall(datos)
                total_bytes += len(datos)
                print(f"[LOG PROXY] {sentido}: {len(datos)} bytes transferidos (Total acumulado: {total_bytes})")
        except Exception:
            pass
        finally:
            try:
                destino.shutdown(socket.SHUT_WR)
            except Exception:
                pass
            destino.close()
            origen.close()

    def atender_conexion(self, cliente_sock, cliente_addr):
        backend_ip, backend_port = self.get_next_backend()
        print(f"\n[PROXY] Conexión entrante desde {cliente_addr} -> Redirigiendo a Backend {backend_ip}:{backend_port}")
        
        try:
            backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_sock.connect((backend_ip, backend_port))
        except Exception as e:
            print(f"[PROXY] Error al conectar con backend {backend_ip}:{backend_port}: {e}")
            cliente_sock.close()
            return

        # Hilo 1: Cliente -> Backend
        t1 = threading.Thread(target=self.copiar, args=(cliente_sock, backend_sock, f"Cliente {cliente_addr} -> Backend {backend_port}"))
        # Hilo 2: Backend -> Cliente
        t2 = threading.Thread(target=self.copiar, args=(backend_sock, cliente_sock, f"Backend {backend_port} -> Cliente {cliente_addr}"))
        
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("0.0.0.0", self.listen_port))
        server_sock.listen(10)
        
        modo = "Balanceador Round-Robin" if self.is_balancer else "Proxy Directo (1 solo backend)"
        print(f"[PROXY] Escuchando en el puerto {self.listen_port} ({modo})")
        print(f"[PROXY] Backends disponibles: {self.backends}")

        while True:
            cliente_sock, cliente_addr = server_sock.accept()
            t = threading.Thread(target=self.atender_conexion, args=(cliente_sock, cliente_addr))
            t.daemon = True
            t.start()

def main():
    parser = argparse.ArgumentParser(description="Proxy TCP / Balanceador de Carga")
    parser.add_argument("--escucha", type=int, default=8080, help="Puerto de escucha del proxy (default: 8080)")
    parser.add_argument("--backend", action="append", required=True, help="Host y puerto del backend (ej: 10.0.3.1:5001). Repetir para múltiples.")
    parser.add_argument("--balancer", action="store_true", help="Habilita balanceo de carga round-robin entre backends")
    args = parser.parse_args()

    proxy = Proxy(args.escucha, args.backend, args.balancer)
    proxy.run()

if __name__ == "__main__":
    main()