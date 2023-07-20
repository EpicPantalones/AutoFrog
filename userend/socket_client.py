import socket

def send_message(hostname, port, message):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("Connecting...")
        # Connect to the server
        client_socket.connect((hostname, port))
        print("Sending...")
        # Send the test message
        client_socket.sendall(message.encode())
        print("Receiving...")
        # Receive the response from the server
        response = client_socket.recv(1024).decode()
        print(f"Received response: {response}")

    finally:
        # Close the socket
        client_socket.close()

# Usage
hostname = "192.168.50.42"  # Hostname or IP address of the server
port = 1234  # Port number that the server is listening on
message = "read all dir"  # Test message to send

send_message(hostname, port, message)
