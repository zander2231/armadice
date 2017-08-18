from upgrade import *
from attacks import *
from results import *
from printer import PrintResults

class App(object):
    def go(self):
        attack = Attack()
        attack.addDie(Red(), 2)
        # attack.addUpgrade(Reroll())

        results = Results()
        n = 1000
        results.generate(n, attack)
        PrintResults(n, results)
