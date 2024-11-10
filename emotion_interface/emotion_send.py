import socket
import json
from time import sleep

# Dados a serem enviados
data = {"Happy": 0.7, "Sad": 0.7, "Angry": 0.7, "Scary": 0.0}

# Converter para JSON
json_data = json.dumps(data)

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor Unity
PORT = 65432        # Porta que o servidor está escutando

sleep(3)
envios = 40
for i in range(envios):
    # Criação do socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json_data.encode('utf-8'))
    print(f"Dados enviados {i+1}/{envios}")
    sleep(0.1)

