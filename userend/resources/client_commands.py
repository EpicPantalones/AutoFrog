import paramiko
import socket

def send_message(hostname, port, message):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((hostname, port))
        # Send message
        client_socket.sendall(message.encode())
        # Close the socket
        client_socket.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
       
def send_request(hostname, port, message):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((hostname, port))
        # Send message
        client_socket.sendall(message.encode())
        # Receive the response from the server
        response = client_socket.recv(1024).decode()
        # Close the socket
        client_socket.close()
        return True, response
    except (socket.timeout, ConnectionRefusedError):
        return False, None
    
def handle_server_response(message):
    if message == None:
        return None
    args = message.split()
    if args[0] == "ERROR":
        return message
    else:
        return None

def scp_transfer(hostname, username, private_key_path, local_path, remote_path):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        # Connect to the SSH server using the private key
        ssh_client.connect(hostname, username=username, pkey=private_key)
        # Create an SCP client
        scp_client = ssh_client.open_sftp()
        # Perform the SCP transfer
        scp_client.put(local_path, remote_path)
        scp_client.close()
    finally:
        # Close the SSH client
        ssh_client.close()

def ping_socket(host, port, timeout=5):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        # Connect to the remote host and port
        client_socket.connect((host, port))
        client_socket.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False