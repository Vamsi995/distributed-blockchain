import threading
from blockchain import Block, BlockChain
from balance_table import BalanceTable
from priority_queue import PriorityQueue
from utils import txt_to_object

class CommunicationFactory:


    def receive(self, server, pqueue: PriorityQueue, block_chain: BlockChain, balance_table: BalanceTable, clients, replies, client_limit):
        while True:
            # Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(str(address)))
            clients.append(client)

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client, pqueue, block_chain, balance_table, clients, replies))
            thread.start()

            if len(clients) == client_limit:
                break


    def handle(self, client, pqueue, block_chain: BlockChain, balance_table: BalanceTable, clients, replies):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(2048).decode("utf-8")
                message, piggy_back_obj = message.split("|")

                if message == "REQUEST":
                    lamport_clock = txt_to_object(piggy_back_obj)

                    # Add to local queue
                    client.send(bytes("REPLY|", "utf-8"))
                    pqueue.insert(lamport_clock)

                elif message == "REPLY":
                    # wait for all replies
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

