import json
from tkinter import *
import threading, server, server_auth

serv_auth = None
serv_chat = None

def start():
    global serv_chat, serv_auth
    serv_chat = threading.Thread(target=server.start_server, args=(pp,))
    serv_auth = threading.Thread(target=server_auth.start_server, args=(pp,))
    serv_chat.start()
    serv_auth.start()


def pp(v):
    cmd.insert(END, v)

def comm_e(event):
    command = comm.get()
    cm_spl = command.split()
    comm.delete("0", END)
    if cm_spl[0] == 'Auth':
        if cm_spl[1] == 'block':
            data['users'][cm_spl[2]]['global_block'] = 'True'
            json.dump(data, open('./data.json' , 'w'))


data = json.load(open('./data.json'))
root = Tk()
root.title('MSGR_ServerAdministratingTools')
cmd = Text()
cmd.pack()
comm = Entry(width=60)
comm.pack()
comm.bind('<Return>', comm_e)
Button(text='Start Servers', command=lambda: start()).pack()
root.mainloop()