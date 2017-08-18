import unittest
from dicerolls import *
from utils import *

class TestDualTurbo(unittest.TestCase):
    def setUp(self):
        self.random = setupRandom()

    def testDiceAdded(self):
        self.choice = 1
        testObj = DualTurbo()
        result = Result()
        result.add(Red(), Miss())
        result = testObj.modifyResult(result)

        self.assertEqual(len(result.sides[Red()]), 1)

class TestH9(unittest.TestCase):
    def setUp(self):
        self.testObj = H9()
        self.result = Result()

    def testBlueHit(self):
        self.result.add(Blue(), Hit())
        checkModifyResult(self, 0,1,False)

    def testRedCritChanged(self):
        self.result.add(Red(), Crit())
        checkModifyResult(self, 0,1,False)

    def testBlackDiceNotAffected(self):
        self.result.add(Black(), Hit())
        checkModifyResult(self, 1,0,False)

    def testNothingIfAlreadyAcc(self):
        self.result.add(Blue(), Hit())
        self.result.add(Blue(), Acc())
        checkModifyResult(self, 1,1,False)

    def testPreferToChangeHits(self):
        self.result.add(Blue(), Crit())
        self.result.add(Blue(), Hit())
        checkModifyResult(self, 1,1,True)

    def testPreferToHitsToDoubles(self):
        self.result.add(Red(), Double())
        self.result.add(Blue(), Hit())
        checkModifyResult(self, 2,1,False)

class TestOrdanenceExp(unittest.TestCase):
    def setUp(self):
        self.testObj = OrdinanceExp()
        self.result = Result()

    def testEmptyOk(self):
        checkModifyResult(self, 0, 0, False)

    def testRedNotChanged(self):
        self.result.add(Red(), Miss())  
        checkModifyResult(self, 0, 0, False)

    def testBlackHitCritNotRerolled(self):
        self.result.add(Black(), Hit())
        self.result.add(Black(), HitCrit())
        checkModifyResult(self, 3, 0, True)

    def testMissRerolled(self):
        random = setupRandom()
        random.choice = 0
        self.result.add(Black(), Miss())
        checkModifyResult(self, 1, 0, False)
