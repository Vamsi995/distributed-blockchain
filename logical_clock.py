class LamportClock:
    
    def __init__(self, proc_id: int):
        self.logical_time = 0
        self.proc_id = proc_id
    
    def __call__(self):
        self.logical_time += 1

    def __lt__(self, others):
        if self.logical_time == others.logical_time:
            return self.proc_id < others.proc_id
        return self.logical_time < others.logical_time

    def __repr__(self):
        return f"Lamport-TimeStamp({self.logical_time}, {self.proc_id})"