import threading
from blockchain import Block, BlockChain
from balance_table import BalanceTable
from priority_queue import PriorityQueue
from utils import txt_to_object
import logging
import time

class CommunicationFactory:

    REPLIES = []
    CLIENTS = []


    def broadcast(self, message):
        for client in self.CLIENTS:
            time.sleep(3)
            client.send(bytes(message, "utf-8"))


    def receive(self, server, pqueue: PriorityQueue, block_chain: BlockChain, balance_table: BalanceTable, client_limit):
        while True:
            # Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(client.getpeername()))
            self.CLIENTS.append(client)

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client, pqueue, block_chain, balance_table, self))
            thread.start()

            if len(self.CLIENTS) == client_limit:
                break


    def handle(self, client, pqueue, block_chain: BlockChain, balance_table: BalanceTable, comm_factory):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(2048).decode("utf-8")
                message, piggy_back_obj = message.split("|")

                if message == "REQUEST":
                    lamport_clock = txt_to_object(piggy_back_obj)
                    logging.info(f"REQUEST Received from client {lamport_clock.proc_id}")
                    # Add to local queue
                    time.sleep(3)
                    client.send(bytes("REPLY|", "utf-8"))
                    pqueue.insert(lamport_clock)

                elif message == "REPLY":
                    # logging.info(f"REQUEST Received from client {lamport_clock.proc_id}")
                    # wait for all replies
                    comm_factory.REPLIES.append(client)

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
                comm_factory.CLIENTS.remove(client)
                client.close()
                break

