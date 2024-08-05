from libsemigroups_pybind11 import Kambites, Presentation, presentation
from presentation_normal_form import *
from check_isomorphic import smalloverlap, unused_letters, rule_converter, check_trivial
from collections import Counter, OrderedDict
from itertools import permutations
import random

def brute_force_checker(p, q): 

    #Checks if presentations are trivially isomorphic
    #or non-isomorphic.
    trivial_result = check_trivial(p, q)
    if trivial_result is not None:
        return trivial_result

    #If either presentation is C(1), kill the algorithm and return a warning.
    if (smalloverlap(p) < 2) or (smalloverlap(q) < 2):
        #print('The algorithm is only valid for presentations that satisfy C(2) or higher!')
        return None

    #Checks if one presentation contains more unused letters than the other. If so, not isomorphic,
    #so we return False.
    p_unused = unused_letters(p)
    q_unused = unused_letters(q)

    if len(p_unused) != len(q_unused):
        #print('Not isomorphic, the amount of unused generators for each presentation differs.')
        return False

    qq = pres_gen_min(q)
    new_qq_rules = rule_converter(qq) 
    q_counter = Counter(new_qq_rules)
    pp = pres_gen_min(p)
    
    #Again, we check trivial results for the presentations in their generator-minimal form. 
    trivial_result = check_trivial(pp, qq)
    if trivial_result is not None:
        return trivial_result

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

      
##############################################################################

######################### UNUSED #############################################


def next_permutation(a):
    """Generate the lexicographically next permutation inplace.

    https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
    Return false if there is no next permutation.
    """
    # Find the largest index i such that a[i] < a[i + 1]. If no such
    # index exists, the permutation is the last permutation
    for i in reversed(range(len(a) - 1)):
        if a[i] < a[i + 1]:
            break  # found
    else:  # no break: not found
        return False  # no next permutation

    # Find the largest index j greater than i such that a[i] < a[j]
    j = next(j for j in reversed(range(i + 1, len(a))) if a[i] < a[j])

    # Swap the value of a[i] with that of a[j]
    a[i], a[j] = a[j], a[i]

    # Reverse sequence from a[i + 1] up to and including the final element a[n]
    a[i + 1 :] = reversed(a[i + 1 :])
    return a


def shuffle_presentation(p):
    alphabet = [p.alphabet()[i] for i in range(len(p.alphabet()))]
    random.shuffle(alphabet)
    result = Presentation(p)
    presentation.change_alphabet(result, "".join(alphabet))

    return result
        
        #cpy = []
        #for letter in current_alph:
        #    cpy.append(letter)
        #if not next_permutation(cpy):  
        #    return False
    
      
        #new_vals = next_permutation(current_alph)
       
             
        #new_bij = {key : new_val for key, new_val in zip(bijection, new_vals)} 
        #assert bijection != new_bij
        #bijection = new_bij
    
        #new_alphabet = "".join(list(bijection.values()))  
        #assert new_alphabet != copy.alphabet()
     
        #presentation.change_alphabet(copy, new_alphabet)
