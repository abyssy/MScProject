from queue import Queue

q = Queue()
a = 10
q.put(a)
q.put(a)
while not q.empty():
    print(q.get())