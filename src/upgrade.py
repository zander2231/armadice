from dice import *
from result import Result

class Upgrade(object):
    def modifyResult(self, result):
        return result

def addUpgradeTo(attack, name):
    name = name.lower()
    if name == "reroll":
        attack.addUpgrade(Reroll())
    if name == "trc":
        attack.addUpgrade(TRC())
    if name == "leadingshot":
        attack.addUpgrade(LeadingShot())
    if name == "sw7":
        attack.addUpgrade(SW7())
    if name == "dualturbo":
        attack.addUpgrade(DualTurbo())
    if name == "ordinanceexp":
        attack.addUpgrade(OrdinanceExp())
    if name == "h9":
        attack.addUpgrade(H9())

class Reroll(Upgrade):
    def modifyResult(self, result):
        lowdie, lowside = result.getLowest()
        if lowside == Miss():
            lowside.setTo(lowdie.chooseSide())
        if lowside == Acc() and result.accuracyCount() > 1:
            lowside.setTo(lowdie.chooseSide())
        return result

class TRC(Upgrade):
    pass

class LeadingShot(Upgrade):
    pass

class SW7(Upgrade):
    def modifyResult(self, result):
        for side in result.getAll(Blue()):
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