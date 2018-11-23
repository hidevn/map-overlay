from dcel import Vertex, Face, HalfEdge, DCEL

v_1 = Vertex((3, 6))
v_2 = Vertex((4, 10))
#v_3 = Vertex((3.5, 2))
#v_3 = Vertex((3, 4))
v_3 = Vertex((5, 6))

e_12 = HalfEdge(v_1)
e_21 = HalfEdge(v_2)
e_23 = HalfEdge(v_2)
e_32 = HalfEdge(v_3)
e_13 = HalfEdge(v_1)
e_31 = HalfEdge(v_3)

f_1 = Face(e_21, name='f2_1')
f_2 = Face(name='f2_0')
f_2.inner_components = [e_12]

e_12.twin = e_21
e_12.next = e_23
e_12.prev = e_31
e_12.incident_face = f_2

e_21.twin = e_12
e_21.next = e_13
e_21.prev = e_32
e_21.incident_face = f_1

e_23.twin = e_32
e_23.next = e_31
e_23.prev = e_12
e_23.incident_face = f_2

e_32.twin = e_23
e_32.next = e_21
e_32.prev = e_13
e_32.incident_face = f_1

e_13.twin = e_31
e_13.next = e_32
e_13.prev = e_21
e_13.incident_face = f_1

e_31.twin = e_13
e_31.next = e_12
e_31.prev = e_23
e_31.incident_face = f_2

v_1.incident_edge = e_12
v_2.incident_edge = e_23
v_3.incident_edge = e_31

#dcel = {'vertex': [v_1, v_2, v_3], 'edge': [e_12, e_21, e_23, e_32, e_31, e_13], 'face': [f_1, f_2]}
# for v in [v_1, v_2, v_3]:
#     dcel.vertices.insert(v)
vertices = [v_1, v_2, v_3]
halfedges = [e_12, e_21, e_23, e_32, e_31, e_13]
faces = [f_1, f_2]

dcel = DCEL(vertices, halfedges, faces, name="dcel2")

if __name__ == '__main__':
    dcel.plot_dcel()