import paramiko

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

        # Close the SCP client
        scp_client.close()

    finally:
        # Close the SSH client
        ssh_client.close()

# Usage
hostname = "192.168.50.42"  # Hostname or IP address of the remote server
username = "ethan"  # Username to connect to the remote server
private_key_path = "/home/epicpantalones/.ssh/id_rsa"  # Path to your private key file
local_path = "/home/epicpantalones/Documents/AutoFrog/userend/file_to_copy.txt"  # Path to the local file you want to transfer
remote_path = "/home/ethan/copied_file.txt"  # Path on the remote server where you want to transfer the file

scp_transfer(hostname, username, private_key_path, local_path, remote_path)
