import unittest
from dicerolls import *

class FakeRandom(object):
    def __init__(self):
        self.choice = 0

    def randint(self, low, high):
        return self.choice

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
        self.assertIsInstance(self.die.chooseSide(), Hit)

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

    def testAddUpgradeLetsUpgradeKnowAboutFinalDieRoll(self):
        upgrade = FakeUpgrade()
        self.testObj.addUpgrade(upgrade)
        self.testObj.addDie(AllHits())
        self.testObj.addDie(AllCrits())
        self.testObj.generateResult()

        self.assertIsInstance(upgrade.rolledDie[0], AllHits)
        self.assertIsInstance(upgrade.rolledSide[0], Hit)
        self.assertIsInstance(upgrade.rolledDie[1], AllCrits)
        self.assertIsInstance(upgrade.rolledSide[1], Crit)

    def testAddUpgradeCanModifyResult(self):
        upgrade = FakeUpgrade()
        upgrade.result = Crit()
        self.testObj.addUpgrade(upgrade)
        self.testObj.addDie(AllHits())
        result = self.testObj.generateResult()

        self.assertEqual(result.hasCrit(), True)

    def testUpgradeCanModifyStartingDice(self):
        upgrade = FakeUpgrade()
        upgrade.dice = [AllCrits(), AllHits()]
        self.testObj.addUpgrade(upgrade)
        self.testObj.addDie(Blue())

        result = self.testObj.generateResult()
        self.assertEqual(result.totalDamage(), 2)

class FakeUpgrade(object):
    def __init__(self):
        self.dice = None;
        self.rolledDie = []
        self.rolledSide = []
        self.result = Hit()

    def modifyDice(self, dice):
        if self.dice is None:
            return dice

        d = self.dice
        self.dice = dice
        return d

    def modifyRoll(self, die, side):
        self.rolledDie.append(die)
        self.rolledSide.append(side)
        return self.result

    def modifyResult(self, result):
        return result

class TestDualTurbo(unittest.TestCase):
    def testDiceAdded(self):
        testObj = DualTurbo()
        self.assertIsInstance(testObj.modifyDice([])[0], Red)

    def testLowDieDropped(self):
        self.checkDrop(Crit(), Hit(), 1, True)
        self.checkDrop(Miss(), Hit(), 1, False)
        self.checkDrop(Miss(), Acc(), 0, False)
        self.checkDrop(Double(), Hit(), 2, False)
        self.checkDrop(Double(), HitCrit(), 2, True)

    def checkDrop(self, sideOne, sideTwo, damage, crit):
        testObj = DualTurbo()
        result = Result()
        result.add(sideOne)
        result.add(sideTwo)
        result = testObj.modifyResult(result)
        self.assertEqual(result.totalDamage(), damage)
        self.assertEqual(result.hasCrit(), crit)

class TestH9(unittest.TestCase):
    def testHitInAccOut(self):
        testObj = H9()
        result = Result()
        result.add(Hit())
        testObj.modifyResult(result)
        self.assertEqual(result.accuracyCount(), 1)

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
