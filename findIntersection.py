import numpy as np
import matplotlib.pyplot as plt
from line import Line       
from eventQueue import EventQueue
from statusStructure import StatusStructure
from dcel import Vertex, HalfEdge, Face, DCEL
import matplotlib.cm as cm

class CycleNode:
    def __init__(self, cycle, inf_outer=False):
        self.cycle = cycle if cycle is not None else []
        for he in self.cycle:
            he.cycle = self
        self.links = []
        self.inf_outer = inf_outer
        self.is_inner_boundary = self.check_inner_cycle() if not self.inf_outer else False

    def find_leftmost_he(self):
        min_x = np.inf
        min_he = None
        for hedge in self.cycle:
            if hedge.next.origin.coordinates[0] < min_x:
                min_he = hedge
                min_x = hedge.next.origin.coordinates[0]
        return min_he
    
    def check_inner_cycle(self):
        lm_hedge = self.find_leftmost_he()
        inside_angle = lm_hedge.inside_angle(lm_hedge.next)
        return inside_angle > 180
        

class FindIntersections:
    def __init__(self):
        self.Q = EventQueue()
        self.T = StatusStructure()        
        self.intersections = []
        self.vertices = []
        self.halfedges = []
        self.faces = []
        self.cycles = [CycleNode(cycle=None, inf_outer=True)]
        
    def find_intersections(self, halfedges):
        # for line in lines:
        #     self.Q.insert_line(line)
        for he in halfedges:
            self.Q.insert_he(he)
        while not self.Q.is_empty():
            next_event = self.Q.pop_next_event()
            self.handle_event_point(next_event)
            
    def handle_event_point(self, p):

        def assign_pointer(hedges):
            # Khong biet la dung khong nua =(
            root = hedges[0]
            sorted_hedges = []
            dcel1_hedges = [hedge for hedge in hedges if hedge.belong_to == root.belong_to]
            dcel2_hedges = [hedge for hedge in hedges if hedge.belong_to != root.belong_to]
            i1 = i2 = 0
            i = 1
            while i < len(dcel2_hedges):
                if root.clockwise_angle(dcel2_hedges[i]) < root.clockwise_angle(dcel2_hedges[i-1]):
                    break
                i += 1
            dcel2_hedges = dcel2_hedges[i:] + dcel2_hedges[:i]
            while (i1 + i2) < len(hedges):
                if i1 == len(dcel1_hedges):
                    sorted_hedges.extend(dcel2_hedges[i2:])
                    break
                elif i2 == len(dcel2_hedges):
                    sorted_hedges.extend(dcel1_hedges[i1:])
                    break
                if root.clockwise_angle(dcel1_hedges[i1]) < root.clockwise_angle(dcel2_hedges[i2]):
                    sorted_hedges.append(dcel1_hedges[i1])
                    i1 += 1
                else:
                    sorted_hedges.append(dcel2_hedges[i2])
                    i2 += 1
            # for he in sorted_hedges:
            #     print(he, root.clockwise_angle(he))
            
            for i in range(0, len(sorted_hedges)-1):
                c_he = sorted_hedges[i]
                n_he = sorted_hedges[i+1]
                c_he.twin.set_next(n_he)
            c_he = sorted_hedges[-1]
            n_he = sorted_hedges[0]
            c_he.twin.set_next(n_he)

        U_p = p.lines_u
        L_p, C_p, L_C = self.T.find_segments_contain(p.point)
        U_C = U_p + C_p
        L_U_C = L_C + U_p
        #print('--')
        #print([l.name for l in L_U_C])
        #print('--')
        if len(L_U_C) > 1:
            self.intersections.append(p.point)
        for line in L_C:
            self.T.delete(p.point, line)
        self.T.insert(p.point, U_C)
        #self.T._print_name()
        if len(U_C) == 0:
            s_l = self.T.find_left_neighbor(p.point)
            s_r = self.T.find_right_neighbor(p.point)
            self.find_new_event(s_l, s_r, p.point)
        else:
            s_lm = self.T.find_leftmost(p.point)
            s_l = self.T.find_left_neighbor(p.point)
            self.find_new_event(s_lm, s_l, p.point)
            s_rm = self.T.find_rightmost(p.point)
            s_r = self.T.find_right_neighbor(p.point)
            self.find_new_event(s_rm, s_r, p.point)

        if p.point.involves_both:
            assign_pointer(p.halfedges)
            p.point.incident_edge = p.halfedges[0]
        self.vertices.append(p.point)  
        p.point.left_hedge = s_l.halfedge if s_l is not None else None    
            
    def find_new_event(self, s_l, s_r, p):
        def add_new_he(new_l, s_l, i):
            h_newl = HalfEdge(origin=i)
            h_sl = HalfEdge(origin=i)
            h_newl.belong_to = new_l.belong_to
            h_sl.belong_to = s_l.belong_to
            h_newl.copy_next(s_l.halfedge)
            h_sl.copy_next(s_l.halfedge.twin)
            h_newl.set_twin(s_l.halfedge.twin)
            h_sl.set_twin(s_l.halfedge)
            new_l.set_halfedge(h_newl)
            return h_sl, h_newl
        
        if s_l is None or s_r is None:
            return
        i = s_l.intersect(s_r)
        if i is None:
            return
        x_i, y_i = i.coordinates
        x_p, y_p = p.coordinates
        if y_i < y_p or (y_i == y_p and x_i > x_p):
            lines=[]
            he_w_origin_i = []
            if s_l.lower_endpoint != i and s_l.upper_endpoint != i:
                new_l = Line(s_l.lower_endpoint, i)
                new_l.belong_to = s_l.belong_to
                s_l.lower_endpoint = i
                lines.append(new_l)
                h1, h2 = add_new_he(new_l, s_l, i)
                he_w_origin_i.extend([h1, h2])
                self.halfedges.extend([h1, h2])
            if s_r.lower_endpoint != i and s_r.upper_endpoint != i:
                new_r = Line(s_r.lower_endpoint, i)
                new_r.belong_to = s_r.belong_to
                s_r.lower_endpoint = i
                lines.append(new_r)
                h1, h2 = add_new_he(new_r, s_r, i)
                he_w_origin_i.extend([h1, h2])
                self.halfedges.extend([h1, h2])
            self.Q.insert(i, lines=lines, hedges=he_w_origin_i)
            # self.Q.insert(i)

    def plot(self, halfedges):
        for he in halfedges:
            x = he.origin
            y = he.next.origin
            if he.belong_to == 'dcel1':
                plt.plot((x.coordinates[0], y.coordinates[0]), (x.coordinates[1], y.coordinates[1]), 'ro-')
            else:
                plt.plot((x.coordinates[0], y.coordinates[0]), (x.coordinates[1], y.coordinates[1]), 'bo-')
        for point in self.intersections:
            plt.plot(point.coordinates[0], point.coordinates[1], marker='x', markersize=10, color="blue")
        plt.show()

    def detect_cycle(self):
        he_set = set(self.halfedges)
        while len(he_set) != 0:
            first_he = he_set.pop()
            current_cycle = [first_he]
            current_he = first_he
            while current_he.next != first_he:
                current_he = current_he.next
                he_set.remove(current_he)
                current_cycle.append(current_he)
            self.cycles.append(CycleNode(current_cycle))
        for cycle in self.cycles:
            if cycle.is_inner_boundary:
                left_hedge = cycle.find_leftmost_he().next.origin.left_hedge
                outer_cycle = left_hedge.cycle if left_hedge is not None else self.cycles[0]
                outer_cycle.links.append(cycle)
                

    def get_faces(self):
        outer_cycles = [cycle for cycle in self.cycles if not cycle.is_inner_boundary]
        for outer_cycle in outer_cycles:
            face = Face()
            face.outer_component = outer_cycle.cycle[0] if len(outer_cycle.cycle) != 0 else None
            for inner_cycle in outer_cycle.links:
                face.inner_components.append(inner_cycle.cycle[0])
            intersect_faces = set()
            if len(outer_cycle.cycle) == 0:
                for hedge in outer_cycle.links[0].cycle:
                    intersect_faces.add(hedge.incident_face)
                    hedge.incident_face = face
                print([face.name for face in intersect_faces])
            for hedge in outer_cycle.cycle:
                intersect_faces.add(hedge.incident_face)
                hedge.incident_face = face
            for inner_cycle in outer_cycle.links:
                for hedge in inner_cycle.cycle:
                    hedge.incident_face = face
            if len(intersect_faces) == 1:
                face.name = intersect_faces.pop().name
            elif len(intersect_faces) == 2:
                f1_name = intersect_faces.pop().name
                f2_name = intersect_faces.pop().name
                face.name = f1_name + '.' + f2_name if f1_name is not None and f2_name is not None else None
            self.faces.append(face)

    def get_return_dcel(self):
        return DCEL(self.vertices, self.halfedges, self.faces)
    
    def arrow_draw(self):
        def shift_left_he(halfedge):
            x1, y1 = halfedge.origin.coordinates
            x2, y2 = halfedge.next.origin.coordinates
            v = np.array([x2-x1, y2-y1])
            xv, yv = v
            norm = np.linalg.norm([xv, yv])
            a = np.array([[xv, yv], [-yv, xv]])
            b = [0, 0.03*norm]
            dx, dy = np.linalg.solve(a,b)
            dxv, dyv = v/norm*0.03
            return x1+dx+dxv, y1+dy+dyv, x2-x1-2*dxv, y2-y1-2*dyv
        plt.axes().set_aspect('equal', 'datalim')
        plt.xlim(min([p.coordinates[0] for p in self.vertices]) - 1, max([p.coordinates[0] for p in self.vertices]) + 1)
        plt.ylim(min([p.coordinates[1] for p in self.vertices]) - 1, max([p.coordinates[1] for p in self.vertices]) + 1)
        color = iter(cm.rainbow(np.linspace(0,1,len(self.cycles))))
        he_list = set(self.halfedges)
        for cycle_node in self.cycles:
            c = next(color)
            for he in cycle_node.cycle:
                plt.quiver(*shift_left_he(he), scale=1, scale_units='xy', angles='xy', color=c, width=0.002, headwidth=7)
        plt.show()


    def map_overlay(self, dcel1, dcel2):
        _, ax = plt.subplots(nrows=1, ncols=3)
        dcel1.plot_dcel(ax[0])
        dcel2.plot_dcel(ax[1])
        h = dcel1.halfedges + dcel2.halfedges
        self.halfedges = h
        self.find_intersections(h)
        self.detect_cycle()
        self.get_faces()
        # self.arrow_draw()
        dcel = self.get_return_dcel()
        dcel.plot_dcel(ax[2])
        plt.show()
        return dcel
