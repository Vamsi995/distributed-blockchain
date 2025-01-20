import socket
import threading

def handle_client(client_socket):
    while True:
        data, addr = client_socket.recvfrom(1024)
        if not data:
            break
        print(f"Received from {addr}: {data.decode()}")
        # client_socket.sendto(b"Message received!", addr)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 8002))

    print("UDP server listening on localhost:8002")


    thread = threading.Thread(target=handle_client, args=(server_socket,))
    thread.start()

if __name__ == "__main__":
    start_server()