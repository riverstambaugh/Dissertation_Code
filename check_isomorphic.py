from libsemigroups_pybind11 import Kambites, Presentation, presentation, congruence_kind
from presentation_normal_form import pres_gen_min
from collections import Counter
import collections
import itertools
from itertools import chain

#Checks whether two presentations (p and q) are isomorphic, provided that they are C(2).
def check_isomorphic(p, q): 
    
    #If the presentations are trivial in some way, will return 
    #whether p and q are trivially isomorphic or not.
    trivial_result = check_trivial(p, q)
    if trivial_result is not None:
        return trivial_result

    #If either presentation is C(1), kill the algorithm and print a warning.
    if (smalloverlap(p) < 2) or (smalloverlap(q) < 2):
        #print('The algorithm is only valid for presentations that satisfy C(2) or higher!')
        return None

    #Algorithm step i: If the presentations have alphabet letters that are unused in their relation words,
    #determine how many there are. If they have a different number of unused alphabet letters, 
    #they cannot be isomorphic.
    p_unused = unused_letters(p)
    q_unused = unused_letters(q)

    #print('The letters not used in any relation words: ')
    #print(p_unused)
    #print(q_unused)
    #print('\n')

    if len(p_unused) != len(q_unused):
        #print('Not isomorphic, the amount of unused generators for each presentation differs.')
        return False
   
    #Get the given presentations in their generator minimal form
    pp = pres_gen_min(p)
    qq = pres_gen_min(q) 
    
    #Just in case the generator-minimal process turned the presentations into
    #Trivial presentations, we check the trivial results again on pp and qq.
    trivial_result = check_trivial(pp, qq)
    if trivial_result is not None:
        return trivial_result

    #Algorithm step ii: Check if the generator-minimal alphabets are the same.
    #If not, the presentations cannot be isomorphic, so return False.
    if len(pp.alphabet()) != len(qq.alphabet()):
        #print('Not isomorphic, generator minimal alphabet sizes differ')
        return False

    #Algorithm step iii: Check if the generator-minimal rule sets have the same 
    #size.  If not, the presentations cannot be isomorphic, so return False.
    if len(pp.rules) != len(qq.rules):
        #print('Not isomorphic, relation word list sizes differ')
        return False

    #Algorithm step iv: If the small overlap classes of the presentations are inequal, they cannot be isomorphic.
    if (smalloverlap(pp) != smalloverlap(qq)):
        #print('Not isomorphic, the presentations have different small overlap classes.')
        return False  

    #Algorithm step iii: Determine if the equivalence classes of the relation words have the same shape.
    #If not, the presentations cannot be isomorphic, so return False. This method also checks whether or 
    #not the presentations have the same amount of equivalence classes as a byproduct.
    p_part = find_classes(pp)
    q_part = find_classes(qq)

    p_classes = getclassdict(pp.rules, p_part)
    q_classes = getclassdict(qq.rules, q_part)

    #print('\n')
    #print('Classes are: ')
    #print(p_classes)
    #print(q_classes)
    #print('\n')
    
    p_dicts = getclassshapes(p_classes, p_part)
    q_dicts = getclassshapes(q_classes, q_part)
    p_shape = p_dicts[0]
    q_shape = q_dicts[0]
    
    #print('Class shapes are: ')
    #print(p_shape)
    #print(q_shape)
    #print('\n')

    if [len(p_shape[x]) for x in range(2, len(p_part)+1, 2)] != [len(q_shape[y]) for y in range(2, len(q_part)+1, 2)]:
        #print('Not isomorphic, equivalence class shapes differ')
        return False

    #Algorithm step iv: for each class, if the particular words in that class 
    #do not have the same lengths, the presentations cannot be isomorphic. This check 
    #determines whether or not the presentations pass this test.
    p_lengths = p_dicts[1]
    q_lengths = q_dicts[1]

    #print('lengths of words in each class: ')
    #print(p_lengths)
    #print(q_lengths)
    #print('\n')

    for i in range(2, len(p_part) + 1, 2):
        if Counter(p_lengths[i]) != Counter(q_lengths[i]):
            #print('Not isomorphic, word lengths for words in classes of size', i, 'differ')
            return False

    #Algorithm step v: By class, the words are converted to their canonical form.  
    #They are sorted shortlex in their class, and then the classes are sorted. 
    #If these arrays are not identical for p and q, the presentations do not
    #present isomorphic monoids, so we return false.
    p_canonical = canonical_classes(p_classes)
    q_canonical = canonical_classes(q_classes)
    
    #print('Classes with words in canonical form, sorted: ')
    #print(p_canonical)
    #print(q_canonical)
    #print('\n')

    if p_canonical != q_canonical:
        #print('Not isomorphic, canonically sorted words do not match.') 
        return False

    #Algorithm step vi.1: The words in each presentation are sorted into a dictionary with keys (x, y, c) where
    #x is the size of the class the word is in, y is the size of the word, and c is the canonical form of the word.
    #The values are all the words that are in a class of size x, length y, with canonical form c.

    p_sorted = sort_by_class_length_shape(p_classes)
    q_sorted = sort_by_class_length_shape(q_classes)

    #print('Sorted dictionary containing each word indexed by class size, word size, and canonical form: ')
    #print(p_sorted, len(q_sorted), '\n')
    #print(q_sorted, len(q_sorted))
    #print('\n')

    #Algorithm step vi.2: Now that the words are categorized and sorted, we need to pick representatives for 
    #(arbitrarily) presentation p. 
    
    p_reps = get_reps(pp)
    
    #print('The representatives chosen for presentation 1 are: ')
    #print(p_reps)

    #Algorithm step vi.3: Now that we have the word representatives, we need to determine the set of 
    #words in q that each representative from p can be mapped to.

    mappings = get_mappings(p_reps, p_sorted, q_sorted)

    #print('The potential mappings to each representative are: ')
    #print(mappings)
    #print('\n')

    #Algorithm step vi.4: Representatives have been chosen.  Now, we do a recursive backtrack search on the 
    #set of representatives, which checks at each level if the partial (or full) bijection agrees.
    #the presentations are isomorphic, so returns the bijection.  If not, returns false.
    final_res = presentation_backtrack(p_reps, mappings, pp, qq) 
    
    if final_res is not None:
        sorted_final = sorted(final_res.items())
        #print('The presentations are isomorphic!')
        #print('Isomorphism: ', sorted_final)
        return sorted_final

    else:
        #print('Not isomorphic, The backtrack search determined no possible bijection between alphabets exist.')
        return False

