import socket
import random
from AES import aes_encryption, valid_block_size, key_and_text_to_matrix

def string_to_hex(input_string):
    try:
        # Convert the string to bytes using UTF-8 encoding
        string_bytes = input_string.encode('utf-8')
        
        # Convert bytes to hexadecimal
        hex_representation = string_bytes.hex()

        return hex_representation.lower()  # Convert to uppercase for consistency
    except UnicodeEncodeError:
        print("Error: Unable to encode the string.")
        return None

def to_hex(n):
    hex_digits = '0123456789abcdef'
    hex_str = ''
    while n > 0:
        hex_str = hex_digits[n % 16] + hex_str
        n = n // 16
    return hex_str
# Function to find gcd 
def gcd(a,b): 
    if b==0: 
        return a 
    else: 
        return gcd(b,a%b) 

# Function to perform Diffie Hellman Key Exchange
def diffie_hellman(sock, q, a):
    # Choose private key
    xb = random.randint(1, q)
    # Calculate public key
    yb = pow(a, xb, q)
    # Send public key to client
    sock.send(str(yb).encode())
    # Receive public key from client
    ya = int(sock.recv(1024).decode())
    # Calculate shared secret key
    k = pow(ya, xb, q)
    # Return the key
    return k

# Create a socket object
s = socket.socket()          
# Define the port on which you want to connect
port = 12345                
# Bind to the port
s.bind(('', port))         
# Put the socket into listening mode
s.listen(5)      
print("Socket is listening")            
# Establish connection with client
c, addr = s.accept()      
print('Got connection from', addr)

# Publicly known numbers
q = random.getrandbits(128)
a = random.randint(2, q)

# Send q and a to client
c.send((str(q) + ' ' + str(a)).encode())

# Perform Diffie Hellman Key Exchange
key = diffie_hellman(c, q, a)
print('Shared Secret Key:', key)

hexkey=to_hex(key)
print(hexkey)

#plain text to matrix
plaintext=string_to_hex("hello client")
valid_pt_block=valid_block_size(plaintext)
plaintext_matrix=key_and_text_to_matrix(plaintext)
print("plaintext block:",plaintext_matrix)
#key to matrix
valid_k_block=valid_block_size(hexkey)
key_matrix=key_and_text_to_matrix(hexkey)
print("key block:",key_matrix)

cipher_text=aes_encryption(plaintext_matrix,key_matrix)
print("encrypted text:",cipher_text)

