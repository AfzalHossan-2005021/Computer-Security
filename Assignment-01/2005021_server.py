# first of all import the socket library 
import socket
import _2005021_ecc as ecc
import _2005021_aes as aes

# reserve a port for your service
port = 12345

# Define the key length
key_length = 128

def main():
    print("Here is Bob")
    # next create a socket object 
    skt = socket.socket()

    # Next bind to the port and listen to requests
    skt.bind(('', port))
    skt.listen(5)	 
 
    while True: 
        # Establish connection with client. 
        client_skt, addr = skt.accept()
        print('Got connection from Alice')

        p = client_skt.recv(1024).decode()
        client_skt.send("ACK".encode())
        a = client_skt.recv(1024).decode()
        client_skt.send("ACK".encode())
        b = client_skt.recv(1024).decode()
        client_skt.send("ACK".encode())
        x = client_skt.recv(1024).decode()
        client_skt.send("ACK".encode())
        y = client_skt.recv(1024).decode()
        client_skt.send("ACK".encode())
        G = (int(x), int(y))

        # Generate private and public keys
        ka, B = ecc.generate_keys(G, int(a), int(p))
        Ax = client_skt.recv(1024).decode()
        client_skt.send(str(B[0]).encode())
        Ay = client_skt.recv(1024).decode()
        client_skt.send(str(B[1]).encode())

        A = (int(Ax), int(Ay))

        # Generate shared secret
        R = ecc.double_and_add(ka, A, int(a), int(p))

        print(f"Shared secret: R={R}")

        client_skt.close()

        # Breaking once connection closed
        break

if __name__ == '__main__':
    main()