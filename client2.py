import socket
import argparse
import threading
from logical_clock import LamportClock
from priority_queue import PriorityQueue
from blockchain import BlockChain
from balance_table import BalanceTable
from banking_server import BankingServer
from communication_factory import CommunicationFactory
from interface import client_interface
import logging

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


    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, 8001))
    comm_factory.CLIENTS.append(clientsocket)

    print("Connected with {}".format(clientsocket.getpeername()))

    thread = threading.Thread(target=comm_factory.handle, args=(clientsocket, pqueue, block_chain, balance_table, comm_factory, lamport_clock))
    thread.start()
    

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Listening on port: {}".format(port))

    comm_factory.receive(server, pqueue, block_chain, balance_table, limit, lamport_clock)

    client_interface(args, comm_factory, banking_server, lamport_clock, pqueue, balance_table, block_chain)
    

    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')


    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)