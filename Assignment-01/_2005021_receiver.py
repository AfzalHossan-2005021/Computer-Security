import os
import socket
import hashlib
import _2005021_ecc as ecc
import _2005021_aes_ctr as aes

CHUNK_SIZE = 4096

# reserve a port for your service
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

# Function to receive domain parameters
def receive_domain_parameters(skt: socket):
    # Receive the prime number p
    p = int(receive_string(skt))
    
    # Receive the curve parameters a and b
    a = int(receive_string(skt))
    b = int(receive_string(skt))
    
    # Receive the generator point G
    Gx = int(receive_string(skt))
    Gy = int(receive_string(skt))
    
    return p, a, b, (Gx, Gy)

# Function to exchange public keys
def exchange_public_keys(skt: socket, B: tuple[int, int]) -> tuple[int, int]:
    # Receive the public key A
    Ax = int(receive_string(skt))
    Ay = int(receive_string(skt))
    A = (Ax, Ay)

    # Send the public key B
    send_string(skt, str(B[0]))
    send_string(skt, str(B[1]))

    return A

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

# Receive any type of file over a socket connection
def receive_file(skt: socket, key: str, save_directory: str='received') -> tuple[str, int]:
    meta_data = secure_receive_string(skt, key)
    file_size_str, file_name = meta_data.split('|', 2)

    file_size = int(file_size_str)

    # Create save path
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, file_name)
    
    print("Total file size:", file_size)
    
    def receive_chunk_by_chunk(file_size: int):
        remaining_bytes = int(2 * file_size)
        while True:
            chunk = skt.recv(min(CHUNK_SIZE, remaining_bytes))
            if not chunk:
                break
            remaining_bytes -= len(chunk)
            yield chunk
    # Decrypt and write the file in chunks
    aes.decrypt_file_in_chunks(key, save_path, receive_chunk_by_chunk(file_size))

    return (file_name, file_size)

def main():
    print("Here is Bob")
    # next create a socket object 
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Next bind to the port and listen to requests
    skt.bind(('', port))
    skt.listen(5)	 
 
    # Establish connection with client. 
    client_skt, addr = skt.accept()
    print('Got connection from Alice')    

    # Receive domain parameters
    p, a, b, G = receive_domain_parameters(client_skt)

    # Generate private and public keys
    ka, B = ecc.generate_keys(G, int(a), int(p))

    # Exchange public keys
    A = exchange_public_keys(client_skt, B)

    # # Generate shared secret
    R = ecc.double_and_add(ka, A, int(a), int(p))

    key = derive_aes_key(R, key_length)

    choice = secure_receive_string(client_skt, key)
    print("Choice from Alice:", choice)

    if choice == "file":
        # Receive the file
        file_name, file_size = receive_file(client_skt, key)
        print(f"File received: {file_name} {file_size} bytes")
    elif choice == "string":
        # Receive and then decrypt the ciphered text using AES
        plain_text = secure_receive_string(client_skt, key)
        print("Text from Alice:", plain_text)
    else:
        print("Invalid choice. Exiting.")

    client_skt.close()
    skt.close()

if __name__ == '__main__':
    main()