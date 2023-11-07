class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left.values)
        if self.right != None:
            size += len(self.right.values)
        return size
    
    def lookup(self, key):
        if self.key == key:
            return self.values
        if key < self.key and self.left != None:
            ret = self.left.lookup(key)
            if ret:
                return ret
        if key > self.key and self.right != None:
            ret = self.right.lookup(key)
            if ret:
                return ret
        return []
        
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)
        curr = self.root
        while True:
            if key < curr.key:
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                assert curr.key == key
                break
        curr.values.append(val)
    
    def __dump(self, node):
        if node == None:
            return
        
        print(node.key, ":", node.values)
        self.__dump(node.left)   
        self.__dump(node.right)            
    def dump(self):
        self.__dump(self.root)
    
    def __getitem__(self, lookup):
        return self.root.lookup(lookup)
        
        
    