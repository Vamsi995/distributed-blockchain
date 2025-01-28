import socket
import argparse
import time
import threading
from logical_clock import LamportClock
from utils import txt_to_object
from priority_queue import PriorityQueue


clients = []
replies = []

def receive(server, queue):
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, queue))
        thread.start()

        if len(clients) == 1:
            break


def handle(client, pqueue):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode("utf-8")
            message, serialized_lamport_clock = message.split("|")
            lamport_clock = txt_to_object(serialized_lamport_clock)

            if message == "REQUEST":
                print(message)
                # Add to local queue
                client.send(bytes("REPLY|", "utf-8"))
                pqueue.insert(lamport_clock)

            elif message == "REPLY":
                # wait for all replies
                replies.append(client)

            elif message == "RELEASE":
                pqueue.delete(lamport_clock.proc_id)
                
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            break


def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    pqueue = PriorityQueue([])
    lamport_clock = LamportClock(args.client)

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, 8001))
    # clientsocket.send(bytes("Hello", "utf-8"))
    clients.append(clientsocket)


    thread = threading.Thread(target=handle, args=(clientsocket, pqueue))
    thread.start()
    

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    receive(server, pqueue)




    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)