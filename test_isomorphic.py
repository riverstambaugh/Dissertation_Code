from check_isomorphic import *
from brute_force import *
from check_isomorphic_graphwise import *
from presentation_normal_form import pres_gen_min
import itertools
import timeit

#This file contains a multitude of tests for all 3 algorithms, created originally
#to ensure the backtrack algorithm was returning proper outputs and modified
#as time went on to test edge cases for all 3 algorithms.

#################################################################################

############################### PRESENTATION DEFINITIONS ########################

#The following are a multitude of presentations used to test the algorithms.
a = Presentation('abcdefgh')
b = Presentation('gfedcbah')
c = Presentation('abcdefgh')
d = Presentation('abcdefgh')
e = Presentation('abcdefgh')
f = Presentation('abcdefgh')
g = Presentation('abcdefgh')
h = Presentation('abcdefgh')
i = Presentation('abcdefgh')
j = Presentation('abcdefgh')
k = Presentation('abcdefg')
l = Presentation('abcdefgh')
m = Presentation('abcdefg')
n = Presentation('abcdefg')
o = Presentation('abcdefg')
p = Presentation('abcd')
q = Presentation('abcd')
r = Presentation('abcdefg')
s = Presentation('abcdefg')
t = Presentation('abcdefgh')
u = Presentation('hbacgdfe')
v = Presentation('zyxwavuts')
w = Presentation('abcdefzgh')
#rules in the presentations
presentation.add_rule(a, 'gg', 'bbcce')
presentation.add_rule(a, 'bbb', 'eeff')
presentation.add_rule(a, 'afcfc', 'bbb')
presentation.add_rule(a, 'afg', 'd')
presentation.add_rule(a, 'ab', 'ba')
presentation.add_rule(a, 'bbb', 'ab')
                      
presentation.add_rule(b, 'ab', 'ba')
presentation.add_rule(b, 'afcfc', 'bbb')
presentation.add_rule(b, 'd', 'afg')
presentation.add_rule(b, 'eeff', 'bbb')
presentation.add_rule(b, 'gg', 'bbcce')
presentation.add_rule(b, 'bbge', 'eeff')
                      
presentation.add_rule(c, 'ba', 'afcfc')
presentation.add_rule(c, 'gg', 'bbcce')
presentation.add_rule(c, 'ab', 'ba')
presentation.add_rule(c, 'bbb', 'eeff')
presentation.add_rule(c, 'aaa', 'bbb')
                      
#Same class shapes, but not isomorphic
presentation.add_rule(d, 'ab', 'ba')
presentation.add_rule(d, 'afcfc', 'bbb')
presentation.add_rule(d, 'd', 'afg')
presentation.add_rule(d, 'eeff', 'bbb')
presentation.add_rule(d, 'gg', 'bbcce')
presentation.add_rule(d, 'bbge', 'gg')
                      
presentation.add_rule(e, 'ab', 'ba')
presentation.add_rule(e, 'afcfc', 'ba')
presentation.add_rule(e, 'd', 'afg')
presentation.add_rule(e, 'eeff', 'bbb')
presentation.add_rule(e, 'gg', 'bbcce')
presentation.add_rule(e, 'bbge', 'eeff')
                      
#F has 5 classes of sie 2
presentation.add_rule(f, 'ab', 'ba')
presentation.add_rule(f, 'afcfc', 'bbb')
presentation.add_rule(f, 'd', 'afg')
presentation.add_rule(f, 'eeff', 'eee')
presentation.add_rule(f, 'gg', 'bbcce')
presentation.add_rule(f, 'bbge', 'fff')
                      
#G has 1 class of size10
presentation.add_rule(g, 'ab', 'ba')
presentation.add_rule(g, 'afcfc', 'ba')
presentation.add_rule(g, 'd', 'afg')
presentation.add_rule(g, 'eeff', 'ba')
presentation.add_rule(g, 'gg', 'fff')
presentation.add_rule(g, 'ab', 'fff')
#q = Presentation(p)
      
#Presentations H and I have the same alphabet, same number of relation words,
#the same relation word equivalence class shape, and the same word sizes in each
#collection of equivalence classes
presentation.add_rule(h, 'bbc', 'efg')
presentation.add_rule(h, 'ccd', 'aa')
presentation.add_rule(h, 'ababfg', 'eee')
presentation.add_rule(h, 'ccd', 'fefe')

presentation.add_rule(i, 'efg', 'dddd')
presentation.add_rule(i, 'cc', 'efg')
presentation.add_rule(i, 'abc', 'bbggee')
presentation.add_rule(i, 'aaa', 'bbb')

