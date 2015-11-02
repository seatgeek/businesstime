from datetime import datetime, date, timedelta
import unittest

from businesstime.holidays.aus import QueenslandPublicHolidays, BrisbanePublicHolidays


class QueenslandPublicHolidaysTest(unittest.TestCase):

    def test_2016_08(self):
        holidays_gen = QueenslandPublicHolidays()
        self.assertEqual(
            list(holidays_gen(date(2016, 8, 1), end=date(2016, 9, 1))),
            []
        )


class BrisbanePublicHolidaysTest(unittest.TestCase):

    def test_2016_08(self):
        holidays_gen = BrisbanePublicHolidays()
        self.assertEqual(
            list(holidays_gen(date(2016, 8, 1), end=date(2016, 9, 1))),
            [
                date(2016, 8, 10)
            ]
        )
