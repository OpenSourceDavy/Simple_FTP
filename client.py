import socket
import sys
import os

def main():
    if len(sys.argv) != 6:
        print("Usage: python client.py <server_address> <n_port> <mode> <req_code> <file_received>")
        return
    try:
        server_address = sys.argv[1]

        n_port = int(sys.argv[2])

        mode = sys.argv[3]
        req_code = int(sys.argv[4])
        file_received = sys.argv[5]
    except ValueError:
        print('ERROR: check type of parameters')
        exit(-2)

    # UDP negotiation process
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as negotiation_socket:
        # Passive Mode
        if mode == 'P':
            requst = 'PASV'
            r_port = 0
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # r_port = int.from_bytes(data[1:3], byteorder='big')

                negotiation_socket.sendto(req_code.to_bytes(2, byteorder='big') + r_port.to_bytes(2,byteorder='big') + requst.encode() + b'\x00',(server_address, n_port))

                data, server = negotiation_socket.recvfrom(1024)

                if data[0] == 0:
                    print("Negotiation failed.")
                    return
                r_port = int.from_bytes(data[0:2], byteorder='big')
                client_socket.connect((server[0], r_port))
                with open(file_received, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        break
                client_socket.close()
                negotiation_socket.close()
        # Active Mode
        elif mode == 'A':
            requst = 'PORT'
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # r_port = int.from_bytes(data[1:3], byteorder='big')
                client_socket.bind(('', 0))
                r_port = client_socket.getsockname()[1]
                client_socket.listen(1)
                negotiation_socket.sendto(req_code.to_bytes(2, byteorder='big') + r_port.to_bytes(2,byteorder='big') + requst.encode() + b'\x00',(server_address, n_port))

                connection_socket, server_address = client_socket.accept()

                with open(file_received, 'wb') as f:
                    while True:
                        data = connection_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                client_socket.close()
                connection_socket.close()
                negotiation_socket.close()

if __name__ == '__main__':
    main()