import paramiko

# Replace with server details
hostname = "192.168.100.7"
username = "vidal"
password = "1234"   # Consider using SSH keys for better security

# Create SSH client
ssh = paramiko.SSHClient()

# Set policy to automatically add unknown host keys (not recommended for production)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
ssh.connect(hostname=hostname, username=username )

# Create SFTP client
sftp = ssh.open_sftp()

print(sftp.listdir('.'))

# Check if directory exists using stat
# try:
#   sftp.stat("/home/vidal/b")  # Replace with actual directory path
#   print("Directory exists")
# except IOError:
#   print("Directory does not exist")
#   ssh.exec_command("mkdir b")

# Execute a command
stdin, stdout, stderr = ssh.exec_command("ls -la")

# Get command output
output = stdout.read().decode()

# Print the output
print(output)

# Close the connection
ssh.close()