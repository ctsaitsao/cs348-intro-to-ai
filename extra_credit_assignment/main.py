import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KBTest(unittest.TestCase):

    def setUp(self):
        # # Assert starter facts
        self.KB = KnowledgeBase([], [])
        
    def compare(self, expected, actual):
        elist = expected.split('\n')
        alist = actual.split('\n')
        for e, a in zip(elist, alist):
            if e.lower() != a.rstrip().lower():
                self.assertEquals('"{0}" ({1} lead spaces)'.format(e, len(e) - len(e.lstrip())), 
                    '"{0}" ({1} lead spaces)'.format(a, len(a) - len(a.strip())))

    def test01(self):
        # KB does not contain
        actual = self.KB.kb_explain(read.parse_input("fact: (notContains kb fact)"))
        self.compare("Fact is not in the KB", actual)
        actual = self.KB.kb_explain(read.parse_input("rule: ((contains bowl flour) (contains bowl water)) -> (contains bowl wetFlour)"))
        self.compare("Rule is not in the KB", actual)

    def test02(self):
        # asserted
        f1 = read.parse_input("fact: (genls nyala antelope)")
        f2 = read.parse_input("fact: (genls antelope herbivore)")
        f3 = read.parse_input("fact: (eats herbivore leaves)")
        f4 = read.parse_input("fact: (isa leaves plantBasedFood)")
        f5 = read.parse_input("fact: (eats nyala plantBasedFood)")

        r1 = read.parse_input("rule: ((genls ?x ?y) (genls ?y ?z) (eats ?z leaves)) -> (eats ?x leaves)")
        r2 = read.parse_input("rule: ((eats ?x plantBasedFood) (isa ?y plantBasedFood)) -> (eats ?x ?y)")

        # inferred
        f0 = read.parse_input("fact: (eats nyala leaves)")
        r3 = read.parse_input("rule: ((genls antelope ?z) (eats ?z leaves)) -> (eats nyala leaves)")
        r4 = read.parse_input("rule: ((eats herbivore leaves)) -> (eats nyala leaves)")
        r5 = read.parse_input("rule: ((isa ?y plantBasedFood)) -> (eats nyala ?y)")

        # first set of support
        f0.supported_by.append([f3, r4])
        r4.supported_by.append([f2, r3])
        r3.supported_by.append([f1, r1])        

        # second set of support
        f0.supported_by.append([f4, r5])
        r5.supported_by.append([f5, r2])

        f1.asserted = True
        f2.asserted = True
        f3.asserted = True
        f4.asserted = True
        r1.asserted = True
        r2.asserted = True

        f0.asserted = False
        r3.asserted = False
        r4.asserted = False
        r5.asserted = False

        self.KB.facts.extend([f0,f1,f2,f3,f4,f5])
        self.KB.rules.extend([r1,r2,r3,r4,r5])

        self.expected = '\
fact: (eats nyala leaves)\n\
  SUPPORTED BY\n\
    fact: (eats herbivore leaves) ASSERTED\n\
    rule: ((eats herbivore leaves)) -> (eats nyala leaves)\n\
      SUPPORTED BY\n\
        fact: (genls antelope herbivore) ASSERTED\n\
        rule: ((genls antelope ?z), (eats ?z leaves)) -> (eats nyala leaves)\n\
          SUPPORTED BY\n\
            fact: (genls nyala antelope) ASSERTED\n\
            rule: ((genls ?x ?y), (genls ?y ?z), (eats ?z leaves)) -> (eats ?x leaves) ASSERTED\n\
  SUPPORTED BY\n\
    fact: (isa leaves plantBasedFood) ASSERTED\n\
    rule: ((isa ?y plantBasedFood)) -> (eats nyala ?y)\n\
      SUPPORTED BY\n\
        fact: (eats nyala plantBasedFood) ASSERTED\n\
        rule: ((eats ?x plantBasedFood), (isa ?y plantBasedFood)) -> (eats ?x ?y) ASSERTED\
'
        actual = self.KB.kb_explain(read.parse_input("fact: (eats nyala leaves)"))
        self.compare(self.expected, actual)


if __name__ == '__main__':
    unittest.main()
