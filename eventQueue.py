from segment import Segment

class Wrapper(object):
    def __init__(self):
        self.obj = None

class TreeNode(object): 
    def __init__(self, point, segments): 
        self.point = point 
        self.left = None
        self.right = None
        self.height = 1
        if segments is None:
            self.segments_u = []
        else:
            self.segments_u = segments
        self.halfedges = []

    def __repr__(self):
        return str(self.point) + ': ' + str(self.segments_u)
        
def compare(p, q):
    px, py = p.coordinates
    qx, qy = q.coordinates
    if p == q:
        return 0
    if py != qy:
        return py - qy
    return qx - px

class EventQueue(object): 
    def __init__(self):
        self.root = None
        self._segment_set = set()
        self.segment_list = []
        
    # def insert_segment(self, segment):
    #     upper_end = segment.upper_endpoint
    #     lower_end = segment.lower_endpoint
    #     self.root = self._insert(self.root, upper_end, segment)
    #     self.root = self._insert(self.root, lower_end, None)

    def insert(self, point, segments=None, hedges=None):
        node = None
        def _insert(root, point, segments=None, hedges=None): 
            nonlocal node
            if not root:
                new_node = TreeNode(point, segments)
                if hedges is not None:
                    new_node.halfedges.extend(hedges)
                if point.incident_edge is not None:
                    new_node.halfedges.extend(point.find_hedges_w_origin()) 
                node = new_node
                return new_node
            elif compare(point, root.point) < 0: 
                root.left = _insert(root.left, point, segments, hedges) 
            elif compare(point, root.point) > 0:
                root.right = _insert(root.right, point, segments, hedges) 
            else:
                if point.involves_both == True:
                    root.point.involves_both = True
                if segments is not None:
                    root.segments_u.extend(segments)
                if hedges is not None:
                    root.halfedges.extend(hedges)
                    for hedge in hedges:
                        hedge.origin = root.point
                if point.event_type == 2 and root.point.event_type == 1:
                    root.point.event_type = 3
                elif point.event_type == 1 and root.point.event_type == 1 and point.belong_to != root.point.belong_to:
                    root.point.event_type = 4
                    if point.incident_edge is not None:
                        root.halfedges.extend(point.find_hedges_w_origin())
                node = root
                return root
            root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
            balance = self.getBalance(root) 
            if balance > 1 and compare(point, root.point) < 0: 
                return self.rightRotate(root) 
            if balance < -1 and compare(point, root.point) > 0: 
                return self.leftRotate(root) 
            if balance > 1 and compare(point, root.point) > 0: 
                root.left = self.leftRotate(root.left) 
                return self.rightRotate(root) 
            if balance < -1 and compare(point, root.point) < 0: 
                root.right = self.rightRotate(root.right) 
                return self.leftRotate(root) 
            return root 
        
        self.root = _insert(self.root, point, segments, hedges)
        return node

    def insert_he(self, halfedge):
        inserted_origin = self.insert(halfedge.origin)
        inserted_des = self.insert(halfedge.next.origin)
        if (halfedge.origin, halfedge.next.origin) not in self._segment_set and (halfedge.next.origin, halfedge.origin) not in self._segment_set:
            self._segment_set.add((halfedge.origin, halfedge.next.origin))
            segment = Segment(halfedge.origin, halfedge.next.origin)
            segment.set_halfedge(halfedge)
            if inserted_origin.point == segment.upper_endpoint:
                inserted_origin.segments_u.append(segment)
            elif inserted_des.point == segment.upper_endpoint:
                inserted_des.segments_u.append(segment)

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
    
    def delete(self, point):
        self.root = self._delete(self.root, point)
        
    def get_max(self):
        current = self.root
        while (current.right != None):
            current = current.right
        return current
    
    def pop_next_event(self):
        current = self.get_max()
        self.delete(current.point)
        return current
    
    def _delete(self, root, key): 
        if not root: 
            return root 
        elif compare(key, root.point) < 0: 
            root.left = self._delete(root.left, key) 
        elif compare(key, root.point) > 0: 
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
            root.point = temp.point 
            root.segments_u = temp.segments_u
            root.right = self._delete(root.right, 
                                      temp.point) 
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
    