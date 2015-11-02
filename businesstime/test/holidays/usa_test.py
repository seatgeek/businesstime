from datetime import datetime, date, timedelta
import unittest

from businesstime.holidays.usa import USFederalHolidays


class USFederalHolidaysTest(unittest.TestCase):

    def test_2013(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2013, 1, 1), end=date(2013, 12, 31))),
            [
                date(2013, 1, 1),
                date(2013, 1, 21),
                date(2013, 2, 18),
                date(2013, 5, 27),
                date(2013, 7, 4),
                date(2013, 9, 2),
                date(2013, 10, 14),
                date(2013, 11, 11),
                date(2013, 11, 28),
                date(2013, 12, 25)
            ]
        )

    def test_2014(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2014, 1, 1), end=date(2014, 12, 31))),
            [
                date(2014, 1, 1),
                date(2014, 1, 20),
                date(2014, 2, 17),
                date(2014, 5, 26),
                date(2014, 7, 4),
                date(2014, 9, 1),
                date(2014, 10, 13),
                date(2014, 11, 11),
                date(2014, 11, 27),
                date(2014, 12, 25)
            ]
        )

    def test_2015(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2015, 1, 1), end=date(2015, 12, 31))),
            [
                date(2015, 1, 1),
                date(2015, 1, 19),
                date(2015, 2, 16),
                date(2015, 5, 25),
                date(2015, 7, 3),
                date(2015, 7, 4),
                date(2015, 9, 7),
                date(2015, 10, 12),
                date(2015, 11, 11),
                date(2015, 11, 26),
                date(2015, 12, 25)
            ]
        )

    def test_2016(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2016, 1, 1), end=date(2016, 12, 31))),
            [
                date(2016, 1, 1),
                date(2016, 1, 18),
                date(2016, 2, 15),
                date(2016, 5, 30),
                date(2016, 7, 4),
                date(2016, 9, 5),
                date(2016, 10, 10),
                date(2016, 11, 11),
                date(2016, 11, 24),
                date(2016, 12, 25),
                date(2016, 12, 26)
            ]
        )

    def test_2017(self):
        holidays_gen = USFederalHolidays()
        self.assertEqual(
            list(holidays_gen(date(2017, 1, 1), end=date(2017, 12, 31))),
            [
                date(2017, 1, 1),
                date(2017, 1, 2),
                date(2017, 1, 16),
                date(2017, 2, 20),
                date(2017, 5, 29),
                date(2017, 7, 4),
                date(2017, 9, 4),
                date(2017, 10, 9),
                date(2017, 11, 10),
                date(2017, 11, 11),
                date(2017, 11, 23),
                date(2017, 12, 25)
            ]
        )
