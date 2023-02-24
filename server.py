import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python server.py <req_code> <file_to_send>")
        return
    try:
        req_code = int(sys.argv[1])
        file_to_send = sys.argv[2]
    except ValueError:
        print('ERROR: check type of parameters')
        exit(-2)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as negotiation_socket:
        negotiation_socket.bind(('', 0))
        n_port = negotiation_socket.getsockname()[1]
        print(f"SERVER_PORT={n_port}")

        while True:
            data, client_address = negotiation_socket.recvfrom(1024)
            print(client_address)
            if len(data) != 9 or int.from_bytes(data[0:2], byteorder='big') != req_code:
                negotiation_socket.sendto(bytes([0]), client_address)
                continue

            r_port = int.from_bytes(data[2:4], byteorder='big')
            command = data[4:9]

            if command == b'PASV\x00':
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

                    server_socket.bind(('', 0))
                    server_socket.listen(1)
                    r_port = server_socket.getsockname()[1]
                    print('succ2')
                    negotiation_socket.sendto(r_port.to_bytes(2,byteorder='big'), client_address)
                    connection_socket, address = server_socket.accept()
                    with open(file_to_send, 'rb') as f:
                        connection_socket.sendall(f.read())
            elif command == b'PORT\x00':
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                    server_socket.connect((client_address[0], r_port))
                    with open(file_to_send, 'rb') as f:
                        server_socket.sendall(f.read())

if __name__ == '__main__':
    main()
