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

def checkModifyResult(test, damage, acc, crit):
    result = test.testObj.modifyResult(test.result)
    test.assertEqual(result.totalDamage(), damage)
    test.assertEqual(result.accuracyCount(), acc)
    test.assertEqual(result.hasCrit(), crit)

def setupRandom():
    random = FakeRandom()
    DiceRandom.instance = random
    return random

class AllHits(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit, Hit,Hit, Hit,Hit, Hit,Hit, Hit]

class AllCrits(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Crit, Crit,Crit, Crit,Crit, Crit,Crit, Crit]

class AllAcc(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Acc, Acc,Acc, Acc,Acc, Acc,Acc, Acc]
