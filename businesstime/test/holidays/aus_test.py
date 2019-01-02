from datetime import date
import unittest

from businesstime.holidays.aus import QueenslandPublicHolidays, BrisbanePublicHolidays


class QueenslandPublicHolidaysTest(unittest.TestCase):
    def test_2016_08(self):
        holidays_gen = QueenslandPublicHolidays()
        self.assertEqual(
            list(holidays_gen(date(2016, 8, 1), end=date(2016, 8, 31))), [])


class BrisbanePublicHolidaysTest(unittest.TestCase):
    def test_2016_08(self):
        holidays_gen = BrisbanePublicHolidays()
        self.assertEqual(
            list(holidays_gen(date(2016, 8, 1), end=date(2016, 8, 31))),
            [date(2016, 8, 10)])

    def test_out_of_range(self):
        holidays_gen = BrisbanePublicHolidays()

        def test():
            return list(holidays_gen(date(2020, 1, 1), end=date(2020, 12, 31)))

        self.assertRaises(NotImplementedError, test)
