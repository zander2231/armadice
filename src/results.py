from attacks import *

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