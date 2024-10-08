from libsemigroups_pybind11 import Kambites, Presentation, presentation
from presentation_normal_form import *
from check_isomorphic import smalloverlap, unused_letters, rule_converter, check_trivial, find_rednt_unused
from collections import Counter, OrderedDict
from itertools import permutations
import random

#An implementation of the brute force algorithm that 
#checks whether presentations p and q are isomorphic,
#provided they both satisfy C(2).
def brute_force_checker(p, q): 

    #Checks if presentations are trivially isomorphic
    #or non-isomorphic.
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
    
    new_qq_rules = rule_converter(qq) 
    q_counter = Counter(new_qq_rules)

    #Again, we check trivial results for the presentations in their generator-minimal form. 
    trivial_result = check_trivial(pp, qq)
    if trivial_result[0] is not None:
        return trivial_result[0]

    #Alphabet sizes must be the same in order for the alphabet change to work properly
    if len(pp.alphabet()) != len(qq.alphabet()):
        return False

    copy = Presentation(pp)
  
    bijection = {x : x for x in qq.alphabet()}
   
    current_alph = sorted(list(qq.alphabet())) 

    all_perms = permutations(current_alph) 

    while True:
        
        res = next(all_perms, False)

        if not res:
            return res
        
        new_vals = res
      
        new_bij = {key : new_val for key, new_val in zip(bijection, new_vals)} 
     
        bijection = new_bij
    
        if type(copy.alphabet()[0]) == str:
            new_alphabet = "".join(list(bijection.values()))        
        else:
            new_alphabet = list(bijection.values())
      
        presentation.change_alphabet(copy, new_alphabet)
        
        copy_counter = Counter(rule_converter(copy))

        if copy_counter == q_counter:
            bij_list = []
            bij_keys = list(bijection.keys()) 
          
            for i in range(len(pp.alphabet())):
                bij_key = list(bijection.keys())[i]
                
                bij_list.append((pp.alphabet()[i], bijection[bij_key]))
            #print('The presentations are isomorphic! (BRUTE FORCE)')
            #print(sorted(bij_list))
            #print('\n')
            return sorted(bij_list)      
