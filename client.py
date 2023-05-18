import socket
import threading

HEADER = 64
PORT = 5051 #5378 is the VU port
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnect"
SERVER = socket.gethostbyname(socket.gethostname()) # This binds the local client and server. If we just placed the IP to the right, it would connect to the VU server "143.47.184.219"
ADDR = (SERVER, PORT)

def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    login()

#Logins in client to server

def login():
    username = input("Choose an username: ")

    client_send(f"HELLO-FROM {username} \n")

    data = receive()

    print(data)

    if username == "!quit":
        exit()
    if data == "BUSY\n":
        print("Maximum number of users currently hosted")
        connect()
    elif data == "IN-USE\n":
        print("That username is already taken please enter another username: ")
        connect()
    elif data == "BAD-RQST-HDR\n":
        print("There is an error in the message header")
        connect()
    elif data == "BAD-RQST-BODY\n":
        print("There is an error in the message body")
        connect()
    
    return
        
#Sends message to clients     

def client_send(msg):
    
    message = msg.encode(FORMAT) #We encode the string into a byte format
    msg_length = len(message)
    bytes_to_send = msg_length

    while bytes_to_send > 0:
        bytes_to_send -= client.send(message[msg_length - bytes_to_send:])

    return 

#Handles !who input

def who():
    client_send("LIST\n")
    return

#Handles sending message to user

def user_send(input_message):
    username_upper_range = input_message.find(" ")
    username = input_message[1:username_upper_range]
    message = input_message[username_upper_range + 1:]
    client_send(f"SEND {username} {message} \n")
    return

#Defines Thread

def thread_reception():
    thread = threading.Thread(target=thread_data_reception, daemon=True)
    thread.start()
    return
    
#Handles Thread data

def receive():
    data = ''
    byte = ''
    while byte != '\n': #Allows us to read byte-by-byte
        byte = client.recv(1).decode(FORMAT)
        data += byte
    return data
        

def thread_data_reception():
    while True:
    
        data = receive()
        
        space_index = data.find(" ")

        if data[0:space_index] == "DELIVERY":
            split_data = data.split(" ")
            username = split_data[1]
            message = split_data[2:]
            message = ' '.join(message) #Decodes the message correctly
            print(f"Message received from {username}\nThe message is: {message}")
        elif data == "BAD-DEST-USER\n":
            print("Erroneous Destination, user not logged in")
        elif data == "SEND-OK":
            print("Successful Message")
        elif data[0:space_index] == "LIST-OK":
            print(data[8:])

#Main program starts here

connect()
thread_reception()

while True:

    input_message = input()
    if input_message == "!quit":
        exit()
    elif input_message == "!who": #Need to login first before calling the !who list
        who()
    elif "@" in input_message: #Means we need to send a message to another user
        user_send(input_message)
    else: 
        print("Unknown Command")
    