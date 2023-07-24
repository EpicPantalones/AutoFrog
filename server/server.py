import threading
import socket
import os

CWD = os.getcwd()
KILLSWITCH = True
'''
Socket server runs on an infinite loop. You can start it in a thread
to prevent the server from blocking the rest of the program.
'''
def start_socket_server(host, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server started. Listening on {host}:{port}")
    
    try:
        while KILLSWITCH:
            # Accept a connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from: {client_address}")
            
            # Handle the client connection in a new thread
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    finally:
        server_socket.close()

'''
handle_client spawns everytime the server gets a connection. It receives
a message and then directs it into handle_message, where a message is returned.
'''
def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        
        if not data:
            break  # No more data received, exit the loop
        
        # Handle the received message in a new thread
        threading.Thread(target=handle_message, args=(client_socket, data)).start()

    # Close the client socket
    client_socket.close()

'''
handle_message will perform the action from the server
spawns from the thread handle_client
'''
def handle_message(client_socket, message):
    # DEBUG Printing the received message
    print(f"Received message: \"{message}\"")
    OK = True
    args = message.split()
    print(args)
    commands = ["UPDATEREGISTRY","REQUESTLIVESTATUS","LIVECOMM"]
    if args[0] not in commands:
        response = "ERROR comm-not-recognized"
    else:
        if args[0] == "UPDATEREGISTRY":
            reached = False
            edits = []
            deletes = []
            for i,arg in enumerate(args):
                if i == 0:
                    continue
                if arg == "DELETES":
                    reached = True
                elif reached:
                    deletes.append(arg)
                else:
                    edits.append(arg)
            # function that will update system
            print(edits)
            print(deletes)
            response = "RECEIVED"
        elif args[0] == "REQUESTLIVESTATUS":
            # will need to create system to grab status...
            response = "RECEIVED 1 0 1 0 1 0 1 0"
        elif args[0] == "LIVECOMM":
            # will need to create system to grab status...
            response = "RECEIVED COMPLETE"
    client_socket.sendall(response.encode())

# Usage example
if __name__ == "__main__":
    host = ""  # Leave empty to listen on all available interfaces
    port = 1234  # Choose a port number
    
    start_socket_server(host, port)
