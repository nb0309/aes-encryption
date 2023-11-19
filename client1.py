import socket
import random

# Function to perform Diffie Hellman Key Exchange
def diffie_hellman(sock, q, a):
    # Choose private key
    xa = random.randint(1, q)
    # Calculate public key
    ya = pow(a, xa, q)
    # Send public key to server
    sock.send(str(ya).encode())
    # Receive public key from server
    yb = int(sock.recv(1024).decode())
    # Calculate shared secret key
    k = pow(yb, xa, q)
    # Return the key
    return k

# Create a socket object
s = socket.socket()          
# Define the port on which you want to connect
port = 12345                
# Connect to the server on local computer
s.connect(('127.0.0.1', port))

# Receive q and a from server
q, a = map(int, s.recv(1024).decode().split())

# Perform Diffie Hellman Key Exchange
key = diffie_hellman(s, q, a)
print('Shared Secret Key:', key)

# Close the connection
