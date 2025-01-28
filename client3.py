import socket
import argparse
import time
import threading
from utils import txt_to_object


clients = []

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

        if len(clients) == 1:
            break


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode("utf-8")
            message, serialized_lamport_clock = message.split("|")
            lamport_clock = txt_to_object(serialized_lamport_clock)
            print(message)
            if message == "REQUEST":
                # Add to local queue
                client.send(bytes("REPLY|", "utf-8"))
                # queue.append(lamport_clock)

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


def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    queue = []

    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket1.connect((host, 8001))

    clients.append(clientsocket1)

    thread = threading.Thread(target=handle, args=(clientsocket1,))
    thread.start()

    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2.connect((host, 8002))

    clients.append(clientsocket2)

    thread = threading.Thread(target=handle, args=(clientsocket2,))
    thread.start()

    input("Waiting")
   




    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)