import unittest
import collections

from normalform import gen_min
from presentation_normal_form import pres_gen_min
from libsemigroups_pybind11 import FpSemigroup, Presentation, presentation

class TestGenMin(unittest.TestCase):

    def test_no_rl(self):
        S = FpSemigroup()
        S.set_alphabet('abc')
        self.assertEqual(gen_min(S), None)

    def test_no_rdnts(self):
        S = FpSemigroup()
        S.set_alphabet('abcde')
        S.add_rule("bab", "ccd")
        S.add_rule("ee", "bcbc")
        S.add_rule("ebbbe", "acdc")
        Srlstp = list(S.rules())
        Srls = []
        for rl in Srlstp:
            Srls.append(rl[0])
            Srls.append(rl[1])

        p = Presentation('abcde')
        presentation.add_rule(p, 'bab', 'ccd')
        presentation.add_rule(p, 'ee', 'bcbc')
        presentation.add_rule(p, 'ebbbe', 'acdc')
        oldrls = p.rules
        pres_gen_min(p)

        self.assertEqual(gen_min(S), None)
        self.assertNotEqual(p.rules, oldrls)

    def test_1_rdnt(self):
        S = FpSemigroup()
        S.set_alphabet('cdefg')
        S.add_rule('ef', 'fe')
        S.add_rule('c', 'ggd')
        S.add_rule('ff', 'c')
        Srls = list(S.rules())
        newS = gen_min(S)
        newrls = list(newS.rules())
        self.assertEqual(newS.alphabet(), 'defg')
        self.assertEqual(newrls, [('ef', 'fe'), ('ff', 'ggd'),])
        self.assertEqual(S.equal_to('efef', 'eggde'), True)
    
    def test_mult_rdnts_1(self):
        S = FpSemigroup()
        S.set_alphabet('abcdefghi')
        S.add_rule('a', 'bbcc')
        S.add_rule('ddff', 'i')
        S.add_rule('hh', 'g')
        S.add_rule('e', 'dcdc')
        newS = gen_min(S)
        newrls = list(newS.rules())
        self.assertEqual(newS.alphabet(), 'bcdfh')
        self.assertEqual(gen_min(newS), None)

    def test_mult_rdnts_2(self):
        S = FpSemigroup()
        S.set_alphabet('abcdefghi')
        S.add_rule('d', 'ffg')
        S.add_rule('bcbc', 'cc')
        S.add_rule('bbb', 'd')
        S.add_rule('biib', 'e')
        S.add_rule('iii', 'h')
        S.add_rule('h', 'gg')
        S.add_rule('d', 'iii')
        newS = gen_min(S)
        newrls = list(newS.rules())
        #print(newS.alphabet())
        #print("New rules for S are: ", newrls)
        self.assertEqual(newS.alphabet(), 'abcfgi')
        self.assertTrue(('bcbc', 'cc') in newrls)
        #self.assertTrue(newS.equal_to('iiibbbffg', 'gggggg'))
        #self.assertTrue(newS.equal_to('iiibbbffg', 'ffgbbbiii'))
        #self.assertEqual(newS.equal_to('gg', 'iii'), True)
        T = FpSemigroup()
        T.set_alphabet('abcdefghi')
        T.add_rule('h', 'gg')
        T.add_rule('d', 'iii')
        T.add_rule('iii', 'h')
        T.add_rule('biib', 'e')
        T.add_rule('bbb', 'd')
        T.add_rule('bcbc', 'cc')
        T.add_rule('d', 'ffg')
        newT = gen_min(T)
        newrlsT = list(newT.rules())
        #print("New rules for T are: ", newrlsT)
        self.assertEqual(collections.Counter(newrls), collections.Counter(newrlsT))


if __name__ == "__main__":
    unittest.main()
    
