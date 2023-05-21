import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
user_list = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):

    print(f"[New Connection] {addr} connected")

    username = '' #Need to make it global within the function so that the receiving user can get the sender's username

    try:

        connected = True

        while connected:

            data = ''
            byte = ''

            # while True:
            #     byte = conn.recv(1).decode(FORMAT)
            #     if not data:
            #         raise Exception('User has thrown exception')
                    
            #     if data == '\n':
            #         break
            #     else:
            #         byte += data
                
            while byte != '\n':
                byte = conn.recv(1).decode(FORMAT)
                data += byte

            if not data:
                raise Exception('Client Disconnected')

            space_index = data.find(" ")
            newline_index = data.find("\n")

            if data[0:space_index] == "HELLO-FROM":

                username = data[space_index + 1:newline_index-1]
                if username in user_list: #Throws an exception
                    print("JA TA CA O FDP")
                    msg = bytes(f"IN-USE\n", FORMAT)
                    conn.send(msg)
                    break
                else:
                    user_list[username] = conn
                print(f"Username is: {username}")
                msg = bytes(f"HELLO {data[space_index:]}\n", FORMAT)
                conn.send(msg)

                

            elif data[0:space_index] == "LIST":

                user_list_message = str()
                counter = 0
                for key in user_list:
                    counter += 1
                    if counter == len(user_list):
                        user_list_message += key
                    else:
                        user_list_message += key + ","
                msg = bytes(f"LIST-OK {user_list_message}\n", FORMAT)
                conn.send(msg)

            elif data[0:space_index] == "SEND":

                split_data = data[data.find(" ") + 1:]
                receiving_user = split_data[0:split_data.find(" ")]
                receiving_message = split_data[split_data.find(" ") + 1:]

                if receiving_user in user_list:
                    receiving_user_conn = user_list[receiving_user]
                    msg = bytes(f"DELIVERY {username} {receiving_message}\n", FORMAT)
                    receiving_user_conn.send(msg)
                    conn.send(bytes(f"SEND-OK\n", FORMAT))
                else: 
                    msg = bytes(f"BAD-DEST-USER\n", FORMAT)
                    conn.send(msg)

    except Exception as e:  

            print(f"There was an error with the user. The error is {e}")

    finally:

        if username and username in user_list:
            del user_list[username]
            print(f"This user has been deleted: {username}")
        
    conn.close()


def start():
    server.listen()
    print(f"Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")


print("Server has been started")
start()