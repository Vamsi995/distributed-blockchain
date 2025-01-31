from communication_factory import CommunicationFactory
from banking_server import BankingServer
from logical_clock import LamportClock
from priority_queue import PriorityQueue
from balance_table import BalanceTable
from blockchain import BlockChain
from exceptions import Abort

def client_interface(args, comm_factory: CommunicationFactory, banking_server: BankingServer, lamport_clock: LamportClock, pqueue: PriorityQueue, balance_table: BalanceTable, block_chain: BlockChain):
    print(f"Balance: ${balance_table[lamport_clock.proc_id]}")
    while True:
        comm_factory.REPLIES.clear()

        s = input("Transaction or Balance:\n")
        try:

            if s == "t":
                receiver = input("Transaction Receiver:\n")
                amount = input("Transaction Amount:\n")
                banking_server.transcation(lamport_clock, pqueue, balance_table, block_chain, receiver, float(amount), comm_factory)
                print("Transaction SUCCESS!")
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
            print("Transaction FAILED!")

        except Exception as e:
            print(e)
            raise Exception("Runtime Error!")