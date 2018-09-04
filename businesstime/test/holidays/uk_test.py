from datetime import date
import unittest

from businesstime.holidays.uk import (
    EnglandHolidays, WalesHolidays, ScotlandHolidays,
    NorthernIrelandHolidays,
)


class EnglandHolidaysTest(unittest.TestCase):
    holidays = EnglandHolidays()

    def test_2012_01(self):
        self.assertEqual(
            list(self.holidays(date(2012, 1, 1), end=date(2012, 1, 31))),
            [date(2012, 1, 2)]
        )


class WalesHolidaysTest(unittest.TestCase):
    holidays = WalesHolidays()

    def test_2012_01(self):
        self.assertEqual(
            list(self.holidays(date(2012, 1, 1), end=date(2012, 1, 31))),
            [date(2012, 1, 2)]
        )


class ScotlandHolidaysTest(unittest.TestCase):
    holidays = ScotlandHolidays()

    def test_2012_01(self):
        self.assertEqual(
            list(self.holidays(date(2012, 1, 1), end=date(2012, 1, 31))),
            [date(2012, 1, 2), date(2012, 1, 3)]
        )


class NorthernIrelandHolidaysTest(unittest.TestCase):
    holidays = NorthernIrelandHolidays()

    def test_2012_01(self):
        self.assertEqual(
            list(self.holidays(date(2012, 1, 1), end=date(2012, 1, 31))),
            [date(2012, 1, 2)]
        )

    def test_2012_07(self):
        self.assertEqual(
            list(self.holidays(date(2012, 7, 1), end=date(2012, 7, 31))),
            [date(2012, 7, 12)]
        )
