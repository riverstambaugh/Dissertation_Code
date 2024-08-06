from libsemigroups_pybind11 import FpSemigroup
#from collections import defaultdict

from libsemigroups_pybind11 import Presentation, presentation
def gen_min(S):

    tprls = list(S.rules())
    if (len(tprls) == 0):
        print("No rules assigned, Presentation is already generator minimal")
        return 

    #while (ctr <= len(tprls) - 1):
    #    rls.append(tprls[ctr][0])
    #    rls.append(tprls[ctr][1])
    #    ctr += 1
    
    #D = defaultdict(list)
    #for i, item in enumerate(rls):
    #    D[item].append(i)
    #D = {k:v for k,v in D.items() if len(v)>1}
    rednts = []

    for tup in tprls:
        if (len(tup[0]) == 1 and (tup[0] not in rednts)):
            rednts.append(tup[0])
        if (len(tup[1]) == 1 and (tup[1] not in rednts)):
            rednts.append(tup[1])

    if (len(rednts) == 0):
        print("Presentation is already generator minimal")
        return

    tempS = FpSemigroup()
    tempS = S
    for gen in rednts:
        newS = remove_gen(tempS, gen)
        tempS = newS

    return tempS
    #print(D)

    #if (len(D) != 0):
    #    for gen in D:
    #       S = newPres(S, gen, tprls)
    #else:
    #    print("Presentation is already generator minimal")
    #    return

def remove_gen(S, gen):
    
    newS = FpSemigroup()
    newAlph = S.alphabet().replace(gen, '')
    newS.set_alphabet(newAlph)

    relwords = []
    newrules = []
    oldrules = list(S.rules())
    for rl in oldrules:
        if (rl[0] == gen and rl[1] != gen):
            relwords.append(rl[1])
        elif (rl[1] == gen and rl[0] != gen):
            relwords.append(rl[0])
        else:
            newrules.append(sorted(rl))
    

    #print('Newrules before adding relwords: ', newrules)
    #print('relwords list: ', relwords)
    for i in range(len(relwords)- 1):
        newrules.append(sorted((relwords[i], relwords[i+1])))
    
    
    #print('Newrules after adding relwords: ', newrules)
    for newrl in newrules:
        newS.add_rule(newrl)
    
    return newS

#T = FpSemigroup()
#T.set_alphabet("abcde")
#T.add_rule("dd", "a")
#T.add_rule("cc", "a")
#T.add_rule("bdb", "bcbc")
#T.add_rule("e", "bb")
#
#G = FpSemigroup()
#G.set_alphabet("abcd")

#
#newT = gen_min(T)
#print('The new alphabet is: ', newT.alphabet())
#gmTrls = list(newT.rules())
#print('The new rules are:')
#for elem in gmTrls:
#    print(elem)
#
#gen_min(G)
p = Presentation('abcdefghi')
presentation.add_rule(p, 'd', 'ffg')

presentation.remove_redundant_generators(p)
