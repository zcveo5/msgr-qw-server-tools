import threading
import server
import server_auth

serv_chat = threading.Thread(target=server.start_server, args=(print,))
serv_auth = threading.Thread(target=server_auth.start_server, args=(print,))

serv_auth.start()
serv_chat.start()
