import sys, atexit
import socket
import threading

HEADER = 64
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT!"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

log = []

def cleanup():
    try:
        with open('log.txt','w') as f:
            f.write(str(log).replace(",","\n").replace("'",""))
    except Exception as e:
        print(e, file=sys.stderr)

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recive(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg = conn.recv(int(msg_length)).decode(FORMAT)
        if msg == DISCONNECT:
            conn.close()
            return False
        message = ((str(addr).replace("', ",":"))[2:-1] + " : \"" + msg +"\"")
        log.append(message)
        send(conn, "message recived\n"+ str(log).replace(",","\n").replace("'",""))
        print(message)
        return True

def handel_client(conn, addr):
    print(f"[NEW CONNECTION] "+ (str(addr).replace("', ",":"))[2:-1] +" connected. ")
    connected = True
    while connected:
        connected = recive(conn, addr)
    exit()

def create_connection():
    conn, addr = server.accept()
    thread = threading.Thread(target=handel_client, args=(conn, addr))
    thread.start()
    activeConn = threading.active_count() - 1
    print(f"[ACTIVE CONNECTIONS] {activeConn} Connections Active")

def start():
    server.listen()
    running = True
    while running:
       create_connection()
          
print("[Starting] Server is starting.....  http://" + (str(ADDR).replace("', ",":"))[2:-1])
start()
atexit.register(cleanup)