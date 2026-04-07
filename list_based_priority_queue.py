class Node:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
        self.prev = None
        self.next = None


class PriorityQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value, priority):
        node = Node(value, priority)
        cur = self.head
        while cur and cur.priority >= priority:
            cur = cur.next
        if cur is None:
            if self.tail:
                self.tail.next = node
                node.prev = self.tail
                self.tail = node
            else:
                self.head = self.tail = node
        else:
            node.next = cur
            node.prev = cur.prev
            if cur.prev:
                cur.prev.next = node
            else:
                self.head = node
            cur.prev = node
        self.size += 1

    def dequeue(self):
        if not self.head:
            raise IndexError("порожня черга")
        node = self.head
        self.head = node.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return node.value, node.priority

    def view(self):
        cur = self.head
        print(f"черга:")
        while cur:
            print(f"значення: {cur.value}, пріоритет: {cur.priority}")
            cur = cur.next
