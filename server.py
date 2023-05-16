import socket
import threading #Threads allow us to separate code out so that it is not waiting for other code to finish before it is able to execute

HEADER = 64
PORT = 5050 #Course port is 5378
SERVER = socket.gethostbyname(socket.gethostname()) #This automatically gets the IP address of every user/device. Course IP is 143.47.184.219
ADDR = (SERVER, PORT) #The address is always a tuple
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Here we make a socket that allows the device to open up to other sockets
server.bind(ADDR) #Anything that connects to the given address will use the corresponding socket

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected") #Prints which new connection was just established

    connected = True
    
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #The integer shows how many bytes we are willing to receive in every message. This is a message protocol. We then decode the message from byte format into string format using utf-8

        if msg_length: #We make sure the msg has some content before trying to get its length and data

            msg_length = int(msg_length) #Length of message
            msg = conn.recv(msg_length.decode(FORMAT)) #Actual message

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}") #We print the message just to make sure it works
            conn.send("Msg received".encode(FORMAT)) #This is how the server sends back to a client

    conn.close() #We close the connection 

def start():

    server. listen() #We listen for new connections
    print(f"Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept() #Every time a new connection is established, a new object with the address is created
        thread = threading.Thread(target = handle_client, args = (conn, addr)) #Every time a new connection is done, we thread and pass it to the handle_client function
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}") #Prints amount of currently active threads/clients


print("Server has been started")
start ()



