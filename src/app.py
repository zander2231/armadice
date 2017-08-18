class App(object):

    def go(self):
        attack = Attack()
        results = Results()
        n = 1000
        results.generate(n, attack)
        PrintResults(results)
