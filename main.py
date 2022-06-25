import sys


class Node(object):
    '''
    Base node object.
    Each node stores keys and values. Keys are not unique to each value, and
    as such values are stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    '''

    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        '''
        Adds a key-value pair to the node.
        '''
        # for 1st key
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        # for next key onward, this loop checks where to put the pey in the list
        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break

            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        '''
        Splits the node into two and stores them as child nodes.
        '''
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order / 2)

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        '''
        Returns True if the node is full.
        '''
        return len(self.keys) == self.order  # checking if key number is equal to order

    def show(self, counter=0):
        '''
        Prints the keys at each level.
        '''
        print(counter, str(self.keys))

        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)


class BPlusTree(object):
    '''
    B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split
    occurs, a key will 'float' upwards and be inserted into the parent node to
    act as a pivot.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    '''

    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        '''
        For a given node and key, returns the index where the key should be
        inserted and the list of values at that index.
        '''
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        '''
        For a parent and child node, extract a pivot from the child to be
        inserted into the keys of the parent. Insert the values from the child
        into the values of the parent.
        '''
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        '''
        Inserts a key-value pair after traversing to a leaf node. If the leaf
        node is full, split the leaf node into two.
        '''
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        if child.is_full():
            child.split()

            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        '''
        Returns a value for a given key, and None if the key does not exist.
        '''
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        '''
        Prints the keys at each level.
        '''
        self.root.show()


def demo_bplustree():
    print('Initializing B+ tree...')
    # order here is the number of data in each node
    bplustree = BPlusTree(order=4)

    f = open("input1.txt", encoding='utf-8-sig')  # to avoid BOM=\ufeff character

    datasize = int(f.readline())
    print(datasize)
    print('\nInserting key from file...')
    for i in range(datasize):
        f1 = f.readline().strip('\n')
        f2 = f.readline().strip('\n')

        bplustree.insert(f1, f2)
    bplustree.show()

    print('\nRetrieving values with key zoo...')
    print(bplustree.retrieve('zone'))
    while True:
        x = input()
        if x == "0":
            break
        print(bplustree.retrieve(x))


if __name__ == '__main__':
    print('\n')
    demo_bplustree()
