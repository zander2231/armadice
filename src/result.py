from side import *

class Result(object):
    def __init__(self):
        self.sides = {}

    def add(self, die, side):
        if die not in self.sides.keys():
            self.sides[die] = []
        self.sides[die].append(side)

    def getAll(self, die):
        if die not in self.sides.keys():
            return []
        return self.sides[die]

    def totalDamage(self):
        total = 0
        for die, sides in self.sides.items():
            for side in sides:
                total += side.damage()

        return total

    def hasCrit(self):
        for die, sides in self.sides.items():
            for side in sides:
                if side.isCrit():
                    return True
        return False

    def removeLowestSide(self):
        lowDie = None
        lowSides = [HitCrit()]

        for die, sides in self.sides.items():
            std = sorted(sides, key=lambda side: side.good)
            if std[0].good < lowSides[0].good:
                lowDie = die
                lowSides = std

        if lowDie is not None:
            del lowSides[0]
            self.sides[lowDie] = lowSides

    def accuracyCount(self):
        total = 0
        for die, sides in self.sides.items():
            for side in sides:
                total += side.accuracy()
        return total

