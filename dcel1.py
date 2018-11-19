from dcel import Vertex, Face, HalfEdge, DCEL

v_1 = Vertex((1, 9))
v_2 = Vertex((5, 9))
v_4 = Vertex((3, 4))
v_3 = Vertex((7.5, 5.5))

e_12 = HalfEdge(v_1)
e_21 = HalfEdge(v_2)
e_14 = HalfEdge(v_1)
e_41 = HalfEdge(v_4)
e_23 = HalfEdge(v_2)
e_32 = HalfEdge(v_3)
e_24 = HalfEdge(v_2)
e_42 = HalfEdge(v_4)
e_34 = HalfEdge(v_3)
e_43 = HalfEdge(v_4)

f_124 = Face(e_21, name='f1_1')
f_234 = Face(e_24, name='f1_2')
f_1234 = Face(name='f1_0')
f_1234.inner_components = [e_41]

#e_21.twin = e_12
e_12.twin = e_21
e_12.next = e_23
e_12.prev = e_41
e_12.incident_face = f_1234

e_21.twin = e_12
e_21.next = e_14
e_21.prev = e_42
e_21.incident_face = f_124

e_41.twin = e_14
e_41.next = e_12
e_41.prev = e_34
e_41.incident_face = f_1234

e_14.twin = e_41
e_14.next = e_42
e_14.prev = e_21
e_14.incident_face = f_124

e_24.twin = e_42
e_24.next = e_43
e_24.prev = e_32
e_24.incident_face = f_234

e_42.twin = e_24
e_42.next = e_21
e_42.prev = e_14
e_42.incident_face = f_124

e_23.twin = e_32
e_23.next = e_34
e_23.prev = e_12
e_23.incident_face = f_1234

e_32.twin = e_23
e_32.next = e_24
e_32.prev = e_43
e_32.incident_face = f_234

e_34.twin = e_43
e_34.next = e_41
e_34.prev = e_23
e_34.incident_face = f_1234

e_43.twin = e_34
e_43.next = e_32
e_43.prev = e_24
e_43.incident_face = f_234

v_1.incident_edge = e_12
v_2.incident_edge = e_24
v_3.incident_edge = e_34
v_4.incident_edge = e_41

#dcel = {'vertex': [v_1, v_2, v_3, v_4], 'edge': [e_12, e_21, e_23, e_32, e_34, e_43, e_14, e_41, e_24, e_42], 'face': [f_124, f_234, f_1234]}
# for v in [v_1, v_2, v_3, v_4]:
#     dcel.vertices.insert(v)
vertices = [v_1, v_2, v_3, v_4]
halfedges = [e_12, e_21, e_23, e_32, e_34, e_43, e_14, e_41, e_24, e_42]
faces = [f_124, f_234, f_1234]

dcel = DCEL(vertices, halfedges, faces, name="dcel1")

if __name__ == '__main__':
    dcel.plot_dcel()