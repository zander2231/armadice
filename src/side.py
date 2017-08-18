from utils import *

class Side(object):
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

    def setTo(self, side):
        self.hit = side.hit
        self.crit = side.crit
        self.acc = side.acc
        self.good = side.good
        self.type = side.type

    def __str__(self):
        return self.type
    def __repr__(self):
        return self.__str__()

def Miss():
    side = Side()
    side.type = "miss"
    return side

def Hit():
    side = Side()
    side.good = 2
    side.hit = 1
    side.good = 1
    side.type = "hit"
    return side

def Double():
    side = Side()
    side.good = 4
    side.hit = 2
    side.type = "double"
    return side

def Crit():
    side = Side()
    side.good = 3
    side.crit = 1
    side.type = "crit"
    return side

def Acc():
    side = Side()
    side.good = 1
    side.acc = 1
    side.type = "acc"
    return side

def HitCrit():
    side = Side()
    side.good = 5
    side.crit = 1
    side.hit = 1
    side.type = "hitcrit"
    return side