#Alphabet changes, just for fun to make the algorithm squirm a bit.
#presentation.change_alphabet(b, 'xyzuabcw')
presentation.change_alphabet(d, 'ghjdirsk')
presentation.change_alphabet(e, 'riadshge')

#Presentations j and k have different generator-minimal alphabet sizes.
presentation.add_rule(j, 'gg', 'bbcce')
presentation.add_rule(j, 'bbb', 'eeff')
presentation.add_rule(j, 'afcfc', 'bbb')
presentation.add_rule(j, 'afg', 'd')
presentation.add_rule(j, 'ab', 'ba')
presentation.add_rule(j, 'hhh', 'ab')
                      
presentation.add_rule(k, 'ab', 'ba')
presentation.add_rule(k, 'afcfc', 'bbb')
presentation.add_rule(k, 'd', 'afg')
presentation.add_rule(k, 'eeff', 'bbb')
presentation.add_rule(k, 'gg', 'bbcce')
presentation.add_rule(k, 'bbge', 'eeff')

#Presentations l and m have different alphabet sizes.
presentation.add_rule(l, 'gg', 'bbcce')
presentation.add_rule(l, 'bbb', 'eeff')
presentation.add_rule(l, 'afcfc', 'bbb')
presentation.add_rule(l, 'afg', 'd')
presentation.add_rule(l, 'ab', 'ba')
presentation.add_rule(l, 'bbb', 'ab')
                      
presentation.add_rule(m, 'ab', 'ba')
presentation.add_rule(m, 'afcfc', 'bbb')
presentation.add_rule(m, 'd', 'afg')
presentation.add_rule(m, 'eeff', 'bbb')
presentation.add_rule(m, 'gg', 'bbcce')
presentation.add_rule(m, 'bbge', 'eeff')

#Presentations n and o have different alphabet sizes.
presentation.add_rule(n, 'gg', 'bbcce')
presentation.add_rule(n, 'bbb', 'eeff')
presentation.add_rule(n, 'afcfc', 'bbb')
presentation.add_rule(n, 'afg', 'd')
presentation.add_rule(n, 'ab', 'ba')
presentation.add_rule(n, 'bbb', 'ab')
presentation.add_rule(n, 'ccbb', 'ffee')
                      
presentation.add_rule(o, 'ab', 'ba')
presentation.add_rule(o, 'afcfc', 'bbb')
presentation.add_rule(o, 'd', 'afg')
presentation.add_rule(o, 'eeff', 'bbb')
presentation.add_rule(o, 'gg', 'bbcce')
presentation.add_rule(o, 'bbge', 'eeff')

#Presentations p and q have different small overlap class sizes
presentation.add_rule(p, 'abdb', 'bb')
presentation.add_rule(p, 'cbccbc', 'aaa')

presentation.add_rule(q, 'aacc', 'dda')
presentation.add_rule(q, 'aab', 'dcd')

#Presentations r and s have the same class shapes, same word
#lengths in each class, and the same canonical form.  but b -> e 
#in presentation s, and so they are not isomorphic.
presentation.add_rule(r, 'aaa', 'cd')
presentation.add_rule(r, 'ffeg', 'aaa')
presentation.add_rule(r, 'bcbcb', 'cc')
presentation.add_rule(r, 'afggfa', 'dgdg')
presentation.add_rule(r, 'dgdg', 'bbb')
presentation.add_rule(r, 'bbb', 'gb')
presentation.add_rule(r, 'agaag', 'dd')

presentation.add_rule(s, 'eee', 'gb')
presentation.add_rule(s, 'cc', 'ecece')
presentation.add_rule(s, 'cd', 'aaa')
presentation.add_rule(s, 'dgdg', 'eee')
presentation.add_rule(s, 'ffeg', 'aaa')
presentation.add_rule(s, 'dgdg', 'afggfa')
presentation.add_rule(s, 'dd', 'agaag')

#Presentations T and U are isomorphic, and have the same alphabets.  The mapping should be a -> b,
#b -> c, c -> d, etc.
presentation.add_rule(t, 'bcbc', 'cbcb')
presentation.add_rule(t, 'faa', 'eee')
presentation.add_rule(t, 'abcde', 'ggfab')
presentation.add_rule(t, 'aaaaa', 'cgh')
presentation.add_rule(t, 'cgh', 'bcbc')

presentation.add_rule(u, 'cdcd', 'bbbbb')
presentation.add_rule(u, 'cdcd', 'dcdc')
presentation.add_rule(u, 'gbb', 'fff')
presentation.add_rule(u, 'bcdef', 'hhgbc')
presentation.add_rule(u, 'bbbbb', 'dha')

