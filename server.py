import socket
import argparse
import time
import threading
import select


def transcation(lamport_time, queue, proc_id):
    
    # put yourself in the queue
    queue.append((lamport_time, proc_id))
    broadcast("REQUEST" + "." + str((lamport_time, proc_id)))

    # Maybe a timeout here - for failed case
    print("Waiting for replies: {}".format(len(replies)))
    while len(replies) != 2:
        # print("Waiting for replies: {}".format(len(replies)))

        continue
    

    # send request to all
    # receive reply from all

    while queue[0][1] != proc_id:
        continue

    update_balance_table()
    broadcast(block)
    
    # if my process id is on the top of queue

    # update balance table 
    # send block to other clients

    # send release to all
    broadcast(release)

    pass

def balance():
    pass


def broadcast(message):
    for client in clients:
        client.send(message)


clients = []
replies = []

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
            message = client.recv(1024).decode("utf-8")
            print(message)
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
        client.send(bytes(message, "utf-8"))

def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    queue = []
    lamport_time = 0


    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    client, address = server.accept()
    print("Connected with {}".format(str(address)))

    while True:
        readable, writable, exceptional = select.select([client], [], [], 1)

        if client in readable:
            data = client.recv(1024)
            if not data:
                break  # Connection closed
            print("Received:", data.decode())
        print("Active")
    # receive(server)

    s = input("Transaction or Balance")

    if s == "t":
        lamport_time += 1
        transcation(lamport_time, queue, args.client)
    else:
        balance()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)