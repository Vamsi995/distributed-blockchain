import socket
import argparse
import time
import threading
from logical_clock import LamportClock
from utils import txt_to_object, broadcast, object_to_txt
from priority_queue import PriorityQueue
from blockchain import Block, BlockChain
from balance_table import BalanceTable
from banking_server import BankingServer
from communication_factory import CommunicationFactory

def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    lamport_clock = LamportClock(args.client)
    block_chain = BlockChain()
    balance_table = BalanceTable()
    pqueue = PriorityQueue([])
    banking_server = BankingServer()
    comm_factory = CommunicationFactory()
    limit = 2


    clients = []
    replies = []

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, 8001))
    clients.append(clientsocket)


    thread = threading.Thread(target=comm_factory.handle, args=(clientsocket, pqueue, block_chain, balance_table, clients, replies))
    thread.start()
    

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    comm_factory.receive(server, pqueue, block_chain, balance_table, clients, replies, limit)

    while True:
        replies.clear()

        s = input("Transaction or Balance:\n")

        if s == "t":
            receiver = input("Transaction Receiver:\n")
            amount = input("Transaction Amount:\n")
            lamport_clock()
            banking_server.transcation(lamport_clock, pqueue, balance_table, block_chain, receiver, float(amount), replies, clients)
        elif s == "b":
            balance = banking_server.balance_request(args.client, balance_table)
            print("Current Balance is: {}".format(balance))
        else:
            continue



    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)