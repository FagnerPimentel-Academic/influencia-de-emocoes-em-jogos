import socket
import json
from time import sleep

# Dados a serem enviados
data = {"emotion": 'NEUTRAL'}

# Converter para JSON
json_data = json.dumps(data)

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor Unity
PORT = 65432        # Porta que o servidor está escutando

sleep(3)

# Criação do socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json_data.encode('utf-8'))



