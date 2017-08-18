from src.dice import *

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
