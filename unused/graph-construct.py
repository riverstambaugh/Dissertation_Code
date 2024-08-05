G = ig.Graph(n = len(A) + 1, directed=True)
letter_to_vertex = {A[i] : i + 1 for i in range(len(A))}

for idx in range(0, len(R), 2):
    u = R[idx]
    v = R[idx+1]

    start_u = len(G)
    G.add_vertices(len(u)+1)
    G.add_edge([0, start_u])
    for i, current_vertex in enumerate(range(start_u, len(G) - 1)):
        G.add_edge([current_vertex, current_vertex+1])
        G.add_edge([letter_to_vertex[u[i]], current_vertex])
    end_u = current_vertex

    start_v = len(G)
    G.add_vertices(len(v))
    G.add_edge([0, start_v])
    for i, current_vertex in enumerate(range(start_v, len(G))):
        G.add_edge([current_vertex, current_vertex+1])
        G.add_edge([letter_to_vertex[v[i]], current_vertex])
    G.add_edge([len(G), end_u])
    # fix indexing

G1, G2 as above

colours1 = [0] + [1] * len(A) + [2] * (len(G1) - len(A) - 1)
colours2 ... 

G1.isomorphic_bliss(G2, return_mapping_12=True, return_mapping_21=False, sh1='fl', sh2=None, color1=colours1, color2=colours2)
