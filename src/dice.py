from side import *

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
