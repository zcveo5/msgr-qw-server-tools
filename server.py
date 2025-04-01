import json
import socket
import threading
import time

data = json.load(open("./conf.json", 'r'))
HOST = data['HOST']
PORT = data['PORT_CHAT']
clients = []
client_addresses = []

if HOST == '' or PORT == 0:
    print('Incorrect IP_CONFIGURATION')
    while True:
        time.sleep(1)


def handle_client(client_socket):
    last_ex = Exception
    counter = 0
    addr = client_addresses[clients.index(client_socket)]
    while True:
        try:
            message = eval(client_socket.recv(1024).decode('utf-8'))
            if not message:
                break
            print(f"Received: {message}")
            name = f'{addr[0]}:{addr[1]}'
            print('check pip')
            if message['_show_ip'] == 'False':
                name = message['name']
            print(name)
            broadcast(f"{name}: {message['text']}", client_socket)
        except ConnectionResetError:
            print(f'{addr} disconnected hard')
            break
        except Exception as _ex:
            print(type(_ex))
            client_socket.send('error'.encode('utf-8'))
            if last_ex == type(_ex):
                counter += 1
            if counter >= 5:
                print(f'too much errors {type(_ex)}')
                break
            last_ex = type(_ex)

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def start_server(pp):
    global print
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print = pp
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connected with {addr}")
        clients.append(client_socket)
        client_addresses.append(addr)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()