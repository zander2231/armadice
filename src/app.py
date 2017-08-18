from upgrade import *
from attacks import *
from results import *
from printer import PrintResults

class App(object):
    def go(self):
        attack = Attack()
        results = Results()
        n = 1000
        results.generate(n, attack)
        PrintResults(results)
