from swap import swap

def less(x, y):
    return x < y

def less_key(x, y):
    return x.key < y.key

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * (i + 1)

def parent(i):
    return (i-1) / 2


# Student code -- fill in all the methods that have pass as the only statement
class Heap:
    def __init__(self, data,
                 less = less):
        self.data = data
        self.less = less
        self.build_min_heap()
    
    def __repr__(self):
        return repr(self.data)
    
    def minimum(self):
        return self.data[0]
    
    def insert(self, obj):
        self.data.append(obj)
        self.build_min_heap()
        pass
    
    def extract_min(self):
        size = len(self.data) - 1
        if size < 1:
            print "error"
        min = self.data[0]
        self.data.pop(0)
        size = size - 1
        self.min_heapify(0)
        return min
 
    def min_heapify(self, i):
        l = left(i)
        r = right(i)
        size = len(self.data) - 1
        if l <= size and self.data[l].key < self.data[i].key:
            smallest = l
        else:
            smallest = i
        if r <= size and self.data[r].key < self.data[smallest].key:
            smallest = r
        if smallest != i:
            swap(self.data,i, smallest)
            self.min_heapify(smallest)
        return self.data

    def build_min_heap(self):
        size = len(self.data)
        for i in range((size/2) - 1,-1, -1):
            self.min_heapify(i)

class PriorityQueue:
    def __init__(self, less=less_key):
        self.heap = Heap([], less)
    
    def __repr__(self):
        return repr(self.heap)
    
    def push(self, obj):
        self.heap.insert(obj)
    
    def pop(self):
        return self.heap.extract_min()

if __name__ == "__main__":
    # unit tests here
    heap = PriorityQueue(less)
    heap.push(4)
    heap.push(5)
    heap.push(2)
    heap.push(1)
    heap.push(9)
    heap.push(11)
    heap.push(34)
    heap.push(3)
    heap.push(6)
    heap.push(7)
    heap.pop()
    print heap

pass