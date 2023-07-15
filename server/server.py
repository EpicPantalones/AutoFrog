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
    alen = len(args)
    if alen < 2:
        response = "vAkEoAYB0pd3nOW8XSOHzxRU87YmEB4KUGoJI1eLnJ7Tk58RPV"
    else:
        '''read command
        this will read from the received directory
        and make all the necessary changes to the
        current directory and the reload the monitor'''
        if args[0] == "read":
            received = os.listdir(f"{CWD}/received")
            current = os.listdir(f"{CWD}/current")
            for file in received:
                if file == "manifest.txt":
                    new_chan = []
                    with open(f"{CWD}/received/{file}","r") as manifest:
                        for i in range(0,8):
                            new_chan.append(manifest.readline().strip())
                        print(new_chan)
                        manifest.close()
                    with open(f"{CWD}/channels.conf","w") as config:
                        for channel in new_chan:
                            config.write(f"{str(channel)}\n")
                        config.close()
                else:
                    os.system(f"cp {CWD}/received/{file} {CWD}/current/{file}")
    
    # Example: Sending a response back to the client
    response = f"received {str(OK)}"
    print(response)
    client_socket.sendall(response.encode())

# Usage example
if __name__ == "__main__":
    host = ""  # Leave empty to listen on all available interfaces
    port = 1234  # Choose a port number
    
    start_socket_server(host, port)
