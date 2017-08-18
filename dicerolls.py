import random

class DiceRandom(object):
    instance = random

    def rollSide(self):
        return DiceRandom.instance.randint(0,7)

class Side(object):
    def __init__(self):
        self.hit = 0
        self.crit = 0
        self.acc = 0
        self.good = 0

    def damage(self):
        return self.hit + self.crit

    def accuracy(self):
        return self.acc

    def isCrit(self):
        return self.crit > 0

    def setTo(self, side):
        self.hit = side.hit
        self.crit = side.crit
        self.acc = side.acc
        self.good = side.good
        self.type = side.type

    def __str__(self):
        return self.type
    def __repr__(self):
        return self.__str__()

def Miss():
    side = Side()
    side.type = "miss"
    return side

def Hit():
    side = Side()
    side.good = 2
    side.hit = 1
    side.good = 1
    side.type = "hit"
    return side

def Double():
    side = Side()
    side.good = 4
    side.hit = 2
    side.type = "double"
    return side

def Crit():
    side = Side()
    side.good = 3
    side.crit = 1
    side.type = "crit"
    return side

def Acc():
    side = Side()
    side.good = 1
    side.acc = 1
    side.type = "acc"
    return side

def HitCrit():
    side = Side()
    side.good = 5
    side.crit = 1
    side.hit = 1
    side.type = "hitcrit"
    return side

class Die(object):
    def averageDamage(self):
       total = 0.0
       for side in self.sides:
          total += side().damage()
       return total/len(self.sides)

    def chooseSide(self):
        roll = DiceRandom().rollSide()
        side = self.sides[roll]
        return side()

    def __hash__(self):
        return hash(type(self).__name__)

    def __eq__(self, other):
        return type(self).__name__ == type(other).__name__ 

class Red(Die):
    def __init__(self):
        super(Red, self).__init__()
        self.sides = [ Hit, Hit, Double, Crit, Crit, Acc, Miss, Miss]

class Blue(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit, Hit, Hit, Hit, Crit, Crit, Acc, Acc]

class Black(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit, Hit, Hit, Hit, HitCrit, HitCrit, Miss, Miss]

class Upgrade(object):
    def modifyResult(self, result):
        return result

class Reroll(Upgrade):
    pass

class TRC(Upgrade):
    pass

class LeadingShot(Upgrade):
    pass

class SW7(Upgrade):
    def modifyResult(self, result):
        for side in result.sides[Blue]:
            if side.damage() == 0:
                side.setTo(Hit())
        return result

class DualTurbo(Upgrade):
    def modifyResult(self, result):
        result.add(Red(), Red().chooseSide())
        result.removeLowestSide()
        return result

class OrdinanceExp(Upgrade):
    def modifyResult(self, result):
        for side in result.getAll(Black()):
            if side.damage() == 0:
                side.setTo(Black().chooseSide())
        return result

class H9(Upgrade):
    def modifyResult(self,result):
        if result.accuracyCount() > 0:
            return result

        sides = result.getAll(Red()) + result.getAll(Blue())
        foundSide = Miss()
        for side in sides:
            if side.damage() > 0:
                if not side.isCrit() and side.damage() < 2:
                    foundSide = side
                    break
                else:
                    foundSide = side

        foundSide.setTo(Acc())
        return result

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

class Results(object):
    def __init__(self):
        self.damages = {}
        self.crits = {}
        self.accuracy = {}

    def generate(self, nResults, withAttack):
        for r in range(nResults):
            result = withAttack.generateResult()
            self.updateDamage(result)
            self.updateCrits(result)
            self.updateAccuracy(result)

    def percentCrit(self):
        percents = {}
        for d, total in self.damages.items():
            critCount = 0.0
            if d in self.crits.keys():
                critCount = self.crits[d]
            percents[d] = critCount/total

        return percents

    def percentAcc(self):
        percents = {}
        for d, total in self.damages.items():
            accuracyCount = 0.0
            if d in self.accuracy.keys():
                accuracyCount = self.accuracy[d]
            percents[d] = accuracyCount/total

        return percents

    def updateDamage(self, result):
        self.updateCounts(result, self.damages)

    def updateCrits(self, result):
        if not result.hasCrit():
            return

        self.updateCounts(result, self.crits)

    def updateAccuracy(self, result):
        if result.accuracyCount() == 0:
            return

        self.updateCounts(result, self.accuracy)

    def updateCounts(self, result, tracker):
        damage = result.totalDamage()
        if damage in tracker.keys():
            tracker[damage] += 1
        else:
            tracker[damage] = 1.0

def main():
    #read in command line args
    #generate attack
    attack = Attack()
    attack.addDie(Red(), 4)
    # attack.addDie(Blue(), 4)
    # attack.addUpgrade(SW7())
    # attack.addUpgrade(DualTurbo())

    # attack.addDie(Blue(), 2)
    # attack.addDie(Black(), 3)
    # attack.addUpgrade(OrdinanceExp())
    # attack.addUpgrade(H9())

    #generate rolls histogram for number of iterations
    results = Results()
    n = 1000
    results.generate(n, attack)
    percentCrit = results.percentCrit()
    percentAcc = results.percentAcc()

    print "Dam results crit  acc"
    for damage, count in results.damages.items():
        percentHit = count/n
        print "{!s:2}:     {:3.0%} {:4.0%} {:4.0%}  ".format(damage, percentHit, percentCrit[damage], percentAcc[damage]) + "X"*int(percentHit*100)

if __name__ == "__main__":
    main()