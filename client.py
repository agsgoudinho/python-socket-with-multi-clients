import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))

exit_chat = False

try:
    input = raw_input
except NameError:
    pass


def receive_message(sock):
    while True:
        expected_data_size = int(sock.recv(4).decode())

        received_data = ''
        while len(received_data) < expected_data_size:
            received_data += sock.recv(4).decode()
        print("Mensagem: " +received_data)

        if received_data.lower() == "see ya":
            exit_chat = True
            break

try:
    receive_process = threading.Thread(target=receive_message, args=(sock,))
    receive_process.setDaemon(True)
    receive_process.start()

    while not exit_chat:
        mensagem = input("Mensagem: ").strip()
        send_data_size = len(mensagem)
        sock.sendall(str(send_data_size).zfill(4).encode())

        sock.sendall(mensagem.encode())

        if mensagem.lower() == "see ya":
            exit_chat = True
            break

finally:
    sock.close()