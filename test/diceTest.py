
class TestRedDice(unittest.TestCase):
    def setUp(self):
        self.random = setupRandom()
        self.die = Red()

    def getAverage(self):
        return 0.75

    def testAverageDamage(self):
        self.assertEqual(self.die.averageDamage(), self.getAverage())

    def testChooseSide(self):
        self.random.choice = 0
        self.assertTrue(checkSides(self.die.chooseSide(), Hit()))

    def testChangeSideAfterRoll(self):
        self.random.choice = 0
        sideOne = self.die.chooseSide()
        sideOne.setTo(Miss())
        sideTwo = self.die.chooseSide()
        self.assertNotEqual(sideOne, sideTwo)

class TestBlueDice(TestRedDice):
    def setUp(self):
        TestRedDice.setUp(self)
        self.die = Blue()

class TestBlackDice(TestRedDice):
    def setUp(self):
        TestRedDice.setUp(self)
        self.die = Black()

    def getAverage(self):
        return 1.0
