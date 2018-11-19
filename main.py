from dcel import *
from findIntersection import FindIntersections
from vertexTree import VertexTree
from line import Line
from dcel1 import dcel as dcel1
from dcel2 import dcel as dcel2
import numpy as np
def map_overlay(dcel1, dcel2):
    # Tao dcel moi ne`k
    # O(nlogn)
    # v_tree = VertexTree()
    # for v in dcel1.vertices: v_tree.insert(v)
    # for v in dcel2.vertices: v_tree.insert(v)
    # v = v_tree.inOrder()
    h = dcel1.halfedges + dcel2.halfedges
    # # Tim giao diem
    # line_set = set()
    # line_list = []
    # for he in h:
    #     p1 = he.origin
    #     p2 = he.next.origin
    #     if (p1, p2) not in line_set and (p2, p1) not in line_set:
    #         line_set.add((p1, p2))
    #         line = Line(p1, p2)
    #         line.set_halfedge(he)
    #         line_list.append(line)
    F = FindIntersections()
    F.find_intersections(h)
    print(F.intersections)
    F.plot(h)


if __name__ == '__main__':
    F = FindIntersections()
    new_dcel = F.map_overlay(dcel1, dcel2)
    #new_dcel.plot_dcel()

