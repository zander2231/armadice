import unittest
from src.side import *

class TestSides(unittest.TestCase):
    def testHit(self):
        self.assertEqual(Hit().damage(), 1)
        self.assertEqual(Hit().isCrit(), False)
        self.assertEqual(Hit().accuracy(), 0)

    def testCrit(self):
        self.assertEqual(Crit().damage(), 1)
        self.assertEqual(Crit().accuracy(), 0)
        self.assertEqual(Crit().isCrit(), True)

    def testAcc(self):
        self.assertEqual(Acc().damage(), 0)
        self.assertEqual(Acc().accuracy(), 1)
        self.assertEqual(Acc().isCrit(), False)

    def testDouble(self):
        self.assertEqual(Double().damage(), 2)
        self.assertEqual(Double().accuracy(), 0)
        self.assertEqual(Double().isCrit(), False)

    def testHitCri(self):
        self.assertEqual(HitCrit().damage(), 2)
        self.assertEqual(HitCrit().isCrit(), True)
        self.assertEqual(HitCrit().accuracy(), 0)
