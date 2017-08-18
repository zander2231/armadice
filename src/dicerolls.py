from upgrade import *
from attacks import *
from results import *

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
    attack.addUpgrade(H9())

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