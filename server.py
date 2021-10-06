import socket
import threading

# Local Host Address of the server
HOST = '127.0.0.1'
# Port number for the server
PORT = 55555

# Creating Socket named server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind that server with the port and the host values
server.bind((HOST, PORT))
# Wait for the connection from the client
server.listen()

# Initalize a dictonary to store values of name and connected client address
dict_conn = {}

def recv_broad(conn):
    '''
        This Function will recive the client message 
        and send it to all the clients
    '''
    # Getting the name of the connected client
    name = dict_conn[conn]
    # Setting and sending a welcome message
    wel_msg = f'welcome to this chat {name}'
    conn.send(wel_msg.encode('ascii'))
    # Running continously untill client disconnected
    while True:
        try:
            # Try to recive message from the client and broadcast it
            message = conn.recv(1024)
            broadcast(message)
        except:
            # If error close the connection and delete the connected item from the dict
            conn.close()
            dict_conn.__delitem__(conn)
            # Broadcast and print the msg that the client has left the chat
            broadcast(message = f'{name} has left the chat!'.encode('ascii'))
            print(f'{name} has left the chat!')
            break

def broadcast(message):
    '''
        This function will broadcast the messages
        to all the clients connected
    '''
    for key in dict_conn:
        key.send(message)

def main():
    '''
        Main function which will run continously
        to recive and broadcast messages to all the client 
    '''
    print('Waiting for connection')
    while True: 
        # Accepting the connection from the client
        conn, addr = server.accept()
        # Sending message to say that the 1st message is a name
        conn.send('Name'.encode('ascii'))
        # Reciving the name and storing it in a variable and add that name and connection details to dict
        name_client = conn.recv(1024).decode('ascii')
        dict_conn[conn] = name_client
        # Printing and broadcasting that the client has joined the chat
        print(f'{name_client} has Joined Connected With {addr}')
        broadcast(message = f'{name_client} has joined the chat!'.encode('ascii'))
        # Sending the message that the client that he is connected to the server
        conn.send('Connected to server'.encode('ascii'))
        # Threading to recive and broadcast function 
        threading.Thread(target = recv_broad, args = (conn, )).start()

# Calling the main function
main()