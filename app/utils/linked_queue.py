import pickle


class Node:
    """
    链表节点类
    """

    def __init__(self, data):
        """
        初始化节点
        :param data: 节点存储的数据
        """
        self.data = data
        self.next = None


class LinkedQueue:
    """
    基于链表实现的队列
        特性：
    - 先进先出(FIFO)原则
    - 支持入队(enqueue)和出队(dequeue)操作
    - 可以查看队首元素(peek)
    - 提供队列长度和空状态检查
        示例：
    >>> queue = LinkedQueue()
    >>> queue.enqueue(1)
    >>> queue.dequeue()
    1
    """

    def __init__(self):
        """
        初始化队列
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.filename = 'queue_data.pkl'

    def is_empty(self) -> bool:
        """
        检查队列是否为空
        :return: 如果队列为空返回 True，否则返回 False
        """
        return self.size == 0

    def enqueue(self, item) -> None:
        """
        入队操作
        :param item: 要入队的元素
        """
        new_node = Node(item)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        """
        出队操作
        :return: 出队的元素
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return item

    def peek(self):
        """
        查看队首元素
        :return: 队首元素
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.head.data

    def save_to_file(self, filename: str = None) -> None:
        """
        将队列数据保存到文件
        :param filename: 要保存的文件名
        """
        if filename is None:
            filename = self.filename
        data = []
        current = self.head
        while current:
            data.append(current.data)
            current = current.next

        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        f.close()

    @classmethod
    def load_from_file(cls, filename: str = None) -> 'LinkedQueue':
        """
        从文件加载队列数据
        :param filename: 要加载的文件名
        :return: 加载后的队列实例
        """
        if filename is None:
            filename = self.filename
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        f.close()

        queue = cls()
        for item in data:
            queue.enqueue(item)

        return queue

    def __len__(self) -> int:
        """
        获取队列长度
        :return: 队列长度
        """
        return self.size

    def __str__(self) -> str:
        """
        打印队列
        :return: 队列字符串表示
        """
        if self.is_empty():
            return "Queue: empty"
        current = self.head
        items = []
        while current:
            items.append(str(current.data))
            current = current.next
        return "Queue: " + " -> ".join(items)
