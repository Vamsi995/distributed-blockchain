import socket
import threading
import argparse

def handle_client(client_socket):
    while True:
        data, addr = client_socket.recvfrom(1024)
        if not data:
            break
        print(f"Received from {addr}: {data.decode()}")
        # client_socket.sendto(b"Message received!", addr)

def start_server(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", args.port))

    print("UDP server listening on localhost:8001")

    thread = threading.Thread(target=handle_client, args=(server_socket,))
    thread.start()

    server_socket.sendto(b"Message received!", ('localhost', 8002))
    server_socket.sendto(b"Message received!", ('localhost', 8003))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    args = parser.parse_args()
    start_server(args)