import socket
import threading #Threads allow us to separate code out so that it is not waiting for other code to finish before it is able to execute

HEADER = 64
PORT = 5050 #Course port is 5378
SERVER = socket.gethostbyname(socket.gethostname()) #This automatically gets the IP address of every user/device. Course IP is 143.47.184.219
ADDR = (SERVER, PORT) #The address is always a tuple
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Disconnect"
user_list = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Here we make a socket that allows the device to open up to other sockets
server.bind(ADDR) #Anything that connects to the given address will use the corresponding socket

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected") #Prints which new connection was just established

    connected = True
    
    while connected:

        data = ''
        byte = ''

        while byte != '\n': #Allows us to read byte-by-byte
            byte = conn.recv(1).decode(FORMAT)
            data += byte

        if data == '':
            break

        #print(f"{data}")

        space_index = data.find(" ")
        newline_index = data.find("\n")
    
        if data[0:space_index] == "HELLO-FROM":
            username = data[space_index + 1:newline_index]
            print(f"Username is: {username}")
            msg = bytes(f"HELLO {data[space_index:]}\n", FORMAT) #For handshake, the message is sent in byte form, which is why decoding is required
            #print(msg)
            conn.send(msg)

            if username in user_list:
                msg = bytes(f"IN USE\n", FORMAT)
                conn.send(msg)
                break
            else:
                user_list[username] = conn #We add the username as well as the connection so we can relate the logged in users appropriately
        elif data[0:space_index] == "LIST":
            user_list_message = str()
            for key in user_list:
                user_list_message += key + ","
            msg = bytes(f"LIST-OK {user_list_message}\n", FORMAT)
            conn.send(msg)
    
    conn.close() #We close the connection 

def start():

    server.listen() #We listen for new connections
    print(f"Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept() #Every time a new connection is established, a new object with the address is created
        thread = threading.Thread(target = handle_client, args = (conn, addr)) #Every time a new connection is done, we thread and pass it to the handle_client function
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}") #Prints amount of currently active threads/clients


print("Server has been started")
start ()



