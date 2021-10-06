import socket
import threading

# Constant Host address of server
HOST = '127.0.0.1'
# Constant port number of server
PORT = 55555

# Getting input for the name of the user
name = input('Enter Your Name:')

# Creating a socket named client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to the server address and server port
client.connect((HOST, PORT))

def rec_msg():
    '''
        This function will recive messages from the 
        server and print the message 
    '''
    # Running continously untill server closed
    while True:
        #first try to recive msg from the server
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Name':
                # if the message is name then send it to the server
                client.send(name.encode('ascii'))
            else:
                # else print the message in the screen
                print(message)
        # if exception close the client and break out of loop
        except:
            # print server down if msg not recived
            print('Server Down...')
            client.close()
            break

def write_msg():
    '''
        To send a message to the server to broadcast
    '''
    # run continously to send the message
    while True:
        # get the message and send it to the server
        message = '{}:{}'.format(name, input())
        client.send(message.encode('ascii'))

def main():
    # call the recive message and write message function in threading and start the threading
    threading.Thread(target = rec_msg).start()
    threading.Thread(target = write_msg).start()
    
# Calling the main function
main()