#Presentation v is isomorphic to w and they both have a redundant generator 
#that is related to two separate relation words. 
presentation.add_rule(v, 'wvwv', 'vwvw')
presentation.add_rule(v, 'zyy', 'xxx')
presentation.add_rule(v, 'ywvux', 'ttzyw')
presentation.add_rule(v, 'yyyyy', 'vts')
presentation.add_rule(v, 'a', 'ssttv')
presentation.add_rule(v, 'vts', 'a')

presentation.add_rule(w, 'abab', 'baba')
presentation.add_rule(w, 'cdd', 'eee')
presentation.add_rule(w, 'dabfe', 'ggcda')
presentation.add_rule(w, 'ddddd', 'bgh')
presentation.add_rule(w, 'z', 'hhggb')
presentation.add_rule(w, 'ddddd', 'z')

#########################################################################################

########################### BACKTRACK ALGORITHM TESTS ###################################

#These tests check that the output of the algorithms match and that 
#the algorithms are returning the expected output.

##Not isomorphic because the word lengths in each class do not match
assert check_isomorphic(d, e) == brute_force_checker(d, e) == check_isomorphic_graphwise(d, e) == False
#
##Not isomorphic because the class shapes differ
assert check_isomorphic(f, g) == brute_force_checker(f, g) == check_isomorphic_graphwise(f, g) == False
#
##Not isomorphic because canonical word forms differ
assert check_isomorphic(h, i) == brute_force_checker(h, i) == check_isomorphic_graphwise(h, i) == False

#Not isomorphic because generator minimal alphabet sizes differ
assert check_isomorphic(j, k) == brute_force_checker(j, k) == check_isomorphic_graphwise(j, k) == False

#Not isomorphic because one has more unused generators than the other
assert check_isomorphic(l, m) == brute_force_checker(l, m) == check_isomorphic_graphwise(l, m) == False

#Not isomorphic because O has more rules than N
assert check_isomorphic(o, n) == brute_force_checker(o, n) == check_isomorphic_graphwise(o, n) == False

#Not isomorphic because P has a different small overlap class size than Q
assert check_isomorphic(p, q) == brute_force_checker(p, q) == check_isomorphic_graphwise(p, q) == False

#Not isomorphic because b (in R) must map to e, but also to itself.
assert check_isomorphic(r, s) == brute_force_checker(r, s) == check_isomorphic_graphwise(r, s) == False

#Isomorphic, each alphabet letter in T maps to the next alphabet letter in U
presentation.change_alphabet(u, '104729fp')
assert bool(check_isomorphic(t, u)) == bool(brute_force_checker(t, u)) == bool(check_isomorphic_graphwise(t, u)) == True

#Presentations v and w are isomorphic and have multiple redundant elements. 
assert bool(check_isomorphic(w, v)) == bool(brute_force_checker(w, v)) == bool(check_isomorphic_graphwise(w, v)) == True


#########################################################################################

################ TEST EVERY POSSIBLE COMBINATION OF PRESENTATIONS #######################

#Adds all presentations to a dictionary to come up with all possible combinations of presentations
#and tests all of these possible combinations on all 3 algorithms, ensuring they have the same output.

allpres = dict()
allpres['a']= a
allpres['b']= b
allpres['c']= c
allpres['d']= d
allpres['e']= e
allpres['f']= f
allpres['g']= g
allpres['h']= h
allpres['i']= i
allpres['j']= j
allpres['k']= k
allpres['l']= l
allpres['m']= m
allpres['n']= n
allpres['o']= o
allpres['p']= p
allpres['q']= q
allpres['r']= r
allpres['s']= s
allpres['t']= t
allpres['u']= u
allpres['v']= v
allpres['w'] = w

all_objs = allpres.values()
all_keys = allpres.keys()
all_combs = [(x, y) for (x, y) in itertools.product(all_objs, all_objs)]

combs = []

ctr = 0

#Comment this code in to confirm output for each algorithm is the same on all 
#combinations of presentations a through w.

for duo in all_combs:
    ctr += 1
    assert check_isomorphic(duo[0], duo[1]) == check_isomorphic_graphwise(duo[0], duo[1]) == brute_force_checker(duo[0], duo[1])

print('All algorithms match output for', ctr, 'tests')


###################################################################################

#################################### STRESS TEST ##################################

#Below is a stress test that combines 5 different presentations and creates a large presentation. 
#This presentation is then duplicated and it's alphabet is swapped to create a nontrivial 
#isomorphism, which is then calculated using both isomorphism checkers (brute force is 
#not used, as it is not feasible for the calculation to be completed given the large alphabet size)

