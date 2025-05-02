import os
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
    seed = str(R[0]).encode('unicode_escape')
    
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
    byte_string = string.encode('unicode_escape')
    
    # Send the length of the string first
    skt.send((str(len(byte_string)).zfill(1024)).encode('unicode_escape'))

    # Wait for the server to be ready to receive the string
    r = skt.recv(1024).decode('unicode_escape')
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
    length = int(skt.recv(1024).decode('unicode_escape'))
    skt.send(str(length).encode('unicode_escape'))

    # Initialize an empty byte array to store the received data
    byte_string = bytearray()

    # Receive the string in chunks
    while len(byte_string) < length:
        chunk = skt.recv(min(CHUNK_SIZE, length - len(byte_string)))
        if not chunk:
            break
        byte_string.extend(chunk)

    # Decode the byte array to a string
    return byte_string.decode('unicode_escape')

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

# Function to send a string over a socket with AES encryption
def secure_send_string(skt: socket, plain_text: str, key: str) -> None:
    # Encode the string to bytes
    ciphered_text = aes.encrypt_plain_text(key, plain_text)
    byte_string = ciphered_text.encode('unicode_escape')
    
    # Send the length of the string first
    skt.send((str(len(byte_string)).zfill(1024)).encode('unicode_escape'))

    # Wait for the server to be ready to receive the string
    r = skt.recv(1024).decode('unicode_escape')
    if(int(r) != len(byte_string)):
        print("Length mismatch")
        return
    
    # Send the actual string as 4kb chunks
    for i in range(0, len(byte_string), CHUNK_SIZE):
        chunk = byte_string[i:min(i + CHUNK_SIZE, len(byte_string))]
        skt.send(chunk)

# Function to receive a string over a socket with AES decryption
def secure_receive_string(skt: socket, key: str) -> str:
    # Receive the length of the string first
    length = int(skt.recv(1024).decode('unicode_escape'))
    skt.send(str(length).encode('unicode_escape'))

    # Initialize an empty byte array to store the received data
    byte_string = bytearray()

    # Receive the string in chunks
    while len(byte_string) < length:
        chunk = skt.recv(min(CHUNK_SIZE, length - len(byte_string)))
        if not chunk:
            break
        byte_string.extend(chunk)

    # Decode the byte array to a string
    ciphered_text = byte_string.decode('unicode_escape')
    plain_text = aes.decrypt_ciphered_text(key, ciphered_text)
    return plain_text

# Function to send a file over a socket
def send_file(skt: socket, file_path: str, key: str):
    # Get file info
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    # Prepare header with metadata (size, name, type)
    header = f"{file_size}|{file_name}"

    # Send the header
    secure_send_string(skt, header, key)

    # Send file content in chunks
    with open(file_path, 'rb') as file:
        bytes_sent = 0
        
        while bytes_sent < file_size:
            # Read chunk and check if we reached EOF
            chunk = file.read(min(CHUNK_SIZE, file_size - bytes_sent))

            if not chunk:
                break
            
            # Send the chunk (convert bytes to string for encryption)
            chunk_str = chunk.hex()  # Convert binary data to hex string
            secure_send_string(skt, chunk_str, key)
            bytes_sent += len(chunk)
            print(f"Sent {bytes_sent} bytes of {file_size} bytes")

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

    choice = input("Do you want to send a file or a string? (file/string): ").strip().lower()
    if choice == "file":
        secure_send_string(skt, "file", key)
        file_path = input("Enter the path of the file to send: ")
        # Send the file
        send_file(skt, file_path, key)
    elif choice == "string":
        # Input the plain text and encrypt it using AES and then send it
        secure_send_string(skt, "string", key)
        plain_text = input("Enter the text to send to Bob: ")
        secure_send_string(skt, plain_text, key)
    else:
        print("Invalid choice. Please enter 'file' or 'string'.")

    skt.close()

if __name__ == "__main__":
    main()