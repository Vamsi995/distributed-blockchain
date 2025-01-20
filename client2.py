import socket
import argparse
import time


def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number


    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        time.sleep(5)
        # s.sendto(b"Hello from Process {args.client}", (host, port))
        data, _ = s.recvfrom(1024)
        print(f"Process {args.client} received: {data.decode()}")


    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    #     server_socket.bind((host, port))
    #     server_socket.listen()

    #     clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     time.sleep(5)
    #     clientsocket1.connect((host, client_map[args.client][0]))
    #     clientsocket2.connect((host, client_map[args.client][1]))

    #     clientsocket1.sendall(bytes("hello", "utf-8"))

    #     print(f'Server listening on {host}:{port}')
    #     conn, addr = server_socket.accept()
    #     with conn:
    #         data = conn.recv(1024)
    #     # while True:
        #     print("yes")

        #     print(conn, addr)
        #     with conn:
        #         print(f'Connected by {addr}')
        #         while True:
        #             data = conn.recv(2048)
        #             print(data)
        #             # if not data:
        #             #     break
        #             print(f'Received: {data.decode()}')
        #             # conn.sendall(data)  # Echo back the data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)