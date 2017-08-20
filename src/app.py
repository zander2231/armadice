from upgrade import *
from attacks import *
from results import *
from printer import PrintResults
import argparse

class App(object):
    def go(self):
        attack = Attack()

        parser = argparse.ArgumentParser(description='Roll a bunch of Star Wars Armada dice')
        parser.add_argument('--red', type=int,default=0, help='number of red dice')
        parser.add_argument('--blue', type=int,default=0, help='number of blue dice')
        parser.add_argument('--black', type=int,default=0, help='number of black dice')
        parser.add_argument('--upgrades', type=str, nargs="*", default=[], help='the upgrades to use for this attack')
        args = parser.parse_args()  

        attack.addDie(Red(), args.red)
        attack.addDie(Blue(), args.blue)
        attack.addDie(Black(), args.black)

        for upgrade in args.upgrades:
            addUpgradeTo(attack, upgrade)

        results = Results()
        n = 1000
        results.generate(n, attack)
        PrintResults(n, results)
