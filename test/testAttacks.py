import unittest
from utils import *
from src.attacks import *

class FakeUpgrade(object):
    def __init__(self):
        self.result = Result()

    def modifyResult(self, result):
        return self.result

class TestResult(unittest.TestCase):
    def testLowDieDropped(self):
        self.checkDrop(Crit(), Hit(), 1, True)
        self.checkDrop(Miss(), Hit(), 1, False)
        self.checkDrop(Miss(), Acc(), 0, False)
        self.checkDrop(Double(), Hit(), 2, False)
        self.checkDrop(Double(), HitCrit(), 2, True)

    def checkDrop(self, sideOne, sideTwo, damage, crit):
        result = Result()
        result.add(Blue(),sideOne)
        result.add(Blue(),sideTwo)
        result.removeLowestSide()
        self.assertEqual(result.totalDamage(), damage)
        self.assertEqual(result.hasCrit(), crit)

    def testRemoveLowSideWorksAcrossTypes(self):
        result = Result()
        result.add(Blue(),Crit())
        result.add(Red(),Double())
        result.removeLowestSide()
        self.assertEqual(result.totalDamage(), 2)
        self.assertEqual(result.hasCrit(), False)

    def testRemoveLowSideOkEmpty(self):
        result = Result()
        result.removeLowestSide()
        self.assertEqual(len(result.sides), 0)

class TestAttackWithResult(unittest.TestCase):
    def setUp(self):
        self.random = setupRandom()
        self.testObj = Attack()

    def testAttackWithNoDice(self):
        result = self.testObj.generateResult()
        self.assertEqual(result.totalDamage(), 0)

    def testAttackWithOneHit(self):
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()
        self.assertEqual(result.totalDamage(), 1)

    def testAttackWith2AddedAtOnce(self):
        self.testObj.addDie(AllHits(), 2)
        result = self.testObj.generateResult()
        self.assertEqual(result.totalDamage(), 2)

    def testAttackWithTwoHits(self):
        self.testObj.addDie(AllHits())
        self.testObj.addDie(AllCrits())
        result = self.testObj.generateResult()
        self.assertEqual(result.totalDamage(), 2)

    def testHasNoCrit(self):
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()
        self.assertEqual(result.hasCrit(), False)

    def testHasCrit(self):
        self.testObj.addDie(AllCrits())
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()
        self.assertEqual(result.hasCrit(), True)

    def testHasNoAcc(self):
        self.testObj.addDie(AllCrits())
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()
        self.assertEqual(result.accuracyCount(), 0)

    def testHasOneAcc(self):
        self.testObj.addDie(AllCrits())
        self.testObj.addDie(AllAcc())
        result = self.testObj.generateResult()
        self.assertEqual(result.accuracyCount(), 1)

    def testHasTwoAcc(self):
        self.testObj.addDie(AllAcc(), 2)
        result = self.testObj.generateResult()
        self.assertEqual(result.accuracyCount(), 2)

    def testAddUpgradeCanModifyResult(self):
        upgrade = FakeUpgrade()
        upgrade.result.add(Blue(), Crit())
        self.testObj.addUpgrade(upgrade)
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()

        self.assertEqual(result.hasCrit(), True)