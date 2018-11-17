class TreeNode(object): 
    def __init__(self, vertex): 
        self.vertex = vertex 
        self.left = None
        self.right = None
        self.height = 1
        
def compare(p, q):
    px, py = p.coordinates
    qx, qy = q.coordinates
    if py != qy:
        return py - qy
    return qx - px

class VertexTree(object): 
    def __init__(self):
        self.root = None
        
    def _insert(self, root, vertex): 
        if not root: 
            return TreeNode(vertex) 
        elif compare(vertex, root.vertex) < 0: 
            root.left = self._insert(root.left, vertex) 
        elif compare(vertex, root.vertex) > 0:
            root.right = self._insert(root.right, vertex) 
        else:
            # root equal vertex
            root.vertex.involves_both = True
            edges = vertex.find_edges_w_origin()
            for e in edges:
                e.origin = root.vertex
            root.vertex.event_type = 4
            return root
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and compare(vertex, root.vertex) < 0: 
            return self.rightRotate(root) 
        if balance < -1 and compare(vertex, root.vertex) > 0: 
            return self.leftRotate(root) 
        if balance > 1 and compare(vertex, root.vertex) > 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and compare(vertex, root.vertex) < 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 
       
    def insert(self, vertex):
        self.root = self._insert(self.root, vertex)
  
    def leftRotate(self, z): 
        y = z.right 
        T2 = y.left 
        y.left = z 
        z.right = T2 
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
        return y 
  
    def rightRotate(self, z): 
  
        y = z.left 
        T3 = y.right 
        y.right = z 
        z.left = T3 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
        return y 
  
    def getHeight(self, root): 
        if not root: 
            return 0
        return root.height 
  
    def getBalance(self, root): 
        if not root: 
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right) 
  
    def _inOrder(self, root, result): 
        if not root: 
            return
  
        self._inOrder(root.left, result) 
        result.append(root.vertex)
        self._inOrder(root.right, result)
        
    def inOrder(self):
        result = []
        self._inOrder(self.root, result)
        return result
    
    def delete(self, vertex):
        self.root = self._delete(self.root, vertex)
        

    def _delete(self, root, key): 
        if not root: 
            return root 
        elif compare(key, root.vertex) < 0: 
            root.left = self._delete(root.left, key) 
        elif compare(key, root.vertex) > 0: 
            root.right = self._delete(root.right, key) 
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
            temp = self.getMinValueNode(root.right) 
            root.vertex = temp.vertex 
            root.right = self._delete(root.right, 
                                      temp.vertex) 
        if root is None: 
            return root 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.rightRotate(root) 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.leftRotate(root) 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 

    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 
  
        return self.getMinValueNode(root.left) 
    
    def is_empty(self):
        return self.root is None
    
    def find(self, vertex):
        return self._find(self.root, vertex)
    
    def _find(self, root, vertex):
        if not root: 
            return None
        elif compare(vertex, root.vertex) < 0: 
            return self._find(root.left, vertex)
        elif compare(vertex, root.vertex) > 0:
            return self._find(root.right, vertex) 
        else:
            return root
        
    def find_or_insert(self, vertex):
        find_res = self.find(vertex)
        if find_res is not None:
            return find_res
        self.insert(vertex)
    