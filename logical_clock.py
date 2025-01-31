class LamportClock:
    
    def __init__(self, proc_id: int):
        self.logical_time = 0
        self.proc_id = proc_id
    
    def __call__(self):
        self.logical_time += 1
        print(f"Clock Value {self.logical_time - 1} -> {self.logical_time}")

    def __lt__(self, others):
        if self.logical_time == others.logical_time:
            return self.proc_id < others.proc_id
        return self.logical_time < others.logical_time

    def __repr__(self):
        return f"Lamport-TimeStamp({self.logical_time}, {self.proc_id})"
    
    def update_clock(self, logical_time: int):
        self.logical_time = max(logical_time, self.logical_time) + 1
        print(f"Clock Value {self.logical_time - 1} -> {self.logical_time}")

        