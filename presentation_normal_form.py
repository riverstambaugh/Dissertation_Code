from libsemigroups_pybind11 import Presentation, presentation

#Given a presentation p, computes the canonical form of the presentation
#by removing redundant generators and rules. Also validates the presentation
#and sorts the rules. The code additionally normalizes the presentation's 
#alphabet, then reduces the complement rules, then restores the old alphabet.
def pres_gen_min(p):
    
    pp = Presentation(p.alphabet())
    presentation.add_rules(pp, p)
     
    pp.validate()
   
    presentation.remove_redundant_generators(pp)
    presentation.remove_duplicate_rules(pp)
 
    #Save the old alphabet, to be reinstated after 
    #complement normalizing.
    oldalph = pp.alphabet()

    #Normalize the presentation's alphabet and 
    #reduce it's complements (equivalent to 
    #constructing an equivalence presentation
    #presenting the same monoid.
   
    presentation.normalize_alphabet(pp)
  
    presentation.reduce_complements(pp)
    
    #Change the alphabet back to the old alphabet
    #so that the bijection returned will map 
    #the original alphabet.
    presentation.change_alphabet(pp, oldalph)
    
    presentation.sort_each_rule(pp)

    if (presentation.are_rules_sorted(pp) != True):
        presentation.sort_rules(pp)
    
    return pp

