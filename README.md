# Distributed Mutual Exclusion with Blockchain-Based Transactions

## Overview

This repository implements a **distributed mutual exclusion** system using **Lamport's Distributed Mutual Exclusion Algorithm**, where multiple clients maintain a **blockchain-based transaction ledger** and ensure **safe money transfers** via mutual exclusion. Each client holds a **local copy of the blockchain** and a **balance table**, ensuring consistent updates across the distributed system. The project simulates a **banking system** where clients transfer funds securely while maintaining a globally ordered transaction history.

<img width="1329" alt="image" src="https://github.com/user-attachments/assets/1d56cbd0-6817-4da9-a18a-76e31ddddede" />



## Setup & Execution

### Prerequisites
- Python 3.10

### Running the Project
1. Start multiple client instances (either on different machines or using multiple processes on a single machine).

```bash
python client1.py -port <portno> -client <clientid> -balance <balance amount>
```

Initialize all the clients in the following order:

```bash
python client1.py -port 8001 -client 1 -balance 10.0
```

```bash
python client1.py -port 8002 -client 2 -balance 10.0
```

```bash
python client1.py -client 3 -balance 10.0
```

Execute the client commands in order, because each client connects to all the other clients on startup.

2. Each client initializes with **$10** in balance, and a client id which acts as the process id.
3. Use the interface to:
   - Perform **money transfers** between clients.
   - Query **balances**.
   - Print **blockchain history**.
4. Observe logs for **message passing**, **clock updates**, and **mutual exclusion handling**.


## Features

- **Blockchain-based transaction history**: Each block contains a single financial transaction with cryptographic hash pointers ensuring data integrity.
- **Lamport's Mutual Exclusion Algorithm**: Clients coordinate access to the blockchain using Lamport timestamps.
- **Concurrency Control**: Transactions execute sequentially across distributed clients to prevent race conditions.
- **TCP/UDP Communication**: Clients communicate over a network using message-passing techniques.
- **Balance Verification**: Transactions are validated before execution, ensuring sufficient funds exist.
- **Logging & Debugging**: Console logs track message exchanges, logical clock updates, and transactions.

## Implementation Details

### Clients
Each client maintains:
- A **blockchain** storing transactions.
- A **balance table** tracking all client balances.
- A **Lamport logical clock** for ordering transactions.
- A **Priority Request Queue** for ordering requests based on lamport logical clock time.
- A **Banking Server** instance for performing transactions and balance requests.
- A **Communication Factory** for message passing abstraction.

### Transactions
- **Transfer Transaction**: Moves money between clients and updates the blockchain.
- **Balance Query**: Returns the current balance of a client (does not modify the blockchain).

### Mutual Exclusion
- Clients use Lamport's algorithm to request exclusive access before modifying the blockchain.
- If a client lacks sufficient funds, the transaction is **aborted**.

### Communication
- Clients connect via **TCP** sockets.
- Messages include transaction requests, acknowledgments, and blockchain updates.

### Example Transaction Flow
1. **Client A requests to send $4 to Client B**.
2. **Lamport's mutual exclusion protocol** ensures ordered execution.
3. **If A has sufficient funds**, the transaction is added to the blockchain.
4. The transaction block is sent to other clients.
5. **All clients update their local copies of the blockchain and balance tables**.
6. The system logs messages, timestamps, and transaction details.

## Notes
- Transactions are **totally ordered** using **Lamport timestamps**.
- The project can run on multiple machines or simulate distribution using multiple processes.
- Future improvements can include **Byzantine Fault Tolerance**, **leader election**, or **enhanced consensus mechanisms**.

## Author

- [Sai Vamsi Alisetti](https://github.com/Vamsi995) 
