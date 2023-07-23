import socket
import threading

'''
handle_message will perform the action from the server
spawns from the thread handle_client
'''
def handle_message(client_socket, message):
    # Add your logic here to act on the received message
    # You can perform any desired actions or processing
    
    # Example: Printing the received message
    print(f"Received message: \"{message}\"")
    
    # Example: Sending a response back to the client
    response = "Message received and processed"
    client_socket.sendall(response.encode())


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
        while True:
            # Accept a connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from: {client_address}")
            
            # Handle the client connection in a new thread
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    finally:
        server_socket.close()

# Usage example
if __name__ == "__main__":
    host = ""  # Leave empty to listen on all available interfaces
    port = 1234  # Choose a port number

    start_socket_server(host, port)
