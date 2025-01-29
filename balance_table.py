class BalanceTable:

    def __init__(self):
        self.balance_table: dict[int: float] = {
            1: 10.0,
            2: 10.0,
            3: 10.0
        } 
    
    def __getitem__(self, index: int):
        return self.balance_table[index]
    
    def __setitem__(self, index: int, value: float):
        self.balance_table[index] = value 