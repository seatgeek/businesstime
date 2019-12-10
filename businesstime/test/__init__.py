import unittest

from varyinghoursbusinesstimetest import VaryingHoursBusinessTimeTest
from businesstimetest import BusinessTimeTest

if __name__ == '__main__':
    # unittest.main()
    test_classes_to_run = [BusinessTimeTest, VaryingHoursBusinessTimeTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
