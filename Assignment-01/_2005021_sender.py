# Import socket module 
import socket
import random
import hashlib
import _2005021_ecc as ecc
import _2005021_aes as aes

SEED = 2005021
CHUNK_SIZE = 4096

# Define the port on which you want to connect 
port = 12345

# Define the key length
key_length = 128

# Function to derive AES key from the shared secret
def derive_aes_key(R: tuple[int, int], key_length_bits: int) -> str:
    # Convert point to bytes
    seed = str(R[0]).encode('utf-8')
    
    # Determine key length in bytes
    key_bytes_length = key_length_bits // 8
    
    # Use SHA-256 for key derivation
    key_material = b""
    counter = 0
    
    # Generate enough key material
    while len(key_material) < key_bytes_length:
        # Combine seed with counter to get unique hash inputs
        counter_bytes = counter.to_bytes(8, byteorder='big')
        hash_input = seed + counter_bytes
        
        # Hash the input
        hash_output = hashlib.sha256(hash_input).digest()
        key_material += hash_output
        counter += 1

    # Truncate to the required key length
    # key_material = key_material[:key_bytes_length]
    
    # key = ""
    # for byte in key_material:
    #     # Convert each byte to its hexadecimal representation
    #     key += chr(byte)

    return key_material[:key_bytes_length].decode('unicode_escape')

# Function to send a string over a socket
def send_string(skt: socket, string: str):
    # Encode the string to bytes
    byte_string = string.encode()
    
    # Send the length of the string first
    skt.send(str(len(byte_string)).encode())

    # Wait for the server to be ready to receive the string
    r = skt.recv(1024).decode()
    if(int(r) != len(byte_string)):
        print("Length mismatch")
        return
    
    # Send the actual string as 4kb chunks
    for i in range(0, len(byte_string), CHUNK_SIZE):
        chunk = byte_string[i:min(i + CHUNK_SIZE, len(byte_string))]
        skt.send(chunk)

# Function to receive a string over a socket
def receive_string(skt: socket):
    # Receive the length of the string first
    length = int(skt.recv(1024).decode())
    skt.send(str(length).encode())

    # Initialize an empty byte array to store the received data
    byte_string = bytearray()

    # Receive the string in chunks
    while len(byte_string) < length:
        chunk = skt.recv(min(CHUNK_SIZE, length - len(byte_string)))
        if not chunk:
            break
        byte_string.extend(chunk)

    # Decode the byte array to a string
    return byte_string.decode()

# Function to send domain parameters
def send_domain_parameters(skt: socket, p: int, a: int, b: int, G: tuple[int, int]) -> None:
    # Send the prime number p
    send_string(skt, str(p))
    
    # Send the curve parameters a and b
    send_string(skt, str(a))
    send_string(skt, str(b))
    
    # Send the generator point G
    send_string(skt, str(G[0]))
    send_string(skt, str(G[1]))

# Function to exchange public keys
def exchange_public_keys(skt: socket, A: tuple[int, int]) -> tuple[int, int]:
    # Send the public key A
    send_string(skt, str(A[0]))
    send_string(skt, str(A[1]))

    # Receive the public key B
    Bx = int(receive_string(skt))
    By = int(receive_string(skt))

    return (Bx, By)

def main():
    print("Here is Alice")
    # Create a socket object 
    skt = socket.socket()		 

    # connect to the server on local computver 
    skt.connect(('127.0.0.1', port))
    print("Connected to Bob")

    # Set seed and generate a random prime number
    random.seed(SEED)
    # Send the values of a, b, G, p to the server
    p = ecc.generate_prime(key_length)
    a, b = ecc.generate_curve_params(p, key_length)
    x, y = ecc.find_generator_point(a, b, p)
    G = (x, y)

    # Send the domain parameters to the server
    send_domain_parameters(skt, p, a, b, G)

    # Generate private and public keys
    ka, A = ecc.generate_keys(G, a, p)
    
    # Exchange public keys with the server
    B = exchange_public_keys(skt, A)

    # # Generate shared secret
    R = ecc.double_and_add(ka, B, int(a), int(p))
    
    key = derive_aes_key(R, key_length)

    plain_text = input("Enter the text to send to Bob: ")

    # Encrypt the plain text using AES
    ciphered_text = aes.encrypt_plain_text(key, plain_text)

    send_string(skt, ciphered_text)

    skt.close()

if __name__ == "__main__":
    main()