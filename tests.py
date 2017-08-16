import unittest
from dicerolls import *

class FakeRandom(object):
    def __init__(self):
        self.choice = 0

    def randint(self, low, high):
        return self.choice

def checkSides(sideOne, sideTwo):
    equal  = True 
    equal = equal and sideOne.hit == sideTwo.hit
    equal = equal and sideOne.crit == sideTwo.crit
    equal = equal and sideOne.acc == sideTwo.acc
    equal = equal and sideOne.good == sideTwo.good
    return equal

class AllHits(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit(), Hit(),Hit(), Hit(),Hit(), Hit(),Hit(), Hit()]

class AllCrits(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Crit(), Crit(),Crit(), Crit(),Crit(), Crit(),Crit(), Crit()]

class AllAcc(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Acc(), Acc(),Acc(), Acc(),Acc(), Acc(),Acc(), Acc()]

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

class TestRedDice(unittest.TestCase):
    def setUp(self):
        self.random = FakeRandom()
        DiceRandom.instance = self.random

        self.die = Red()

    def getAverage(self):
        return 0.75

    def testAverageDamage(self):
        self.assertEqual(self.die.averageDamage(), self.getAverage())

    def testChooseSide(self):
        self.random.choice = 0
        self.assertTrue(checkSides(self.die.chooseSide(), Hit()))

class TestBlueDice(TestRedDice):
    def setUp(self):
        TestRedDice.setUp(self)
        self.die = Blue()

class TestBlackDice(TestRedDice):
    def setUp(self):
        TestRedDice.setUp(self)
        self.die = Black()

    def getAverage(self):
        return 1.0

class TestSides(unittest.TestCase):
    def testHit(self):
        self.assertEqual(Hit().damage(), 1)
        self.assertEqual(Hit().isCrit(), False)
        self.assertEqual(Hit().accuracy(), 0)

    def testCrit(self):
        self.assertEqual(Crit().damage(), 1)
        self.assertEqual(Crit().accuracy(), 0)
        self.assertEqual(Crit().isCrit(), True)

    def testAcc(self):
        self.assertEqual(Acc().damage(), 0)
        self.assertEqual(Acc().accuracy(), 1)
        self.assertEqual(Acc().isCrit(), False)

    def testDouble(self):
        self.assertEqual(Double().damage(), 2)
        self.assertEqual(Double().accuracy(), 0)
        self.assertEqual(Double().isCrit(), False)

    def testHitCri(self):
        self.assertEqual(HitCrit().damage(), 2)
        self.assertEqual(HitCrit().isCrit(), True)
        self.assertEqual(HitCrit().accuracy(), 0)

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
        self.random = FakeRandom()
        DiceRandom.instance = self.random

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

class FakeUpgrade(object):
    def __init__(self):
        self.result = Result()

    def modifyResult(self, result):
        return self.result

class TestDualTurbo(unittest.TestCase):
    def setUp(self):
        self.random = FakeRandom()
        DiceRandom.instance = self.random

    def testDiceAdded(self):
        self.choice = 1
        testObj = DualTurbo()
        result = Result()
        result.add(Red(), Miss())
        result = testObj.modifyResult(result)

        self.assertEqual(len(result.sides[Red()]), 1)

class TestH9(unittest.TestCase):
    def testHitInAccOut(self):
        testObj = H9()
        result = Result()
        result.add(Blue(), Hit())
        testObj.modifyResult(result)
        self.assertEqual(result.accuracyCount(), 1)
        self.assertEqual(result.totalDamage(), 0)

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