presentation.change_alphabet(a, 'abcdefgh')
presentation.change_alphabet(v, 'ijklmnopq')
presentation.change_alphabet(w, 'rstuvwxyz')
presentation.change_alphabet(b, '12345678')
presentation.change_alphabet(j, '90/.,;][')
presentation.change_alphabet(r, '!@#$%^&')
presentation.change_alphabet(s, '=-:|)(*')
presentation.change_alphabet(n, 'ABCDEFG')
presentation.change_alphabet(o, 'HIJKLMN')
longalph = v.alphabet() + w.alphabet() + a.alphabet() + b.alphabet() + j.alphabet() + r.alphabet() + s.alphabet() + n.alphabet() + o.alphabet()

bigpres = Presentation(longalph)
longrules = v.rules + w.rules + a.rules + b.rules + j.rules + r.rules + s.rules + n.rules + o.rules

for x in range(0, len(longrules), 2):
    presentation.add_rule(bigpres, longrules[x], longrules[x+1])

bigpres2 = Presentation(bigpres.alphabet())
rules_2 = []
for y in range(len(bigpres.rules)):
    rules_2.append(bigpres.rules[y])
for z in range(0, len(rules_2), 2):
    presentation.add_rule(bigpres2, rules_2[z], rules_2[z+1])
presentation.change_alphabet(bigpres2, '1234567890qwertyuiop[]asdfghjkl;zxcvbnm,./)(*&^%$#@!~=-+QWERTYUIOPASDF')

assert bool(check_isomorphic(bigpres, bigpres2)) == bool(check_isomorphic_graphwise(bigpres, bigpres2)) == True


####################################################################################################

#################################### TIMING THE METHODS ############################################

#The following code times each isomorphism algorithm based on all 529 possible combinations of 
#presentations a through w. The times for each one are stored and compared, and the number of 
#times each presentation is the fastest is printed.
def test_time(all_combs):

    backtrack_wins = 0
    graphwise_wins = 0
    bruteforce_wins = 0

    for duo in all_combs:

        def backtrack_method():
            check_isomorphic(duo[0], duo[1])

        def graphwise_method():
            check_isomorphic_graphwise(duo[0], duo[1])

        def bruteforce_method():
            brute_force_checker(duo[0], duo[1])

        backtrack_time = timeit.timeit(backtrack_method, number=1)
        graph_time = timeit.timeit(graphwise_method, number=1)
        brute_time = timeit.timeit(bruteforce_method, number=1)
    
        if backtrack_time > graph_time and backtrack_time > brute_time:
            backtrack_wins += 1
        if graph_time > backtrack_time and graph_time > brute_time:
            graphwise_wins += 1
        if brute_time > backtrack_time and brute_time > graph_time:
            bruteforce_wins += 1

    total_runs = backtrack_wins + graphwise_wins + bruteforce_wins

    assert total_runs == len(all_combs)

    return (bruteforce_wins, backtrack_wins, graphwise_wins, total_runs)

brute_total = 0
back_total = 0
graph_total = 0
run_total = 0

##Comment this code in to run the timed test on all combinations
##of presentations a through w 50 times in total.

#for i in range(50):
#    
#    res = test_time(all_combs)
#
#    brute_total += res[0]
#    back_total += res[1]
#    graph_total += res[2]
#
#    run_total += res[3]
#
#print('Brute Force won', brute_total, 'out of', run_total, 'runs')
#print('Backtrack won', back_total, 'out of', run_total, 'runs')
#print('Graphwise won', graph_total, 'out of', run_total, 'runs')


#####################################################################################################

############### DOES THE ALGORITHM WORK FOR PRESENTATIONS DEFINED ON INTEGER ALPHABETS? #############

#The following are copies of v and w using integer list alphabets rather than character string alphabets
#The goal of this test is to ensure each algorithm works using either definition of presentation

int_alph = list(range(9))
rev_alph = list(reversed(int_alph))


forced = [0, 1, 2, 3, 4, 5, 6, 7, 8]
vi = Presentation(forced)
wi = Presentation(rev_alph)

presentation.add_rule(vi, [0, 1, 0, 1], [1, 0, 1, 0])
presentation.add_rule(vi, [2, 3, 3], [4, 4, 4])
presentation.add_rule(vi, [3, 0, 1, 5, 4], [6, 6, 2, 3, 0])
presentation.add_rule(vi, [3, 3, 3, 3, 3], [1, 6, 7])
presentation.add_rule(vi, [8], [7, 7, 6, 6, 1])
presentation.add_rule(vi, [3, 3, 3, 0, 2], [8])

