from tests import test_api
import unittest

def suite_api():
    api_suite = unittest.TestSuite()
    loader_api = unittest.TestLoader()
    tests_api = loader_api.loadTestsFromModule(test_api)
    api_suite.addTests(tests_api)
    return api_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite_api())