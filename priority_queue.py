from __future__ import annotations
from typing import TypeVar, Generic
from logical_clock import LamportClock

T = TypeVar('T', bound=LamportClock)


class PriorityQueue(Generic[T]):


    def __init__(self, data: list[T]):
        self.data = data

    def build_heap(self):
        last_parent = ((len(self.data) - 1) - 1) // 2
        for i in range(last_parent, -1, -1):
            self.sift_down(i)

    def insert(self, node: T):
        self.data.append(node)
        self.sift_up(len(self.data) - 1)

    def delete(self, proc_id: int):
        
        self.data = list(filter(lambda clock: clock.proc_id != proc_id, self.data))
        self.sift_down(0)
        

    def peek_top(self):
        
        if len(self.data) != 0:
            return self.data[0]

        return None

    def sift_up(self, i: int):
        parent = (i - 1) // 2
        
        while parent >= 0 and self.data[i] < self.data[parent]:
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent
            parent = (i - 1) // 2

    def sift_down(self, i: int):
        
        l = 2 * i + 1
        r = 2 * i + 2

        smallest = i

        if l < len(self.data) and self.data[l] < self.data[smallest]:
            smallest = l

        if r < len(self.data) and self.data[r] < self.data[smallest]:
            smallest = r
        
        if smallest != i:
            self.data[smallest], self.data[i] = self.data[i], self.data[smallest]
            self.sift_down(smallest)


    def extract_top(self) -> T:

        if len(self.data) == 0:
            return None
        
        self.data[0], self.data[-1] = self.data[-1], self.data[0]

        out = self.data.pop()

        self.sift_down(0)

        return out

# if __name__ == "__main__":

#     queue = PriorityQueue([])
#     a = LamportClock(1)
#     a()
#     a()
#     b = LamportClock(2)
#     b()
#     b()

#     queue.insert(a)
#     queue.insert(b)

#     print(queue.peek_top())