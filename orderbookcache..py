class OrderBookNode:
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume
        self.prev = None
        self.next = None

class OrderBookCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # Maps price to OrderBookNode
        self.head = OrderBookNode(0, 0)  # Dummy head
        self.tail = OrderBookNode(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, price):
        node = self.cache.get(price)
        if not node:
            return None
        # Move the node to the front of the list
        self._move_to_front(node)
        return node.volume

    def put(self, price, volume):
        node = self.cache.get(price)
        if node:
            # Update the node and move it to the front
            node.volume = volume
            self._move_to_front(node)
        else:
            # Add a new node to the front of the list
            if len(self.cache) >= self.capacity:
                # Remove the least recently used node
                self._remove(self.tail.prev)
            newNode = OrderBookNode(price, volume)
            self.cache[price] = newNode
            self._add_to_front(newNode)

    def _remove(self, node):
        # Remove a node from the list and the cache
        del self.cache[node.price]
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        # Add a node to the front of the list
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node):
        # Move an existing node to the front of the list
        self._remove(node)
        self._add_to_front(node)



class OrderBookCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.bids = {}  # Maps price to OrderBookNode for bids
        self.asks = {}  # Maps price to OrderBookNode for asks
        self.bid_head = OrderBookNode(0, 0)  # Dummy head for bids
        self.bid_tail = OrderBookNode(0, 0)  # Dummy tail for bids
        self.ask_head = OrderBookNode(0, 0)  # Dummy head for asks
        self.ask_tail = OrderBookNode(0, 0)  # Dummy tail for asks
        # Initialize dummy nodes for bid and ask lists
        self._init_list(self.bid_head, self.bid_tail)
        self._init_list(self.ask_head, self.ask_tail)

    def _init_list(self, head, tail):
        head.next = tail
        tail.prev = head

    def put_bid(self, price, volume):
        self._put(self.bids, self.bid_head, price, volume)

    def put_ask(self, price, volume):
        self._put(self.asks, self.ask_head, price, volume)

    def _put(self, cache, head, price, volume):
        node = cache.get(price)
        if node:
            node.volume = volume
            self._move_to_front(node, head)
        else:
            if len(cache) >= self.capacity:
                self._remove(self.tail.prev, cache)
            newNode = OrderBookNode(price, volume)
            cache[price] = newNode
            self._add_to_front(newNode, head)

    def get_top_bid(self):
        if self.bid_head.next != self.bid_tail:
            return self.bid_head.next.price, self.bid_head.next.volume
        return None, None

    def get_top_ask(self):
        if self.ask_head.next != self.ask_tail:
            return self.ask_head.next.price, self.ask_head.next.volume
        return None, None

    # Existing methods _remove, _add_to_front, _move_to_front remain the same but include the cache parameter for _remove

    def _remove(self, node, cache):
        # Adjusted to include cache parameter
        del cache[node.price]
        node.prev.next = node.next
        node.next.prev = node.prev