presentation.add_rule(wi, [8, 7, 8, 7], [7, 8, 7, 8])
presentation.add_rule(wi, [6, 5, 5], [4, 4, 4])
presentation.add_rule(wi, [5, 8, 7, 3, 4], [2, 2, 6, 5, 8])
presentation.add_rule(wi, [5, 5, 5, 5, 5], [7, 2, 1])
presentation.add_rule(wi, [0], [1, 1, 2, 2, 7])
presentation.add_rule(wi, [5, 5, 5, 8, 6], [0])

##Works on the below example  
assert bool(brute_force_checker(vi, wi)) == bool(check_isomorphic(vi, wi)) == bool(check_isomorphic_graphwise(vi, wi)) == True
##Does NOT work on presentations of mixed type, unless the graphwise algorithm is used.


#####################################################################################################

################################ FIXING CANONICAL WORD FORM ERROR ###################################

#During development, we realized that storing canonical word forms as string presents a major issue.
#If a word uses more than 10 distinct elements, the next letter in the word will be represented as 
#the string '11'. Consider the word 'abcdefghijk'. In the originial canonical word form code, this 
#would have canonical form '012345678911'. But this word would then have identical canonical form 
#to the word 'abcdefghijbb' = '012345678911', since 'b' is represented by '1'. This is a clear error
#and so the code was changed, these tests were used to ensure the changes worked properly.

#print(h)
#print(i)

##This example now works!
#print(check_isomorphic(h, i))

##This example works as well!
#print(check_isomorphic(t, u))

##We now try an example as given above. the following presentations, in the old build,
##would have two words in the same class size, with the same length, and with the same 
##canonical word form: '01234567891010', but they are clearly different words. the new 
##build ensures that this will not happen, as can be seen by running this example and 
##in the check_isomorphic code, commenting in the 'words in canonical form, sorted' 
##print statement. 
#
#long1 = Presentation('abcdefghijk')
#presentation.add_rule(long1, 'abcdefghijkk', 'bcdijbcdijijk')
#
#long2 = Presentation('abcdefghijk')
#presentation.add_rule(long2, 'abcdefghijkba', 'ijfghkbfghkb')
#
#print(check_isomorphic(long1, long2))


#####################################################################################################

################## EDGE CASES: NO RULES AT ALL/NO ALPHABET OR RULES/ONLY TRIVIAL RULES ##############

#If two presentations have the same alphabet sizes and no rules, they should be isomorphic. This checks
#that the algorithms recognize this and return a bijection between the presentation alphabets 
#which, since they have no rules, is a free monoid isomorphism between them.
noalph1 = Presentation('abcdefghijklm')
noalph2 = Presentation('zyxwvutsrqpon')

#This example works!
assert bool(check_isomorphic(noalph1, noalph2) == check_isomorphic_graphwise(noalph1, noalph2) == brute_force_checker(noalph1, noalph2)) == True

#If the presentations have no rules but different size alphabets, they 
#are not isomorphic because there is no free monoid isomorphism between their alphabets.
#The following test ensures the algorithms handle this edge case.
noalph3 = Presentation('abcdefg')
assert check_isomorphic(noalph1, noalph3) == check_isomorphic_graphwise(noalph1, noalph3) == brute_force_checker(noalph1, noalph3) == False

#If the presentations are simply empty, they are trivially isomorphic. This test
#ensures that outputs match for all algorithms, should simply return True
empty1 = Presentation('')
empty2 = Presentation([])

assert check_isomorphic(empty1, empty2) == check_isomorphic_graphwise(empty1, empty2) == brute_force_checker(empty1, empty2) == True

#All algorithms will also return false if one presentation is empty and the other is nonempty.
assert check_isomorphic(empty1, a) == check_isomorphic_graphwise(empty1, a) == brute_force_checker(empty1, a) == False
assert check_isomorphic(b, empty2) == check_isomorphic_graphwise(b, empty2) == brute_force_checker(b, empty2) == False

#Algorithms should return 'True' if the only relations are trivial and the alphabet sizes
#are the same, and 'False' otherwise. 

#Algorithms were returning 'True' here, this is wrong, but has been fixed.
triv1 = Presentation('abc')
presentation.add_rule(triv1, 'aba',  'aba')

triv2 = Presentation('abcd') 
presentation.add_rule(triv2, 'bcd', 'bcd')

assert bool(brute_force_checker(triv1, triv2)) == bool(check_isomorphic(triv1, triv2)) == bool(check_isomorphic_graphwise(triv1, triv2)) == False

#The following presentation pairs were returning 'False' for all algorithms, this has been fixed.
triv3 = Presentation('abc')
presentation.add_rule(triv3, 'aba',  'aba')

triv4 = Presentation('abc') 
presentation.add_rule(triv4, 'aaa', 'aaa')

assert bool(brute_force_checker(triv3, triv4)) == bool(check_isomorphic(triv3, triv4)) == bool(check_isomorphic_graphwise(triv3, triv4)) == True

