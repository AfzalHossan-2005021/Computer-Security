# Import socket module 
import socket
import random
import _2005021_ecc as ecc
import _2005021_aes as aes

# Define the port on which you want to connect 
port = 12345

# Define the key length
key_length = 128

def main():
    print("Here is Alice")
    # Create a socket object 
    skt = socket.socket()		 

    # connect to the server on local computer 
    skt.connect(('127.0.0.1', port))
    print("Connected to Bob")

    # Set seed and generate a random prime number
    random.seed(2005021)
    # Send the values of a, b, G, p to the server
    p = ecc.generate_prime(key_length)
    skt.send(str(p).encode())
    skt.recv(1024).decode()
    a, b = ecc.generate_curve_params(p, key_length)
    skt.send(str(a).encode())
    skt.recv(1024).decode()
    skt.send(str(b).encode())
    skt.recv(1024).decode()
    x, y = ecc.find_generator_point(a, b, p)
    skt.send(str(x).encode())
    skt.recv(1024).decode()
    skt.send(str(y).encode())
    skt.recv(1024).decode()
    G = (x, y)

    # Generate private and public keys
    ka, A = ecc.generate_keys(G, a, p)

    skt.send(str(A[0]).encode())
    Bx = skt.recv(1024).decode()
    skt.send(str(A[1]).encode())
    By = skt.recv(1024).decode()

    B = (int(Bx), int(By))

    # Generate shared secret
    R = ecc.double_and_add(ka, B, a, p)
    
    print(f"Shared secret: R={R}")

    skt.close()

if __name__ == "__main__":
    main()