######################################################################################################

####################################### HELPER FUNCTIONS #############################################

#Using a presentation's relation word list, determines if there are any letters in the 
#presentation's alphabet that are unused.  Returns a list containing any unused letters.
def unused_letters(pp):
    
    used_letters = set()

    for word in pp.rules:
        used_letters.update(word)
    
    used_letters = list(used_letters)
    full_alph = list(pp.alphabet())

    no_rl_letters = [x for x in full_alph if x not in used_letters]
   
    return no_rl_letters

#Uses a sorting algorithm to determine which relation words are in which equivalence 
#classes. Returns a full list denoting what class each word is in.
def find_classes(pp):
    p_part = list(range(0, len(pp.rules)))
        
    for i in range(0, len(pp.rules), 2):
        unite(i, i+1, p_part)
       
    for i in range(len(pp.rules)-1):
        for j in range(i+2, len(pp.rules)):
            if pp.rules[i] == pp.rules[j]:
                unite(i, j, p_part)
    

    return normalize(p_part)

#Helper for normalize
def unite(a, b, part):

    if find(a, part) < find(b, part):
        part[find(b, part)] = find(a, part)

    else:
        part[find(a, part)] = find(b, part)

#Helper for unite
def find(k, part):

    while part[k] < k:
        k = part[k]

    return k

