from segment import Segment

class TreeNode(object): 
    def __init__(self, segment):
        # val = seg
        self.segment = segment
        self.left = None
        self.right = None
        self.height = 1
    
    def copy(self, node):
        self.segment = node.segment
        self.left = node.left
        self.right = node.right
        self.height = node.height
       
        
class StatusStructure(object): 
    def __init__(self):
        self.root = None
        
    def _insert(self, root, point, segment): 
        if not root: 
            return TreeNode(segment) 
        elif root.segment.compare_lower(point, segment) > 0: 
            root.left = self._insert(root.left, point, segment) 
        else:
            root.right = self._insert(root.right, point, segment) 
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and root.segment.compare_lower(point, segment) > 0: 
            return self.rightRotate(root) 
        if balance < -1 and root.segment.compare_lower(point, segment) < 0: 
            return self.leftRotate(root) 
        if balance > 1 and root.segment.compare_lower(point, segment) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and root.segment.compare_lower(point, segment) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 
    
    def insert(self, point, segments):
        if type(segments) != list:
            segments = [segments]
        
        for segment in segments:
            self.root = self._insert(self.root, point, segment)
  
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
        result.append(root)
        self._inOrder(root.right, result)
        
    def inOrder(self):
        result = []
        self._inOrder(self.root, result)
        return result
    
    def delete(self, point, segment):
        self.root = self._delete(self.root, point, segment) 
    
    def delete_list(self, point, segments):
        for segment in segments:
            self.delete(point, segment)
    
    def _delete(self, root, point, segment): 
        if not root: 
            return root 
        elif root.segment.compare_upper(point, segment) > 0: 
            root.left = self._delete(root.left, point, segment) 
        elif root.segment.compare_upper(point, segment) < 0: 
            root.right = self._delete(root.right, point, segment) 
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
            root.segment = temp.segment 
            root.right = self._delete(root.right, point, temp.segment) 
                                      
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
       
    def find_segments_contain(self, point):
        L = []
        C = []
        L_C = []
        self._find_segments_contain(self.root, point, L, C, L_C)
        return L, C, L_C
    
    def _find_segments_contain(self, root, point, L, C, L_C):
        if not root: 
            return 
        elif root.segment.point_location(point) > 0: 
            self._find_segments_contain(root.right, point, L, C, L_C) 
        elif root.segment.point_location(point) < 0: 
            self._find_segments_contain(root.left, point, L, C, L_C) 
        else:
            if root.left is not None:
                self._find_segments_contain(root.left, point, L, C, L_C) 
            if root.segment.lower_endpoint == point:
                L.append(root.segment)
            else:
                C.append(root.segment)
            L_C.append(root.segment)
            if root.right is not None:
                self._find_segments_contain(root.right, point, L, C, L_C)
           
                
    def find_left_neighbor(self, point):
        left_neighbor = TreeNode(None)
        self._find_left_neighbor(self.root, point, left_neighbor)
        return left_neighbor.segment

    def find_right_neighbor(self, point):
        right_neighbor = TreeNode(None)
        self._find_right_neighbor(self.root, point, right_neighbor)
        return right_neighbor.segment
    
    def _find_left_neighbor(self, root, point, left_neighbor):
        if not root: 
            return 
        elif root.segment.point_location(point) > 0: 
            left_neighbor.copy(root)
            self._find_left_neighbor(root.right, point, left_neighbor) 
        elif root.segment.point_location(point) <= 0: 
            self._find_left_neighbor(root.left, point, left_neighbor) 
    
    def _find_right_neighbor(self, root, point, right_neighbor):
        if not root: 
            return 
        elif root.segment.point_location(point) >= 0: 
            self._find_right_neighbor(root.right, point, right_neighbor) 
        elif root.segment.point_location(point) < 0: 
            right_neighbor.copy(root)
            self._find_right_neighbor(root.left, point, right_neighbor)
    
    def find_leftmost(self, point):
        lm_node = TreeNode(None)
        self._find_leftmost(self.root, point, lm_node)
        return lm_node.segment
        
    def _find_leftmost(self, root, point, lm_node):
        if not root:
            return
        elif root.segment.point_location(point) > 0:
            self._find_leftmost(root.right, point, lm_node)
        elif root.segment.point_location(point) < 0:
            self._find_leftmost(root.left, point, lm_node)
        else:
            self._find_leftmost(root.right, point, lm_node)
            lm_node.copy(root)
            self._find_leftmost(root.left, point, lm_node)
            
    def find_rightmost(self, point):
        rm_node = TreeNode(None)
        self._find_rightmost(self.root, point, rm_node)
        return rm_node.segment
        
    def _find_rightmost(self, root, point, rm_node):
        if not root:
            return
        elif root.segment.point_location(point) > 0:
            self._find_rightmost(root.right, point, rm_node)
        elif root.segment.point_location(point) < 0:
            self._find_rightmost(root.left, point, rm_node)
        else:
            self._find_rightmost(root.left, point, rm_node)
            rm_node.copy(root)
            self._find_rightmost(root.right, point, rm_node)
    
