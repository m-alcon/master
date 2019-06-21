import numpy as np
import time

class Node(object):

    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value

    def __repr__(self):
        return "Node With key: %d, value: %d" % (self.key, self.value)

    def copy(self, node):
        if node:
            if node.left:
                self.left = node.left
            else:
                self.left = None
            if node.right:
                self.right = node.right
            else:
                self.right = None
            if node.key:
                self.key = node.key
            else:
                self.key = None
            if node.value:
                self.value = node.value
            else:
                self.value = None

    def insert(self, key, value):
        node, parent = self.lookup(key, self)
        if node is None:
            if self.key is None:
                self.key = key
                self.value = value
            else:
                if key < self.key:
                    if self.left is None:
                        self.left = Node(key=key, value=value)
                    else:
                        self.left.insert(key, value)
                else:
                    if self.right is None:
                        self.right = Node(key=key, value=value)
                    else:
                        self.right.insert(key, value)
        else:
            node.value = value

    def lookup(self, key, parent=None):
        if self.key is None:
            return None, None
        if key < self.key:
            if self.left is None:
                return None, None
            return self.left.lookup(key, self)
        elif key > self.key:
            if self.right is None:
                return None, None
            return self.right.lookup(key, self)
        else:
            return self, parent

    def children_count(self):
        count = 0
        if self.left:
            count += 1
        if self.right:
            count += 1
        return count

    def descendant_count(self):
        count = None
        if self.left:
            count += 1 + self.left.descendant_count()
        if self.right:
            count += 1 + self.right.descendant_count()
        return count
    
    def search_greatest(self):
        actual_node = self
        while (actual_node.right != None):
            actual_node = actual_node.right
        return actual_node

    def delete(self, key):
        node, parent = self.lookup(key)
        if node:
            children_count = node.children_count()
            if children_count == 0:
                # If node has no children then remove it
                if not parent:
                    node.key = None
                    node.value = None
                elif parent.left is node:
                    parent.left = None
                else:
                    parent.right = None
                del node
            elif children_count == 1:
                if not parent:
                    if node.left:
                        self.copy(node.left)
                    else:
                        self.copy(node.right)
                else:
                    if node.left:
                        child = node.left
                    else:
                        child = node.right
                    if parent:
                        if parent.left is node:
                            parent.left = child
                        else:
                            parent.right = child
                    del node
            else:
                if not parent:
                    if node.left and node.right:
                        left = node.left
                        right = node.right
                        node.copy(node.left.search_greatest())
                        node.left = left
                        node.right = right
                    elif node.left:
                        node.copy(node.left)
                    else:
                        node.copy(node.right)
                else:
                    parent = node
                    successor = node.right
                    while successor.left:
                        parent = successor
                        successor = successor.left
                    node.key = successor.key
                    if parent.left == successor:
                        parent.left = successor.right
                    else:
                        parent.right = successor.right

    def inorder_print(self):
        if self.left:
            self.left.inorder_print()
        print(self.key, self.value)
        if self.right:
            self.right.inorder_print()

    def print_each_level(self):
        # Start off with root node
        thislevel = [self]

        # While there is another level
        while thislevel:
            nextlevel = list()
            # Print all the nodes in the current level, and store the next level in a list
            for node in thislevel:
                print(node.key, node.value)
                if node.left:
                    nextlevel.append(node.left)
                if node.right:
                    nextlevel.append(node.right)
            print()
            thislevel = nextlevel

    def compare_trees(self, node):
        if node is None:
            return False
        if self.key != node.key or self.value != node.value:
            return False
        res = True
        if self.left is None:
            if node.left:
                return False
        else:
            res = self.left.compare_trees(node.left)
        if self.right is None:
            if node.right:
                return False
        else:
            res = self.right.compare_trees(node.right)
        return res

    def tree_key(self):
        # we use a stack to traverse the tree in a non-recursive way
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node.copy(node.left)
            else:  # we are returning so we pop the node and we yield it
                node.copy(stack.pop())
                yield node.key
                node.copy(node.right)


class Dictionary(object):
    def __init__(self):
        self.__tree = Node()

    def __str__(self):
        self.__tree.inorder_print()
        return ''

    def __getitem__(self, key):
        node, parent = self.__tree.lookup(key)
        res = None
        if node:
            res = node.value
        return res

    def __setitem__(self, key, value):
        return self.__tree.insert(key, value)

    def __delitem__(self, key):
        self.__tree.delete(key)

    def empty(self):
        return self.__tree.key is None


if __name__ == '__main__':
    test = Dictionary()
    test[0.54786] = [True]
    print(test[0.54786])

    test = Dictionary()
    test['test'] = {True}
    print(test['test'])

    test = Dictionary()
    test[['array','of','whatever',0]] = (True)
    print(test[['array','of','whatever',0]])

    test = Dictionary()
    test[['array','of','whatever',0]] = True
    print(test[['array']])

    bst_dict = Dictionary()
    py_dict = {}
    iterations = 1000

    bst = {'insertion': 0, 'deletion':0 ,'search': 0}
    py = dict(bst)
    keys = []
    for i in range(iterations):
        k = np.random.randint(10000000)
        keys.append(k)
        v = np.random.randint(10000000)
        start = time.time()
        bst_dict[k] = v
        bst['insertion'] += time.time() - start
        start = time.time()
        py_dict[k] = v
        py['insertion'] += time.time() - start
    
    np.random.shuffle(keys)
    for k in keys:
        start = time.time()
        v = bst_dict[k]
        bst['search'] += time.time() - start
        start = time.time()
        v = py_dict[k]
        py['search'] += time.time() - start
    
    np.random.shuffle(keys)
    for k in keys:
        start = time.time()
        del bst_dict[k]
        bst['deletion'] += time.time() - start
        start = time.time()
        py_dict.pop(k)
        py['deletion'] += time.time() - start
    
    for k in bst.keys():
        print('BST %s:'%k, bst[k]/iterations)
        print('Python %s:'%k, py[k]/iterations)
    
    

