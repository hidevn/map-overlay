from matplotlib import pyplot as plt
class Vertex:
    def __init__(self, coordinates=None, incident_edge=None, event_type=1):
        self.coordinates = coordinates
        self.incident_edge = incident_edge
        self.involves_both = False
        self.belong_to = None
        # Dinh nghia 1 la chi thuoc 1 dcel
        # 2 la giao 2 doan thuoc 2 dcel
        # 3 la 1 doan cua dcel di qua dinh cua dcel khac
        # 4 la 2 dinh cua 2 dcel trung nhau
        self.event_type = event_type
    
    def find_hedges_w_origin(self):
        edges = [self.incident_edge]
        current = self.incident_edge
        while True:
            if self.incident_edge == current.twin.next:
                break
            current = current.twin.next
            edges.append(current)
        return edges
    
    def find_hedges_w_des(self):
        edges = [self.incident_edge.twin]
        current = self.incident_edge.twin
        while True:
            if self.incident_edge.twin == current.next.twin:
                break
            current = current.next.twin
            edges.append(current)
        return edges

    def __repr__(self):
        return str(self.coordinates)
                
    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.coordinates == other.coordinates
        return False
    
    def __hash__(self):
        return hash(self.coordinates)
             
class Face:
    def __init__(self, outer_component=None):
        self.outer_component = outer_component
        self.inner_components = []
        self.line = None
        self.belong_to = None

class HalfEdge:
    def __init__(self, origin=None):
        self.origin = origin
        self.twin = None
        self.incident_face = None
        self.next = None
        self.prev = None
        self.belong_to = None
    
    def __repr__(self):
        return 'HalfEdge[Origin=' + str(self.origin) + ']'

class DCEL:
    def __init__(self, vertices, halfedges, faces, name=None):
        if name is None:
            self.vertices = vertices
            self.halfedges = halfedges
            self.faces = faces
        else:
            for v in vertices + halfedges + faces:
                v.belong_to = name
            self.vertices = vertices
            self.halfedges = halfedges
            self.faces = faces

    def plot(self):
        for he in self.halfedges:
            x = he.origin
            y = he.next.origin
            plt.plot((x.coordinates[0], y.coordinates[0]), (x.coordinates[1], y.coordinates[1]), 'ro-')
        plt.show()

        
    