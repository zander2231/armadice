import random

class DiceRandom(object):
    instance = random

    def rollSide(self):
        return DiceRandom.instance.randint(0,7)