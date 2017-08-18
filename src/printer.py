
def PrintResults(results):
    percentCrit = results.percentCrit()
    percentAcc = results.percentAcc()

    print "Dam results crit  acc"
    for damage, count in results.damages.items():
        percentHit = count/n
        print "{!s:2}:     {:3.0%} {:4.0%} {:4.0%}  ".format(damage, percentHit, percentCrit[damage], percentAcc[damage]) + "X"*int(percentHit*100)
