from libsemigroups_pybind11 import Presentation, presentation

#Given a presentation p, computes the canonical form of the presentation
#by removing redundant generators and rules. Also validates the presentation
#and sorts the rules. The code additionally normalizes the presentation's 
#alphabet, then reduces the complement rules, then restores the old alphabet.
def pres_gen_min(p):
    
    pp = Presentation(p.alphabet())
    presentation.add_rules(pp, p)

    pp.validate()
    
    #presentation.normalize_alphabet(pp)
    presentation.remove_redundant_generators(pp)
    presentation.remove_duplicate_rules(pp)
    
    oldalph = pp.alphabet()

    presentation.normalize_alphabet(pp)

    presentation.reduce_complements(pp)
    
    presentation.change_alphabet(pp, oldalph)
    
    presentation.sort_each_rule(pp)

    if (presentation.are_rules_sorted(pp) != True):
        presentation.sort_rules(pp)
    
    #presentation.normalize_alphabet(pp)

    return pp

