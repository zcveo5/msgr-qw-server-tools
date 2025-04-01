import json
import time
import traceback
import socket
import threading

ip_data = json.load(open("./conf.json", 'r'))
HOST = ip_data['HOST']
PORT = ip_data['PORT_AUTH']
clients = []
client_addresses = []

if HOST == '' or PORT == 0:
    print('Incorrect IP_CONFIGURATION')
    while True:
        time.sleep(1)

def handle_client(client_socket):
    data_raw = json.load(open('data.json', 'r'))
    data = data_raw['users']
    while True:
        try:
            try:
                message = client_socket.recv(1024).decode('utf-8')
            except ConnectionResetError:
                print('Client close his connection')
                message = ''
            if not message:
                break
            print('=========')
            print(f"Received: {message}")
            data_recv = eval(message)
            ans = {}


            if 'username' in data_recv:
                if data_recv['username'] not in data:
                    data.update({data_recv['username']: {'password': data_recv['password'], 'global_block': 'False'}})
                    ans = {'status': 'ok', 'answer': data[data_recv['username']]}
                    print(f"new user {data_recv['username']}")
                else:
                    if data[data_recv['username']]['global_block'] == 'True':
                        ans = {'status': 'ok', 'answer': 'blocked'}
            if 'action' in data_recv:
                if data_recv['action'].split(':')[0] == 'update_data':
                    print('upddata')
                    if data_recv['action'].split(':')[1] not in data[data_recv['username']]:
                        if data_recv['action'].split(':')[1] != 'global_block':
                            print('adding')
                            data[data_recv['username']].update({data_recv['action'].split(':')[1]:data_recv['action'].split(':')[2]})
                    else:
                        if data_recv['action'].split(':')[1] != 'global_block':
                            print('adding')
                            data[data_recv['username']][data_recv['action'].split(':')[1]] = data_recv['action'].split(':')[2]
                if data_recv['action'].split(':')[0] == '_in_db':
                    ans = {'status': 'ok', 'answer': data_recv['username'] in data}
                if data_recv['action'] == 'modlist':
                    ans = {'status': 'ok', 'answer': f'{list(data_raw["modlist"].keys())}'}
                if data_recv['action'].split(':')[0] == 'get_mod':
                    ans = {'status': 'ok', 'answer': f'{data_raw["modlist"][data_recv['action'].split(':')[1]]}'}
                if data_recv['action'] == 'upload_mod':
                    data_raw["modlist"].update({data_recv['MOD_NAME']: data_recv['PLUG_CODE']})
                    ans = {'status': 'ok', 'answer': 'uploaded'}
                if data_recv['action'] == 'update':
                    ans = {'status': 'ok', 'answer': f"{open('./msgr.py', 'r').read()}"}
            if ans == {}:
                ans = {'status': 'ok', 'answer': data[data_recv['username']]}
            client_socket.send(f'{ans}'.encode('utf-8'))
            json.dump(data_raw, open('data.json', 'w'))
            print('=========\n')
        except Exception as handle_err:
            print(f'handle: {handle_err}')
            client_socket.send("Incorrect server".encode('utf-8'))
            print(traceback.format_exc())
            break


def start_server(pp):
    global print
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print = pp
    print(f"\nServer started on addr {HOST}:{PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Connected with {addr}")
            clients.append(client_socket)
            client_addresses.append(addr)
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        except Exception as main_err:
            print(f'main: {main_err}')
            break

if __name__ == "__main__":
    start_server()