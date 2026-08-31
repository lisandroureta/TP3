import os

def load_config():
    # Lectura basica de archivo .env si esta presente localmente
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

    # busca la variable SERVER_ID en el entorno. Si no la encuentra, usa el valor por defecto 0
    server_id = int(os.environ.get("SERVER_ID", 0))
    # Busca LISTEN_PORT. Si no existe, usa por defecto el puerto 5001
    listen_port = int(os.environ.get("LISTEN_PORT", 5001))
    
    return server_id, listen_port
#Imprime por pantalla el resultado con el formato exacto que pide el enunciado (servidor X, puerto Y)
if __name__ == "__main__":
    sid, port = load_config()
    print(f"servidor {sid}, puerto {port}")