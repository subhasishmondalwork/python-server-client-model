
import socket
HEADER = 64
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT!"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg = conn.recv(int(msg_length)).decode(FORMAT)
        print(msg)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
def start():
    connected = True
    while connected:
        msg = input("write a message:")
        send(msg)
        recive(client)
        if msg == "!end":
            connected = False
            send(DISCONNECT)

start()