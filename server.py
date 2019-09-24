import socket
import threading

# Criar o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Escutar a porta 9000
server = sock.bind(('localhost', 9000))

# definir limite de 10 conecxoes paralelas
sock.listen(10)

# Lista de clientes conectados
connections = []

def message_listener(connection, address_client):
    while True:
        # Aguardar tamanho da mensagem
        expected_data_size = ''
        while(expected_data_size == ''):
            expected_data_size += connection.recv(4).decode()
        expected_data_size = int(expected_data_size)

        received_data = ''
        while len(received_data) < expected_data_size:
            # Ler o dado recebido
            received_data += connection.recv(4).decode()
        message_to_send = "Cliente " + str(address_client[1]) + ": " + received_data
        print(message_to_send)

        for receiver in connections:
            if receiver != connection:
                # Tamanho da mensagem
                send_data_size = len(message_to_send)
                receiver.sendall(str(send_data_size).zfill(4).encode())

                # Enviar a mensagem
                receiver.sendall(message_to_send.encode())

        if received_data.lower() == "see ya":
            break

    # Finalizar a conexao com cliente
    print("Cliente " + str(address_client[1]) + " desconectando")
    connection.close()
    connections.remove(connection)

try:
    while True:
        # Aguardar uma conexao
        print("Aguardando conexao")
        connection, address_client = sock.accept()
        print(address_client[0] + ":" + str(address_client[1]) + " conectado")
        connections.append(connection)

        connections_process = threading.Thread(target=message_listener, args=(connection, address_client,))
        connections_process.setDaemon(True)
        connections_process.start()

finally:
    # Finalizar a conexao
    sock.close()