import random

class DiceRandom(object):
    instance = random

    def rollSide(self):
        return DiceRandom.instance.randint(0,7)

class Miss(object):
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

class Hit(Miss):
    def __init__(self):
        Miss.__init__(self)
        self.good = 2
        self.hit = 1
        self.good = 1

class Double(Miss):
    def __init__(self):
        Miss.__init__(self)
        self.good = 4
        self.hit = 2

class Crit(Miss):
    def __init__(self):
        Miss.__init__(self)
        self.good = 3
        self.crit = 1

class Acc(Miss):
    def __init__(self):
        Miss.__init__(self)
        self.good = 1
        self.acc = 1

class HitCrit(Miss):
    def __init__(self):
        Miss.__init__(self)
        self.good = 5
        self.crit = 1
        self.hit = 1

class Die(object):
    def averageDamage(self):
       total = 0.0
       for side in self.sides:
          total += side.damage()
       return total/len(self.sides)

    def chooseSide(self):
        side = DiceRandom().rollSide()
        return self.sides[side]

class Red(Die):
    def __init__(self):
        super(Red, self).__init__()
        self.sides = [ Hit(), Hit(), Double(), Crit(), Crit(), Acc(), Miss(), Miss()]

class Blue(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit(), Hit(), Hit(), Hit(), Crit(), Crit(), Acc(), Acc()]

class Black(Die):
    def __init__(self):
        Die.__init__(self)
        self.sides = [ Hit(), Hit(), Hit(), Hit(), HitCrit(), HitCrit(), Miss(), Miss()]

class Upgrade(object):
    def modifyDice(self, dice):
        return dice

    def modifyRoll(self, die, side):
        return side

    def modifyResult(self, result):
        return result

class FirstRoll(Upgrade):
    def modifyRoll(self, die, side):
        return die.chooseSide()    

class SW7(Upgrade):
    def modifyRoll(self, die, side):
        if isinstance(die, Blue) and side.damage() == 0:
            return Hit()
        else:
            return side

class DualTurbo(Upgrade):
    def modifyDice(self, dice):
        dice.append(Red())
        return dice

    def modifyResult(self, result):
        result.removeLowestSide()
        return result

class OrdinanceExp(Upgrade):
    def modifyRoll(self, die, side):
        if isinstance(die, Black) and side.damage() == 0:
            return die.chooseSide()
        else:
            return side

class H9(Upgrade):
    def modifyResult(self,result):
        pass

class Result(object):
    def __init__(self):
        self.sides = []

    def add(self, side):
        self.sides.append(side)

    def totalDamage(self):
        total = 0
        for side in self.sides:
            total += side.damage()

        return total

    def hasCrit(self):
        for side in self.sides:
            if side.isCrit():
                return True
        return False

    def removeLowestSide(self):
        std = sorted(self.sides, key=lambda side: side.good)
        del std[0]
        self.sides = std

    def accuracyCount(self):
        total = 0
        for side in self.sides:
            total += side.accuracy()
        return total

class Attack(object):
    def __init__(self):
        self.dice = []
        self.upgrades = [FirstRoll()]

    def generateResult(self):
        result = Result()
        dice = self.dice[:]

        for upgrade in self.upgrades:
            dice = upgrade.modifyDice(dice)

        for die in dice:
            side = None
            for upgrade in self.upgrades:
                side = upgrade.modifyRoll(die, side)
            result.add(side)

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
    attack.addDie(Red(), 2)
    attack.addDie(Blue(), 1)
    attack.addUpgrade(SW7())
    # attack.addUpgrade(DualTurbo())

    # attack.addDie(Blue(), 2)
    # attack.addDie(Black(), 3)
    # attack.addUpgrade(OrdinanceExp())

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