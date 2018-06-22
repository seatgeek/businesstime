from datetime import datetime, date, timedelta
import unittest

from businesstime import BusinessTime
from businesstime.holidays.usa import USFederalHolidays


class BusinessTimeTest(unittest.TestCase):
    def setUp(self):
        """
        Tests mostly based around January 2014, where two holidays, New Years Day
        and MLK day, fall on the 1st and 20th, respectively.

            January 2014
        Su Mo Tu We Th Fr Sa
                  1  2  3  4
         5  6  7  8  9 10 11
        12 13 14 15 16 17 18
        19 20 21 22 23 24 25
        26 27 28 29 30 31
        """
        self.bt = BusinessTime(holidays=USFederalHolidays())

    def test_iterdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)),
            (datetime(2014, 1, 16), datetime(2014, 1, 17), datetime(
                2014, 1, 18), datetime(2014, 1, 19), datetime(2014, 1, 20),
             datetime(2014, 1, 21)))

    def test_iterdays_same_day(self):
        start = datetime(2014, 1, 16, 12, 15)
        end = datetime(2014, 1, 16, 12, 16)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)), (datetime(2014, 1, 16), ))

    def test_iterdays_clears_time(self):
        start = datetime(2014, 1, 16, 12, 12, 11)
        end = datetime(2014, 1, 18, 15)
        self.assertEqual(
            tuple(self.bt.iterdays(start, end)),
            (datetime(2014, 1, 16), datetime(2014, 1, 17)))

    def test_iterweekdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterweekdays(start, end)),
            (datetime(2014, 1, 16), datetime(2014, 1, 17), datetime(
                2014, 1, 20), datetime(2014, 1, 21)))

    def test_iterbusinessdays(self):
        start = datetime(2014, 1, 16)
        end = datetime(2014, 1, 22)
        self.assertEqual(
            tuple(self.bt.iterbusinessdays(start, end)), (datetime(
                2014, 1, 16), datetime(2014, 1, 17), datetime(2014, 1, 21)))

    def test_iterbusinessdays_conforms_to_business_hours(self):
        start = datetime(2014, 1, 16, 17, 1)
        end = datetime(2014, 1, 23, 2)
        self.assertEqual(
            tuple(self.bt.iterbusinessdays(start, end)), (datetime(
                2014, 1, 17), datetime(2014, 1, 21), datetime(2014, 1, 22)))

    def test_isduringbusinessday(self):
        self.assertTrue(
            self.bt.isduringbusinesshours(datetime(2014, 1, 15, 12)))
        self.assertFalse(self.bt.isduringbusinesshours(datetime(2014, 1, 15)))
        self.assertFalse(
            self.bt.isduringbusinesshours(datetime(2014, 1, 18, 11)))
        self.assertFalse(
            self.bt.isduringbusinesshours(datetime(2014, 1, 20, 11, 46, 43)))

    def test_holidays_specified_as_list(self):
        bd = BusinessTime(holidays=[date(2014, 1, 1)])
        self.assertTrue(bd.isholiday(date(2014, 1, 1)))
        self.assertFalse(bd.isholiday(date(2014, 1, 2)))

    def test_no_holidays(self):
        bt = BusinessTime()
        self.assertFalse(bt.isholiday(date(2014, 1, 1)))

    def test_businesstimedelta_after_during(self):
        start = datetime(2014, 1, 16, 18, 30)
        end = datetime(2014, 1, 22, 10, 0)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=2, hours=1))

    def test_businesstimedelta_1_minute_after_during(self):
        """https://github.com/seatgeek/businesstime/issues/7"""
        start = datetime(2015, 2, 23, 17, 0)
        end = datetime(2015, 2, 24, 14, 20)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(hours=5, minutes=20))
        start = datetime(2015, 2, 23, 17, 1)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(hours=5, minutes=20))

    def test_businesstimedelta_nonbusiness_after(self):
        start = datetime(2014, 1, 12, 12)
        end = datetime(2014, 1, 17, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=4, hours=8))

    def test_businesstimedelta_before_after(self):
        start = datetime(2014, 1, 13, 4)
        end = datetime(2014, 1, 17, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=4, hours=8))

    def test_businesstimedelta_during_after(self):
        start = datetime(2014, 1, 30, 12, 15)
        end = datetime(2014, 1, 31, 19, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(days=1, hours=4, minutes=45))

    def test_businesstimedelta_during_before(self):
        start = datetime(2014, 8, 4, 11)
        end = datetime(2014, 8, 6, 5)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=1, hours=6))

    def test_businesstimedelta_before_before(self):
        start = datetime(2014, 8, 4, 1)
        end = datetime(2014, 8, 4, 5)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=0))

    def test_businesstimedelta_after_after(self):
        start = datetime(2014, 8, 4, 22)
        end = datetime(2014, 8, 4, 23)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=0))

    def test_businesstimedelta_during_nonbusiness(self):
        start = datetime(2014, 1, 10, 16, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(minutes=45))

    def test_businesstimedelta_during_nonbusiness2(self):
        start = datetime(2014, 1, 9, 16, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(
                days=1, minutes=45))

    def test_businesstimedelta_after_nonbusiness(self):
        start = datetime(2014, 1, 10, 17, 15)
        end = datetime(2014, 1, 12, 12, 30)
        self.assertEqual(self.bt.businesstimedelta(start, end), timedelta())

    def test_businesstimedelta_during_during(self):
        start = datetime(2014, 1, 2, 9, 12)
        end = datetime(2014, 1, 3, 9, 10)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(hours=7, minutes=58))

    def test_businesstimedelta_during_during2(self):
        start = datetime(2014, 1, 2, 9, 10)
        end = datetime(2014, 1, 3, 9, 12)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(
                days=1, minutes=2))

    def test_businesstimedelta_during_during3(self):
        start = datetime(2014, 1, 2, 9, 10)
        end = datetime(2014, 1, 2, 9, 12)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(minutes=2))

    def test_businesstimedelta_nonbusiness_nonbusiness(self):
        start = datetime(2014, 1, 4, 9, 10)
        end = datetime(2014, 1, 4, 9, 12)
        self.assertEqual(self.bt.businesstimedelta(start, end), timedelta())

    def test_businesstimedelta_exactly_one_day(self):
        start = datetime(2014, 1, 7, 10)
        end = datetime(2014, 1, 8, 10)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=1))

    def test_businesstimedelta_exactly_one_day2(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/3
        """
        start = datetime(2014, 1, 7, 9)
        end = datetime(2014, 1, 8, 9)
        self.assertEqual(
            self.bt.businesstimedelta(start, end), timedelta(days=1))

    def test_businesstimedelta_during_during_reverse(self):
        end = datetime(2014, 1, 2, 9, 12)
        start = datetime(2014, 1, 3, 9, 10)
        self.assertEqual(
            self.bt.businesstimedelta(start, end),
            timedelta(hours=-7, minutes=-58))

    def test_businesstime_hours_exactly_one_day(self):
        start = datetime(2014, 1, 16, 9, 0)
        end = datetime(2014, 1, 17, 9, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=8))

    def test_businesstime_hours_one_day(self):
        start = datetime(2014, 1, 16, 9, 0)
        end = datetime(2014, 1, 17, 15, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=14))

    def test_businesstime_hours_one_day_reverse(self):
        start = datetime(2014, 1, 17, 9, 0)
        end = datetime(2014, 1, 16, 9, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=-8))

    def test_businesstime_out_of_hours_start(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/13
        """
        start = datetime(2014, 8, 9, 9, 0)
        end = datetime(2014, 8, 11, 17, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=8))

    def test_businesstime_out_of_hours_start_end(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/13
        """
        start = datetime(2014, 8, 9, 9, 0)
        end = datetime(2014, 8, 11, 23, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=8))

    def test_businesstime_out_of_hours_end(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/13
        """
        start = datetime(2014, 8, 8, 9, 0)
        end = datetime(2014, 8, 11, 23, 0)
        self.assertEqual(
            self.bt.businesstime_hours(start, end), timedelta(hours=16))

    def test_businesstime_holidays(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/25
        """
        bt_cal = BusinessTime(holidays=USFederalHolidays())

        non_holiday = datetime(2018, 5, 31, 12, 0)
        memorial_day = datetime(2018, 5, 28, 12, 0)

        is_non_holiday_holiday = bt_cal.isholiday(non_holiday)
        is_memorial_day_holiday = bt_cal.isholiday(memorial_day)

        self.assertFalse(is_non_holiday_holiday)
        self.assertTrue(is_memorial_day_holiday)

    def test_businesstime_holidays_2(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/25
        """
        bt_cal = BusinessTime(holidays=USFederalHolidays())

        non_holiday = datetime(2018, 5, 31, 12, 0)
        memorial_day = datetime(2018, 5, 28, 12, 0)

        # Note that we have flipped the order from the above test
        # to check if memorial day is a holiday before checking if
        # the other (non-holiday) is a holiday.
        # Results should be the same regardless of order of calling isholiday
        is_memorial_day_holiday = bt_cal.isholiday(memorial_day)
        is_non_holiday_holiday = bt_cal.isholiday(non_holiday)

        self.assertTrue(is_memorial_day_holiday)
        self.assertFalse(is_non_holiday_holiday)

    def test_lots_of_holidays(self):
        """
        Test for https://github.com/seatgeek/businesstime/issues/25
        """
        bt_cal = BusinessTime(holidays=USFederalHolidays())

        non_holiday = datetime(2018, 5, 31, 12, 0)
        non_holiday2 = datetime(2018, 2, 3, 12, 0)
        non_holiday3 = datetime(2018, 6, 4, 12, 0)
        non_holiday4 = datetime(2018, 11, 21, 12, 0)

        memorial_day = datetime(2018, 5, 28, 12, 0)
        new_year_day = datetime(2018, 1, 1, 12, 0)
        labor_day = datetime(2018, 9, 3, 12, 0)
        christmas = datetime(2018, 12, 25, 12, 0)

        self.assertFalse(bt_cal.isholiday(non_holiday))
        self.assertTrue(bt_cal.isholiday(memorial_day))
        self.assertTrue(bt_cal.isholiday(new_year_day))
        self.assertFalse(bt_cal.isholiday(non_holiday2))
        self.assertFalse(bt_cal.isholiday(non_holiday4))
        self.assertTrue(bt_cal.isholiday(labor_day))
        self.assertFalse(bt_cal.isholiday(non_holiday3))
        self.assertTrue(bt_cal.isholiday(christmas))

