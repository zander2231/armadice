import unittest
from dicerolls import *
from utils import *

class HalfCrits(Die):
    def __init__(self):
        Die.__init__(self)
        self.isCrit = False

    def chooseSide(self):
        self.isCrit = not self.isCrit
        if self.isCrit:
            return Crit()
        else:
            return Hit()

class TestResults(unittest.TestCase):
    def setUp(self):
        self.attack = Attack()
        self.testObj = Results()

    def testNoDiceInAttack(self):
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.damages, {0:1})

    def testTwoDiceInAttack(self):
        self.attack.addDie(AllHits(),2)
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.damages, {2:1})
        self.assertEqual(self.testObj.percentAcc(), {2:0.0})

    def testAccuracyInAttack(self):
        self.attack.addDie(AllAcc())
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.percentAcc(), {0:1.0})

    def testNoDiceIsCrit(self):
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.percentCrit(), {0:0.0})

    def testTwoDiceWithNoCrits(self):
        self.attack.addDie(AllHits(),2)
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.percentCrit(), {2:0.0})

    def testTwoDiceWithCrits(self):
        self.attack.addDie(AllCrits(),2)
        self.testObj.generate(1, self.attack)
        self.assertEqual(self.testObj.percentCrit(), {2:1.0})

    def testTwoDiceWithHalfCrits(self):
        self.attack.addDie(HalfCrits())
        self.attack.addDie(HalfCrits())
        self.testObj.generate(2, self.attack)
        self.assertEqual(self.testObj.percentCrit(), {2:0.5})