#Helper for partition
def normalize(part):
    for i in range(len(part)):
        part[i] = find(i, part)
    
    newpart = [x // 2 for x in part]

    return newpart


#Constructs and returns a dictionary, whose keys are the 
#class indices and whose values are the given relation words in the class
def getclassdict(pres_rules, pres_part):
    classes = {x : [] for x in range(len(pres_part) // 2)}
    for i, w in enumerate(pres_rules):
        classes[pres_part[i]].append(w)

    return classes


#Creates and returns a dictionary storing the class index (from the partition array) in the value
#slot whose key represents the size of the given class, as well as a dictionary that stores the lengths
#of all the words in each class size
def getclassshapes(pres_classes, pres_part):
    DS = {x : [] for x in range(2, len(pres_part) + 1, 2)}
    DL = {x : [] for x in range(2, len(pres_part) + 1, 2)}
    for i, cls in pres_classes.items():
        if(len(cls) != 0):
            DS[len(cls)].append(i)
            DL[len(cls)].extend([len(i) for i in cls])
    return (DS, DL)


#Create and return a dictionary using (c_size, w_size, w_shape) as the key, where c_size is the class size, 
#w_size is the word size, and w_shape is the canonical word shape.  The values stored for each key are 
#the words that fit each parameter.
def sort_by_class_length_shape(pres_classes):                              
    D = dict()  

    for cls in pres_classes.values():
        for wrd in cls:
             
            w_canon = tuple(canonical_form(wrd))

            if (len(cls), len(wrd), w_canon) not in D.keys():
                D[(len(cls), len(wrd), w_canon)] = [wrd]

            elif wrd not in D[(len(cls), len(wrd), w_canon)]: 
                D[(len(cls), len(wrd), w_canon)].append(wrd)
    
    sorted_keys = sorted(D.items())
    sorted_D = dict(sorted_keys)

    return sorted_D                             
                                            
#Takes in the set of rules and the presentation's alphabet with the finest sort (sorted_p) 
#and uses it to construct a set of representatives for presentation p.  
#This set of representatives starts with the very first word in p.rules(), and is 
#completed once every letter in the presentation's alphabet is 'covered'. 
def get_reps(pp):

    reps = []
    letters = set()
    rls = list(pp.rules)
  
    i = 0
    while len(letters) < len(pp.alphabet()) and (i < len(rls)):

        letters_from_wrd = set(rls[i])
        newletters = letters.union(letters_from_wrd)       

        if rls[i] not in reps and len(newletters) != len(letters):
            reps.append(rls[i])
            letters = newletters

        i += 1

    assert len(letters) == len(pp.alphabet())
    
    return reps

#Returns the canonical shape of a word by as#signing integer values for 
#each letter based on where they appear in the word.
def canonical_form(w):

    word_dict = dict()
    result = []

    for index, char in enumerate(w):
        if char not in word_dict:
            word_dict[char] = index
        result.append(word_dict[char])

    return result


#Using the class dictionary, creates a 2-d array that stores words in canonical form sorted first in
#their given class shortlex, then sorts each of these classes by length.
def canonical_classes(pres_classes):

    canonical_array = []

    for key in pres_classes:
        canonical_words = []
        ind = 0
        while ind < len(pres_classes[key]):
            canonical_words.append(canonical_form(pres_classes[key][ind]))
            ind += 1
        canonical_words = shortlex_sort(canonical_words)
        if canonical_words != []:
            canonical_array.append(canonical_words)

    return sort_canonical_classes(canonical_array)


#Sorts a list of elements in short lexographic (shortlex) order, and returns the sorted list
def shortlex_sort(words):

    return sorted(words, key = lambda s: (len(s), s))


#Sorts the list of words stored in canonical form by combining the length of all words in a given class and sorting 
#those words in shortlex order.
def sort_canonical_classes(canonical_array):

    bigwords = dict()
    sorted_classes = []

    for cls in canonical_array:
        allwrds = [element for word in cls for element in word]
        bigwords[tuple(allwrds)] = cls

    sorted_keys = shortlex_sort(bigwords.keys())
    sorted_bigwords = {key: bigwords[key] for key in sorted_keys}

    for key in sorted_bigwords:
        sorted_classes.append(sorted_bigwords[key])

    return sorted_classes

#Takes in the list of representatives, the list of possible matches for those reps, and the 
#presentation's alphabet (used to check the length of the bijection).  Performs 
#a backtrack search on every possibility for each representative in the representative
#list, and returns false if a bijection is impossible and the bijection as a dictionary w.r.t.
#presentation p's alphabet.
def presentation_backtrack(pres_reps, pres_mappings, pp, qq):

    current_perm = dict()
 
    def dive(current_partial, w_ind):

        #Get the next word from mappings.
        next_w = None
        if w_ind < len(pres_reps):
            next_w = pres_reps[w_ind] 

        #Check if the isomorphism has been defined for each letter.  If so, build the new presentation,
        #if the presentation is equal to presentation q, return the bijection, if not, return None.
        if len(current_partial) == len(pp.alphabet()):
            return check_isomorphism(current_partial, pp, qq)    
        
        #For each choice of v for next_w, we work out the partial map of letters next_w -> v and 
        #check that it agrees with the current partial map on the letters already defined. If it does, 
        #we copy the current_partial data to a new variable new_partial and add the letters  just defined.
        
        added_by_w = set(next_w) - set(current_partial.keys())
   
        for v in pres_mappings[w_ind]:
  
            defns_to_add = dict() 

            assert len(v) == len(next_w)

            #"Work out the partial map of letters from next_w -> v
            for i in range(len(v)):
                defns_to_add[next_w[i]] = v[i]
          
            #Check that it agrees with the current partial map on the letters.
            #If it does, copy the current partial to a new variable new_partial i
            #and add the letters just defined."
            if check_partial(current_partial, defns_to_add):  

                current_partial.update(defns_to_add)

                res = dive(current_partial, w_ind + 1)
                if res is not None:
                    return res 
            
            #If check is false, remove the definitions that do not work and reset to try again.
            for key in added_by_w:
                if key in current_partial.keys():
                    del(current_partial[key]) 
     
        return None

    return dive(current_perm, 0)


#This function takes in a potential isomorphism permutation for presentation 1
#and checks if it matches up with the rules of presentation 2. If so, returns
#the isomorphism, and if not, returns None.
def check_isomorphism(current_partial, pp, qq):
    
    q_counter = Counter(rule_converter(qq))
    newrules = []

    rl_type = None
    if len(pp.rules) > 0:
        rl_type = type(pp.rules[0])

    for rl in pp.rules:
        rl_list = list(rl)
       
        for i in range(len(rl_list)):
            rl_list[i] = current_partial[rl_list[i]]
            if rl_type == str:
                newrl = ''.join(rl_list)
            else:
                newrl = rl_list
        newrules.append(newrl)

    assert len(newrules) == len(pp.rules) and len(newrules) % 2 == 0 

    if len(newrules) > 0 and type(newrules[0]) == list:
        newrules = [tuple(rl) for rl in newrules]

    if Counter(newrules) == q_counter:
        return current_partial

    else: 
        return None


#Iterates through every possible key combination in the definitions we want to add. If 
#there is a contradiction, returns False. Otherwise, returns True.
def check_partial(current_partial, defns_to_add):
    for add_key in defns_to_add.keys():
        for cur_key in current_partial.keys():
                
            if (cur_key == add_key) and (current_partial[cur_key] != defns_to_add[add_key]): 
                return False
            if (cur_key != add_key) and current_partial[cur_key] == defns_to_add[add_key]:
                return False
    
    return True


#This function takes the list of representatives as well as the sorted dictionaries
#uses that information to determine a list of possible mappings for each 
#representative, and then returns this list of possible mappings.
def get_mappings(pres_reps, p_sorted, q_sorted):
    
    mappings = []

    for rep in pres_reps:

        key = next((key for key, value_list in p_sorted.items() if rep in value_list), None)

        assert key != None
        assert key in q_sorted.keys()
 
        mappings.append(sorted(q_sorted[key]))

    return mappings


#Creates a Kambites object for a presentation and returns the 
#presentation's small overlap class
def smalloverlap(p):
      
    kp = Kambites()
 
    cp = Presentation(p)

    if type(cp.alphabet()) == str:
        kp.set_alphabet(cp.alphabet())

    else: 
        cp_alph = list(range(len(p.alphabet())))
        presentation.change_alphabet(cp, cp_alph)
        kp.set_alphabet(len(p.alphabet()))

    i = 0
    while i < (len(cp.rules) - 1):
        kp.add_rule(cp.rules[i], cp.rules[i+1])
        i += 2

    return kp.small_overlap_class()


#The following function is necessary to determine whether or not the rules
#in a given presentation are strings or lists of integers. If the latter is
#true, the function converts them into tuples so they are immutable and 
#can be used as keys in dictionaries and the Counter() function can be i
#called on them. Returns a list of immutable objects representing the 
#rules of presentation p.
def rule_converter(p):

    if len(p.rules) > 0 and type(p.rules[0]) == list:
        return [tuple(rl) for rl in p.rules]
    else:
        return p.rules

#This method checks multiple trivial results possible, and returns 'True'
#or 'False' depending on what the presentations satisfy.
def check_trivial(p, q):

    #If the presentations are both empty, they are trivially isomorphic.
    if len(p.alphabet()) == len(q.alphabet()) == 0:
        return True

    #If one alphabet is length 0, and the other is not, return False.
    if (len(p.alphabet()) == 0 and len(q.alphabet()) != 0) or (len(q.alphabet()) == 0 and len(p.alphabet()) != 0):  
        return False

    #If the lengths of the alphabets are the same and neither presentation
    #has any rules, then they are isomorphic, and in fact there are 
    #(len(pp.alphabet()))! isomorphisms. Returns one of these.
    if len(p.alphabet()) == len(q.alphabet()) and len(p.rules) == len(q.rules) == 0:
        bijection = []
        for i in range(len(p.alphabet())):
            bijection.append((p.alphabet()[i], q.alphabet()[i]))
        return bijection

    return None

#################################################################################################

############################### UNUSED HELPERS/PROTOTYPES #######################################

##The originial canonical_form build, does not work.
#def canonical_form_broken(w):
#
#    word_dict = dict()
#    result = []
#
#    for index, char in enumerate(w):
#        if char not in word_dict:
#            word_dict[char] = index
#        result.append(str(word_dict[char]))
#
#    return ''.join(result)

#Determines the shape of a relation word equivalence class array.
#In this array, by convention, classes of size 2 are stored at
#index 0, size 4 at index 1, and so on.
#def get_shape(p_part):
#
#    classes = len(p_part)
#
#    class_size_ctr = [0] * (classes // 2)
#    
#    for i in range(classes):
#        ctr = 0
#        for j in range(classes):
#            
#            if p_part[j] == i:
#                ctr += 1
#        
#        if ctr != 0:
#            ind = (ctr // 2) - 1
#            class_size_ctr[ind] += 1
#    
#    return class_size_ctr


    ##Create Kambites objects from the presentations
    #kp = Kambites()
    #kq = Kambites()

    #kp.set_alphabet(pp.alphabet())
    #kq.set_alphabet(qq.alphabet())

    #i = 0
    #while i < (len(pp.rules) - 1):
    #    kp.add_rule(pp.rules[i], pp.rules[i+1])
    #    i += 2
    #
    #j = 0
    #while j < (len(qq.rules) - 1):
    #    kq.add_rule(qq.rules[j], qq.rules[j+1])
    #    j += 2
    #
    ##If either presentation is C(1), kill the algorithm and return a warning.
    #if (kp.small_overlap_class() < 2) or (kq.small_overlap_class() < 2):
    #    print('The algorithm is only valid for presentations that satisfy C(2) or higher!')
    #    return None


    #p_sizes = getss(p_lengths, p_classes, pp.rules)
    #q_sizes = getss(q_lengths, q_classes, qq.rules)

    #print('Dictionary containing each word indexed by class size and word size: ')
    #print(p_sizes, len(p_sizes), '\n')
    #print(q_sizes, len(q_sizes))
    #print('\n')

##Creates and returns a dictionary using (c_size, w_size) as the key, where c_size is the class size and
##w_size is the word size.  The values stored for each key are the words that are both contained in a class 
##of size c_size and are length w_size.
#def getss(pres_lengths, pres_classes, pres_rules):
#
#    classsizes = [cs for cs in pres_lengths if pres_lengths[cs] != []]
#    wordsizes = list(set(list(chain.from_iterable(pres_lengths.values()))))
#
#    D = {(cs, ws) : [] for (cs, ws) in itertools.product(classsizes, wordsizes) if ws in pres_lengths[cs]}
#    
#    for cls in pres_classes.values():
#        for wrd in cls:
#            if wrd not in D[(len(cls), len(wrd))]:
#                D[(len(cls), len(wrd))].append(wrd)
#        
#    return D

#########################################################################################################

##################################### MEETING NOTES #####################################################

#DONE ||||||||||||||||||||||||||||||

#Monday 7/1/24

#FOR BIJECTIONS, FIRST CHECK SHOULD BE TO SAY IF WE CAN EVEN MATCH UP THE WORDS.
#Take the union of the classses of each size, length of words in each thing, and compare those lists to each other. so
#shortlex sort them, store lengths of words in each list and sort and determine if those lists are equal.

#Function that determines for each word in a given pres, find the indices in the partition list of what word is possible for it to go to (word size and class size). If there is only one, that gives less choice for algorithm.

#NEED TO CREATE A DICTIONARY WHICH CONTAINS all possible info, F = {(class size, word length) : [all such words])}

#Thursday 7/4/24

#Canonical form of a word w = w1, ... ,wn : C(w) = (c1, ...... ,cn) n = |w|
#ci = index of first appearance of wi, for example, dded = 0020
#Turn the classes into these, sort each class, then sort the classes together and compare
#All information derived from the dictionary of classes.

#Pick some word representatives to cover all the letters in the alphabet.  Call the set of them W. take w1, ... , wl e W
#, then w is in some class Ai.  We map w using the map f, (w)f, in class Bi.
# We build a tree, (w1)f = v1, (w1)f = v2, etc.  If a mapping is possible, we take (w2)f and do the same.  

#But how do we pick the representatives? SET COVERING:
#First, order words to agree with the ordering of the classes. (optional? a good idea.)
#Pick first word w1, add w1 to W (the set of reps) first word in the ordering.  Let L:= letters(w1)
#while |L| < |A| where A is the alphabet:
#   pick next word wi   
#   if letters(wi) !<= L:
#       add letters(wi) to L 
#       add wi to W
#When this is done, for each wi, find the list of all vji that wi can map to, try each one.
#If we get to a full permutation of the alphabet, we then create a new presentation with this alphabet and with the same rules, but new alphabet, and check if the rules are identical to the rules in presentation 'q'.

#NEED A CHECK FOR IF THE PRESENTATIONS AHVE A DIFFERENT NUMBER OF UNUSED LETTERS
