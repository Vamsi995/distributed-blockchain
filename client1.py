import socket
import argparse
import time
import threading
from logical_clock import LamportClock
from utils import object_to_txt, txt_to_object
from blockchain import Block, BlockChain
from balance_table import BalanceTable
from priority_queue import PriorityQueue


clients = []
replies = []

def transcation(lamport_clock: LamportClock, queue: PriorityQueue, balance_table: BalanceTable, block_chain: BlockChain, receiver: str, amount: float):
    
    # put yourself in the queue
    queue.insert(lamport_clock)

    # send request to all
    broadcast("REQUEST" + "|" + object_to_txt(lamport_clock))


    # global replies
    # receive reply from all
    while len(replies) != 2:
        # global replies
        # print("Waiting for replies: {}".format(len(replies)))
        continue
    
    print("Received all replies: {}".format(len(replies)))

    # if my process id is on the top of queue
    while queue.peek_top().proc_id != lamport_clock.proc_id:
        continue

    # Critical Section
   
    block = critical_section(lamport_clock, balance_table, block_chain, receiver, amount)
    # update balance table 
    # send block to other clients
     # Should I receive ack or no?
    balance_table[int(block.sender)] -= block.amount
    balance_table[int(block.receiver)] += block.amount

    broadcast("BLOCK" + "|" + object_to_txt(block))


    # send release to all
    broadcast("RELEASE")


def critical_section(lamport_clock, balance_table, block_chain, receiver, amount):

    if balance_table[lamport_clock.proc_id] < amount:
        raise Exception("Cannot perform transaction: Transaction amount is higher than the balance!")

    block = block_chain.insert(lamport_clock.proc_id, receiver, amount)

    return block 

    




def balance_request(proc_id: int, balance_table: BalanceTable):
    return balance_table[proc_id]


def broadcast(message):
    for client in clients:
        client.send(message)




def receive(server, pqueue, block_chain, balance_table):
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        global clients
        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, pqueue, block_chain, balance_table))
        thread.start()
        
        print(len(clients))
        if len(clients) == 2:
            break


def handle(client, pqueue, block_chain: BlockChain, balance_table: BalanceTable):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(2048).decode("utf-8")
            message, piggy_back_obj = message.split("|")

            if message == "REQUEST":
                lamport_clock = txt_to_object(piggy_back_obj)

                # Add to local queue
                client.send("REPLY")
                pqueue.insert(lamport_clock)

            elif message == "REPLY":
                # wait for all replies
                global replies
                replies.append(client)

            elif message == "RELEASE":
                lamport_clock = txt_to_object(piggy_back_obj)
                pqueue.delete(lamport_clock.proc_id)

            elif message == "BLOCK":
                block: Block = txt_to_object(piggy_back_obj)
                block_chain.update_head(block)
                balance_table[int(block.sender)] -= block.amount
                balance_table[int(block.receiver)] += block.amount
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            break


def broadcast(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))

def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    lamport_clock = LamportClock(args.client)
    block_chain = BlockChain()
    balance_table = BalanceTable()
    pqueue = PriorityQueue([])


    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    receive(server, pqueue, block_chain, balance_table)

    while True:
        global replies
        replies.clear()

        s = input("Transaction or Balance:\n")


        if s == "t":
            receiver = input("Transaction Receiver:\n")
            amount = input("Transaction Amount:\n")
            lamport_clock()
            transcation(lamport_clock, pqueue, balance_table, block_chain, receiver, float(amount))
        elif s == "b":
            balance = balance_request(args.client, balance_table)
            print("Current Balance is: {}".format(balance))
        else:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)