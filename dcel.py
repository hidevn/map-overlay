class Vertex:
    def __init__(self, coordinates=None, incident_edge=None):
        self.coordinates = coordinates
        self.incident_edge = incident_edge
        self.involves_both = False
    
    def find_edges_w_origin(self):
        edges = [self.incident_edge]
        current = self.incident_edge
        while True:
            if self.incident_edge == current.twin.next:
                break
            current = current.twin.next
            edges.append(current)
        return edges
             
class Face:
    def __init__(self, outer_component=None):
        self.outer_component = outer_component
        self.inner_components = []

class HalfEdge:
    def __init__(self, origin=None):
        self.origin = origin
        self.twin = None
        self.incident_face = None
        self.next = None
        self.prev = None

class DCEL:
    def __init__(self):
        self.vertices = []
        self.halfedges = []
        self.faces = []