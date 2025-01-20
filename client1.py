import socket
import argparse
import time
import threading



def transcation(s: socket.socket):
    
    # put yourself in the queue
    # send request to all
    # receive reply from all
    # if my process id is on the top of queue

    # update balance table 
    # send block to other clients

    # send release to all

    pass

def balance():
    pass


clients = []
replies = []

client_socket = 

def receive(server):
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        # client.send('NICK'.encode('ascii'))
        # nickname = client.recv(1024).decode('ascii')
        # nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        # print("Nickname is {}".format(nickname))
        # broadcast("{} joined!".format(nickname).encode('ascii'))
        # client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        if len(clients) == 2:
            break


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message == "REQUEST":
                # Add to local queue
                client.send("REPLY")
            elif message == "REPLY":
                # wait for all replies
                replies.append(client)
                if len(replies) == 2:
                   # "Perform action"
                    # append to block chain
                    # send block to other processes
                    # broadcast("block")
                    # broadcast("release")
                    pass
            elif message == "RELEASE":
                # remove process from the queue.
                pass
                
            # broadcast(message)
        except:
            # Removing And Closing Clients
            # index = clients.index(client)
            # clients.remove(client)
            client.close()
            # nickname = nicknames[index]
            # broadcast('{} left!'.format(nickname).encode('ascii'))
            # nicknames.remove(nickname)
            break


def broadcast(message):
    for client in clients:
        client.send(message)

def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number


    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    receive(server)

    action = input("Action: Transaction or Balance")


    if action == "t":
        broadcast("REQUEST")
    else:
        print("Balance Table")

        # data, _ = s.recvfrom(1024)
        # print(f"Process {args.client} received: {data.decode()}")


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