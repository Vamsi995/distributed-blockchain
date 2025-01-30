from logical_clock import LamportClock
from priority_queue import PriorityQueue
from balance_table import BalanceTable
from blockchain import Block, BlockChain
from utils import object_to_txt
from exceptions import Abort

class BankingServer:


    def transcation(self, lamport_clock: LamportClock, queue: PriorityQueue, balance_table: BalanceTable, block_chain: BlockChain, receiver: str, amount: float, comm_factory):
        
        print(f"Current Balance: {self.balance_request(lamport_clock.proc_id, balance_table)}")

        # put yourself in the queue
        queue.insert(lamport_clock)

        # send request to all
        comm_factory.broadcast("REQUEST" + "|" + object_to_txt(lamport_clock))

        while len(comm_factory.REPLIES) != 2:
            # print(f"Waiting for reply: {len(replies)}")
            continue
        
        print("Received all replies: {}".format(len(comm_factory.REPLIES)))

        # if my process id is on the top of queue
        while queue.peek_top().proc_id != lamport_clock.proc_id:
            continue

        try:
            # Critical Section   
            block = self.critical_section(lamport_clock, balance_table, block_chain, receiver, amount)
            # update balance table 
            # send block to other clients
            # Should I receive ack or no?
            balance_table[int(block.sender)] -= block.amount
            balance_table[int(block.receiver)] += block.amount

            # Remove process from the top of my queue
            queue.extract_top()

            comm_factory.broadcast("BLOCK" + "|" + object_to_txt(block))

            # send release to all
            comm_factory.broadcast("RELEASE")

            print(f"Balance after transaction: {self.balance_request(lamport_clock.proc_id, balance_table)}")

        except Exception as e:
            print(e)
            broadcast("RELEASE", comm_factory.CLIENTS)
            raise Abort(e)

        


    def critical_section(self, lamport_clock, balance_table, block_chain, receiver, amount):
        if balance_table[lamport_clock.proc_id] < amount:
            raise Exception("Cannot perform transaction: Transaction amount is higher than the balance!")
        block = block_chain.insert(lamport_clock.proc_id, receiver, amount)
        return block 


    def balance_request(self, proc_id: int, balance_table: BalanceTable) -> float:
        return balance_table[proc_id]
