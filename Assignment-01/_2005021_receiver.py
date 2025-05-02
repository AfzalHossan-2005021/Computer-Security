import socket
import hashlib
import _2005021_ecc as ecc
import _2005021_aes as aes

CHUNK_SIZE = 4096

# reserve a port for your service
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

    ciphered_text = receive_string(client_skt)

    # Decrypt the ciphered text using AES
    plain_text = aes.decrypt_ciphered_text(key, ciphered_text)
    print("Text from Alice:", plain_text)

    client_skt.close()
    skt.close()

if __name__ == '__main__':
    main()