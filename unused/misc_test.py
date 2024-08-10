from libsemigroups_pybind11 import Kambites, Presentation, presentation, congruence_kind
from presentation_normal_form import pres_gen_min
from collections import Counter

h = Presentation('abcdefg')

presentation.add_rule(h, 'ab', 'ba')
presentation.add_rule(h, 'afcfc', 'bbb')
presentation.add_rule(h, 'd', 'afg')
presentation.add_rule(h, 'eeff', 'ddd')
presentation.add_rule(h, 'gg', 'bbcce')
presentation.add_rule(h, 'bbge', 'fff')

#Create Kambites objects from the presentations
kp = Kambites()
    #kq = Kambites()

kp.set_alphabet(h.alphabet())
    #kq.set_alphabet(qq.alphabet())

i = 0
while i < (len(h.rules) - 1):
    kp.add_rule(h.rules[i], h.rules[i+1])
    i += 2
    
    #j = 0
    #while j < (len(qq.rules) - 1):
    #    kq.add_rule(qq.rules[j], qq.rules[j+1])
    #    j += 2
    
    #If either presentation is C(1), kill the algorithm and return a warning.

print(kp.small_overlap_class())

hh = pres_gen_min(h)

print(hh.alphabet(), '\n', hh.rules)

kh = Kambites()
    #kq = Kambites()

kh.set_alphabet(hh.alphabet())
    #kq.set_alphabet(qq.alphabet())
print(kh.alphabet())

i = 0
while i < (len(hh.rules) - 1):
    kh.add_rule(hh.rules[i], hh.rules[i+1])
    i += 2

print(list(kh.rules()))
    #j = 0
    #while j < (len(qq.rules) - 1):
    #    kq.add_rule(qq.rules[j], qq.rules[j+1])
    #    j += 2
    
    #If either presentation is C(1), kill the algorithm and return a warning.

print(kh.small_overlap_class())

