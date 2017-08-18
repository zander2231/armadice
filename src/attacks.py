from dice import *
from upgrade import *
from result import Result

class Attack(object):
    def __init__(self):
        self.dice = []
        self.upgrades = []

    def generateResult(self):
        result = Result()
        dice = self.dice[:]

        for die in dice:
            result.add(die, die.chooseSide())

        for upgrade in self.upgrades:
            result = upgrade.modifyResult(result)

        return result

    def addDie(self, die, count=1):
        for i in range(count):
            self.dice.append(die)

    def addUpgrade(self, upgrade):
        self.upgrades.append(upgrade)
