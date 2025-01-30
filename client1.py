import socket
import argparse
from logical_clock import LamportClock
from blockchain import Block, BlockChain
from balance_table import BalanceTable
from priority_queue import PriorityQueue
import logging
from banking_server import BankingServer
from communication_factory import CommunicationFactory
from exceptions import Abort


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

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Listening on port: {}".format(port))

    comm_factory.receive(server, pqueue, block_chain, balance_table, limit)

    while True:
        comm_factory.REPLIES.clear()

        s = input("Transaction or Balance:\n")
        try:

            if s == "t":
                receiver = input("Transaction Receiver:\n")
                amount = input("Transaction Amount:\n")
                lamport_clock()
                banking_server.transcation(lamport_clock, pqueue, balance_table, block_chain, receiver, float(amount), comm_factory)
            elif s == "b":
                balance = banking_server.balance_request(args.client, balance_table)
                print("Current Balance is: {}".format(balance))
            elif s == "bl":
                print("Current Block Chain Information is: ")
                print(block_chain)
            elif s == "bt":
                print("Current Balance table is: ")
                print(balance_table)
            else:
                continue

        except Abort as e:
            print("Transaction Failed!")

        except Exception as e:
            print(e)
            raise Exception("Runtime Error!")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    args = parser.parse_args()
    run_server(args)