triv5 = Presentation('abcde')
presentation.add_rule(triv5, 'aba',  'aba')
presentation.add_rule(triv5, 'dde', 'ede')

triv6 = Presentation('abcde') 
presentation.add_rule(triv6, 'aaa', 'aaa')
presentation.add_rule(triv6, 'eed', 'ded')

assert bool(brute_force_checker(triv5, triv6)) == bool(check_isomorphic(triv5, triv6)) == bool(check_isomorphic_graphwise(triv5, triv6)) == True

######################################################################################################

############################# FIXING OUTPUT FOR SMALL ALPHABETS ######################################

#There was an issue with differing outputs for the algorithms on small relation word lists,
#for example the presentation p = <'abc' | 'a' = 'bc'>. These tests seek to fix that

#In these two presentations, 'a' and 'b' are redundant, respectively. This means that
#the presentations are isomorphic as free monoids with two generators, so the algorithms
#should return 'True'.
smallrl = Presentation('abc')
presentation.add_rule(smallrl, 'a', 'bc')
smallrl2 = Presentation('abc')
presentation.add_rule(smallrl2, 'b', 'cacc')

#If we have a redundant generator, some trivial results will arise after 
#generator-minimal presentation forms are found. These tests ensure that
#is indeed the case.

red1 = Presentation('abcdefgh')
presentation.add_rule(red1, 'a', 'dde')

red2 = Presentation('abcdefgh')
presentation.add_rule(red2, 'b', 'ccc')

assert bool(brute_force_checker(red1, red2)) == bool(check_isomorphic(red1, red2)) == bool(check_isomorphic_graphwise(red1, red2)) == True

#Try this again, but with slightly more complex versions
#of presentations red1 and red2

presentation.add_rule(red1, 'ggh', 'fff')
presentation.add_rule(red2, 'ffg', 'hhh')

assert bool(brute_force_checker(red1, red2)) == bool(check_isomorphic(red1, red2)) == bool(check_isomorphic_graphwise(red1, red2)) == True

#The outputs have been fixed, and should now match.
assert brute_force_checker(smallrl, smallrl2) == check_isomorphic(smallrl, smallrl2) == check_isomorphic_graphwise(smallrl, smallrl2) == True

#These presentations deal with the edge case where certain redundant generators are present
#which was wrongfully triggering the unused generator clause in all 3 algorithms.

#isomorphic
red1 = Presentation('abcdefgh')
presentation.add_rule(red1, 'a', 'dde')
presentation.add_rule(red1, 'ggh', 'fff')

red2 = Presentation('abcdefgh')
presentation.add_rule(red2, 'b', 'ccc')
presentation.add_rule(red2, 'ffg', 'hhh')

assert bool(brute_force_checker(red1, red2)) == bool(check_isomorphic(red1, red2)) == bool(check_isomorphic_graphwise(red1, red2)) == True

#isomorphic.
red3 = Presentation('abcdefghi')
presentation.add_rule(red3, 'a', 'dde')
presentation.add_rule(red3, 'i', 'bbc')
presentation.add_rule(red3, 'ggh', 'fff')

red4 = Presentation('abcdefgh')
presentation.add_rule(red4, 'b', 'ccc')
presentation.add_rule(red4, 'ffg', 'hhh')

assert bool(brute_force_checker(red3, red4)) == bool(check_isomorphic(red3, red4)) == bool(check_isomorphic_graphwise(red3, red4)) == True

#non-isomorphic.
red5 = Presentation('abcdefghi')
presentation.add_rule(red5, 'a', 'dde')
presentation.add_rule(red5, 'i', 'bbc')
presentation.add_rule(red5, 'i', 'bbc')
presentation.add_rule(red5, 'ggh', 'fff')

red6 = Presentation('fgh')
presentation.add_rule(red6, 'ffg', 'hhh')

assert bool(brute_force_checker(red5, red6)) == bool(check_isomorphic(red5, red6)) == bool(check_isomorphic_graphwise(red5, red6)) == False

#One more test regarding this issue.
red7 = Presentation('abcdefghi')
presentation.add_rule(red7, 'a', 'dde')
presentation.add_rule(red7, 'i', 'bbc')
presentation.add_rule(red7, 'ggh', 'fff')

red8 = Presentation('abcdefghi')
presentation.add_rule(red8, 'b', 'ccc')
presentation.add_rule(red8, 'ffg', 'hhh')

assert bool(brute_force_checker(red7, red8)) == bool(check_isomorphic(red7, red8)) == bool(check_isomorphic_graphwise(red7, red8)) == False

