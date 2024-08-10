
from check_isomorphic import *
from brute_force import *
from check_isomorphic_graphwise import *
from presentation_normal_form import pres_gen_min
import itertools
import timeit

#Algorithms should return 'True' if the only relations are trivial and the alphabet sizes
#are the same, and 'False' otherwise. 

##Algorithms were returning 'True' here, this is wrong.
#triv1 = Presentation('abc')
#presentation.add_rule(triv1, 'aba',  'aba')
#
#triv2 = Presentation('abcd') 
#presentation.add_rule(triv2, 'bcd', 'bcd')
#
##print(triv1.rules)
##print(triv2.rules)
#
#triv1normal = pres_gen_min(triv1)
#triv2normal = pres_gen_min(triv2)
#
##print(triv1normal.alphabet())
##print(triv1normal.rules)
#
##print(triv2normal.alphabet())
##print(triv2normal.rules)
#
#print(brute_force_checker(triv1, triv2))
#print(check_isomorphic(triv1, triv2))
#print(check_isomorphic_graphwise(triv1, triv2))
#
#triv3 = Presentation('abc')
#presentation.add_rule(triv3, 'aba',  'aba')
#
#triv4 = Presentation('abc') 
#presentation.add_rule(triv4, 'aaa', 'aaa')
#
#print(brute_force_checker(triv3, triv4))
#print(check_isomorphic(triv3, triv4))
#print(check_isomorphic_graphwise(triv3, triv4))
#
#triv5 = Presentation('abcde')
#presentation.add_rule(triv5, 'aba',  'aba')
#presentation.add_rule(triv5, 'dde', 'ede')
#
#triv6 = Presentation('abcde') 
#presentation.add_rule(triv6, 'aaa', 'aaa')
#presentation.add_rule(triv6, 'eed', 'ded')
#
#print(brute_force_checker(triv5, triv6))
#print(check_isomorphic(triv5, triv6))
#print(check_isomorphic_graphwise(triv5, triv6))

red1 = Presentation('abcdefgh')
presentation.add_rule(red1, 'a', 'dde')
presentation.add_rule(red1, 'ggh', 'fff')

red2 = Presentation('abcdefgh')
presentation.add_rule(red2, 'b', 'ccc')
presentation.add_rule(red2, 'ffg', 'hhh')

print(brute_force_checker(red1, red2))
print(check_isomorphic(red1, red2))
print(check_isomorphic_graphwise(red1, red2))

l = Presentation('abcdefgh')
m = Presentation('abcdefg')
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
#Not isomorphic because one has more unused generators than the others
print(brute_force_checker(l, m))
print(check_isomorphic(l, m))
print(check_isomorphic_graphwise(l, m))


red3 = Presentation('abcdefghi')
presentation.add_rule(red3, 'a', 'dde')
presentation.add_rule(red3, 'i', 'bbc')
presentation.add_rule(red3, 'ggh', 'fff')

red4 = Presentation('abcdefgh')
presentation.add_rule(red4, 'b', 'ccc')
presentation.add_rule(red4, 'ffg', 'hhh')

print(brute_force_checker(red3, red4))
print(check_isomorphic(red3, red4))
print(check_isomorphic_graphwise(red3, red4))

red5 = Presentation('abcdefghi')
presentation.add_rule(red5, 'a', 'dde')
presentation.add_rule(red5, 'i', 'bbc')
presentation.add_rule(red5, 'ggh', 'fff')

red6 = Presentation('fgh')
#presentation.add_rule(red4, 'b', 'ccc')
presentation.add_rule(red6, 'ffg', 'hhh')

print(brute_force_checker(red5, red6))
print(check_isomorphic(red5, red6))
print(check_isomorphic_graphwise(red5, red6))

red7 = Presentation('abc')
presentation.add_rule(red7, 'a', 'bb')

red8 = Presentation('abc')
presentation.add_rule(red8, 'b', 'aca')

print(brute_force_checker(red7, red8))
print(check_isomorphic(red7, red8))
print(check_isomorphic_graphwise(red7, red8))
