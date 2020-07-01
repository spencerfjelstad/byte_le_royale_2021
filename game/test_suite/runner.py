import unittest
import game.test_suite.tests

def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=3)

    suite.addTests(loader.loadTestsFromModule(game.test_suite.tests))

    runner.run(suite)

if __name__ == '__main__':
    main()

