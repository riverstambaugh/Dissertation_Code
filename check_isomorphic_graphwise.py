from libsemigroups_pybind11 import Kambites, Presentation, presentation, congruence_kind
from presentation_normal_form import pres_gen_min
from check_isomorphic import unused_letters, check_trivial, smalloverlap, find_rednt_unused
import igraph as ig

#Implementation of the graphwise algorithm that checks whether presentations
#p and q are isomorphic, provided they both satisfy C(2).
def check_isomorphic_graphwise(p, q):

    #Checks whether p and q are trivially isomorphic or trivially
    #non-isomorphic. If they are, returns trivial isomorphism or 
    #'True'. If not, returns 'False'.
    trivial_result = check_trivial(p, q)
    if trivial_result[0] is not None:
        return trivial_result[0]

    #If either presentation is C(1), kill the algorithm and return a warning.
    if (smalloverlap(p) < 2) or (smalloverlap(q) < 2):
        #print('The algorithm is only valid for presentations that satisfy C(2) or higher!')
        return None

    #Get the given presentations in their generator minimal form
    pp = pres_gen_min(p)
    qq = pres_gen_min(q)
  
    #If the presentations have alphabet letters that are unused in their 
    #non-trivial and non-generator removable relations,
    #determine how many there are. If the number of these unused letters
    #differs, the presentations are not isomorphic.
    if find_rednt_unused(p, q, pp, qq, trivial_result) == False:
        return False

    #Again, we have to check trivial results for the resulting generator-minimal presentations as well. 
    trivial_result = check_trivial(pp, qq)
    if trivial_result[0] is not None:
        return trivial_result[0]

    #Creates graphs of the generator-minimal forms of the presentations  
    GP = rules_as_graph(pp)
    GQ = rules_as_graph(qq)

    #Colors each graph. The empty node is color 0, the alphabet vertices are each
    #color 1, and all other vertices are color 2.
    colorsP = [0] + [1] * len(pp.alphabet()) + [2] * (GP.vcount() - len(pp.alphabet()) - 1)
    colorsQ = [0] + [1] * len(qq.alphabet()) + [2] * (GQ.vcount() - len(qq.alphabet()) - 1)

    #Calls the igraph isomorphic_bliss function to determine 
    #whether or not the graphs are isomorphic.
    is_iso = GP.isomorphic_bliss(GQ, return_mapping_12=True, return_mapping_21=False, sh1='fl', sh2=None, color1=colorsP, color2=colorsQ)

    #If the graphs are isomorphic, works backwards to 
    #determine where each letter in p's alphabet maps to
    #and returns this alphabet bijection.
    if is_iso[0]:
        alph_switch = is_iso[1][1:len(pp.alphabet())+1]
    
        bij = []
        i = 0
     
        for p_letter, ctrprt in zip(list(pp.alphabet()), alph_switch):
            bij.append((p_letter, qq.alphabet()[ctrprt - 1]))
      
        return sorted(bij)

    return False

#Creates a graph for a given presentation, which has vertex 0 representing the empty word, 
#and vertices connected with edges that represent each relation word. Each pair of relation
#words is connected by a shared vertex at the end. Furthermore, there are vertices representing
#each alphabet letter that are connected to their corresponding vertices in each relation word.
def rules_as_graph(p):

    A = p.alphabet()
    R = p.rules

    G = ig.Graph(len(A) + 1, directed=True)
    letter_to_vertex = {A[i] : i + 1 for i in range(len(A))}

    for idx in range(0, len(R), 2):
        u = R[idx]
        v = R[idx+1]

        start_u = G.vcount()
        G.add_vertices(len(u)+1)
        G.add_edge(0, start_u)
    
        for i, current_vertex in enumerate(range(start_u, G.vcount() - 1)): 
            G.add_edge(current_vertex, current_vertex+1)
            G.add_edge(letter_to_vertex[u[i]], current_vertex)
        end_u = current_vertex
 

        start_v = G.vcount()
        G.add_vertices(len(v)) 
        G.add_edge(0, start_v) 
        for i, current_vertex in enumerate(range(start_v+1, G.vcount())):
            G.add_edge(current_vertex - 1, current_vertex)
            G.add_edge(letter_to_vertex[v[i]], current_vertex - 1)
        G.add_edge(G.vcount() - 1, end_u + 1)
        G.add_edge(letter_to_vertex[v[len(v) - 1]], G.vcount() - 1) 
 
    return G