#Does this code now fix the outstanding issue due to the bug in libsemigroups?
bug1 = Presentation('abc')
presentation.add_rule(red7, 'aaa', 'aaa')

bug2 = Presentation('def')
presentation.add_rule(red8, 'ded', 'ded')

assert bool(brute_force_checker(bug1, bug2)) == bool(check_isomorphic(bug1, bug2)) == bool(check_isomorphic_graphwise(bug1, bug2)) == True

#Another example of presentations whose outputs failed to match:
tst1 = Presentation('abc')
presentation.add_rule(tst1, 'aa', 'ba')
tst2 = Presentation('abc')
presentation.add_rule(tst2, 'ab', 'bb')

#The outputs should now match.
assert bool(brute_force_checker(tst1, tst2)) == bool(check_isomorphic(tst1, tst2)) == bool(check_isomorphic_graphwise(tst1, tst2)) == True

#Another failed example
tst3 = Presentation('abc')
presentation.add_rule(tst3, 'aa', 'cc')
tst4 = Presentation('abc')
presentation.add_rule(tst4, 'aa', 'bb')

##This example has differed outputs for the presentations, but they are all 
##valid isomorphisms. brute_force_checker and check_isomorphic_graphwise
##send a -> a and c -> b, but check_isomorphic sends a -> b and c -> a.
##In context, it is OK that these outputs do not match.
#print(brute_force_checker(tst3, tst4))
#print(check_isomorphic(tst3, tst4))
#print(check_isomorphic_graphwise(tst3, tst4))


######################################################################################################

############################# TESTS FOR GRAPH ISOMORPHISM METHOD #####################################

#The following were used in the development of check_isomorphic_graphwise. Presentations
#pp and qq are very simple and isomorphic. We drew the graphs of both of them and then
#printed the graphs the code generated to make sure the algorithm was producing the 
#proper graphs.

pp = Presentation('abc')
presentation.add_rule(pp, 'aabc', 'ca')
presentation.add_rule(pp, 'baab', 'cb')
qq = Presentation('abc')
presentation.add_rule(qq, 'bbca', 'ab')
presentation.add_rule(qq, 'cbbc', 'ac')

rr = Presentation('abcd')
presentation.add_rule(rr, 'daaba', 'bcda')
presentation.add_rule(rr, 'bba', 'cab')

assert check_isomorphic_graphwise(pp, qq)
assert check_isomorphic_graphwise(rr, rr)
assert not(check_isomorphic_graphwise(pp, rr))

#######################################################################################

#################################### THE JAMES TEST ###################################

#This was an example concocted by J. D. Mitchell of two isomorphic presentations 
#that the algorithms determined were non-isomorphic. The tests below were 
#implemented to first check the example and then ensure it was fixed. 

#This issue has been resolved. 

ss = Presentation('ab')
presentation.add_rule(ss, 'aba', 'aaa')
presentation.add_rule(ss, 'bba', 'aaa')

tt = Presentation('ab')
presentation.add_rule(tt, 'aba', 'aaa')
presentation.add_rule(tt, 'bba', 'aba')
#print(ss.rules)
#print(tt.rules)

sss = pres_gen_min(ss)
ttt = pres_gen_min(tt)

#print(sss.rules)
#print(ttt.rules)

assert bool(check_isomorphic_graphwise(ss, tt)) == bool(check_isomorphic(ss, tt)) == bool(brute_force_checker(ss, tt)) == True

#The River variation, testing whether or not the 
#error induced by the above test was fixed.
ssss = Presentation('ab')
presentation.add_rule(ssss, 'aba', 'aaa')
presentation.add_rule(ssss, 'bba', 'aaa')

tttt = Presentation('ab')
presentation.add_rule(tttt, 'bab', 'bbb')
presentation.add_rule(tttt, 'aab', 'bab')

#print(ssss.rules)
#print(tttt.rules)

sssss = pres_gen_min(ssss)
ttttt = pres_gen_min(tttt)

#print(sssss.rules)
#print(ttttt.rules)

assert bool(check_isomorphic_graphwise(ssss, tttt)) == bool(check_isomorphic(ssss, tttt)) == bool(brute_force_checker(ssss, tttt)) == True

#one more test to ensure the method still works

#Presentations xx and yy are isomorphic. The mapping should be a -> z,
#b -> y, c -> x, etc.

xx = Presentation('ahgbedcf')
yy = Presentation('suzxwytv')

presentation.add_rule(yy, 'xwxw', 'yyyyy')
presentation.add_rule(yy, 'xwxw', 'wxwx')
presentation.add_rule(yy, 'tyy', 'uuu')
presentation.add_rule(yy, 'yxwvu', 'sstyx')
presentation.add_rule(yy, 'yyyyy', 'wsz')

presentation.add_rule(xx, 'cdcd', 'bbbbb')
presentation.add_rule(xx, 'cdcd', 'dcdc')
presentation.add_rule(xx, 'gbb', 'fff')
presentation.add_rule(xx, 'bcdef', 'hhgbc')
presentation.add_rule(xx, 'bbbbb', 'dha')

#Observe that the new pres_gen_min function has a non-negligible
#effect on the two presentations' rulesets.
gmx = pres_gen_min(xx)
gmy = pres_gen_min(yy)

assert Counter(gmx.rules) != Counter(xx.rules)
assert Counter(gmy.rules) != Counter(yy.rules)

expected_output = [('a', 'z'), ('b', 'y'), ('c', 'x'), ('d', 'w'), ('e', 'v'), ('f', 'u'), ('g', 't'), ('h', 's')]

#Ensure that the functions map to the expected output. 
assert check_isomorphic(xx, yy) == brute_force_checker(xx, yy) == check_isomorphic_graphwise(xx, yy) == expected_output

######################################################################################################

####################################### UNUSED/OLD TESTS/HELPERS #####################################

def print_info(p, q):

    print('Presentation 1 alphabet: ')
    print(p.alphabet())
    print('Presentation 1 rules: ')
    print(p.rules)
    print('\n')
    print('Presentation 2 alphabet: ')
    print(q.alphabet())
    print('Presentation 2 rules: ')
    print(q.rules)


def confirm_output(p, q, allpres):
    
    combo = []

    if (check_isomorphic(p, q) != brute_force_checker(p, q)): 
    
        for key, val in allpres.items():
            if duo[0] == val:
                combo.append(key)
            if duo[1] == val:
                combo.append(key)
            
    return combo

#  res = confirm_output(duo[0], duo[1], allpres)

   # if res:
    #    ctr += 1
     #   failed_combs.append(res)
    

#print('the combinations that failed: ', failed_combs)
#print('The amount of failed assertions: ', ctr)


#assert check_isomorphic(a, b) == brute_force_checker(a, b)
#assert check_isomorphic(a, c) == brute_force_checker(a, c)
   
#assert (check_isomorphic(a, a) == brute_force_checker(a, a)) 
#assert (check_isomorphic(c, c) == brute_force_checker(c, c)) 
#assert (check_isomorphic(d, d) == brute_force_checker(d, d)) 
#assert (check_isomorphic(e, e) == brute_force_checker(e, e)) 
#assert (check_isomorphic(f, f) == brute_force_checker(f, f)) 
#assert (check_isomorphic(g, g) == brute_force_checker(g, g)) 
#assert (check_isomorphic(h, h) == brute_force_checker(h, h)) 
#assert (check_isomorphic(i, i) == brute_force_checker(i, i))
#assert (check_isomorphic(j, j) == brute_force_checker(j, j)) 
#assert (check_isomorphic(k, k) == brute_force_checker(k, k)) 
#assert (check_isomorphic(l, l) == brute_force_checker(l, l)) 
#assert (check_isomorphic(m, m) == brute_force_checker(m, m)) 
#assert (check_isomorphic(n, n) == brute_force_checker(n, n)) 
#assert (check_isomorphic(o, o) == brute_force_checker(o, o)) 
#assert (check_isomorphic(p, p) == brute_force_checker(p, p)) 
#assert (check_isomorphic(q, q) == brute_force_checker(q, q)) 
#assert (check_isomorphic(r, r) == brute_force_checker(r, r)) 
#assert (check_isomorphic(s, s) == brute_force_checker(s, s)) 
#assert (check_isomorphic(t, t) == brute_force_checker(t, t)) 
#assert (check_isomorphic(u, u) == brute_force_checker(u, u)) 
#assert (check_isomorphic(v, v) == brute_force_checker(v, v)) 
  
#def backtrack_method():
    #check_isomorphic(bigpres, bigpres2)

#def graphwise_method():
    #check_isomorphic_graphwise(bigpres, bigpres2)


##Times for each algorithm to complete the check on bigpres1 and bigpres2. Note that 
##the backtrack algorithm is really starting to struggle with a presentation of this size.
#backtrack_time = timeit.timeit(backtrack_method, number=1)
#graph_time = timeit.timeit(graphwise_method, number=1)


##THESE TWO PRESENTATIONS PRODUCE DIFFERENT ISOMORPHISMS FOR EACH ALGORITHM. 
##This is because presentations 'b' and 'o' are identical, and hence there are 
##multiple choices for what maps to rules in them.

#print('Backtrack algorithm took:', backtrack_time, 'seconds')
#print('Graphwise algorithm took:', graph_time, 'seconds')

