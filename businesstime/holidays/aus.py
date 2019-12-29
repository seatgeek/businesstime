from datetime import date
from businesstime.holidays import Holidays


class QueenslandPublicHolidays(Holidays):
    """
    http://www.qld.gov.au/recreation/travel/holidays/public/

    Current coverage is only 2013-2021.
    """

    # Australian public holidays are legislated by each state individually for
    # each year individually. They are so messed up that trying to write
    # general rules to apply across all years is too hard.

    _coverage_start_year = 2013
    _coverage_end_year = 2021

    holidays = [
        # New Year's Day
        date(2013, 1, 1),
        date(2014, 1, 1),
        date(2015, 1, 1),
        date(2016, 1, 1),
        date(2017, 1, 1),
        date(2017, 1, 2),  # extra because 1 Jan is a Sunday
        date(2018, 1, 1),
        date(2019, 1, 1),
        date(2020, 1, 1),
        date(2021, 1, 1),

        # Australia Day
        date(2013, 1, 28),
        date(2014, 1, 27),
        date(2015, 1, 26),
        date(2016, 1, 26),
        date(2017, 1, 26),
        date(2018, 1, 26),
        date(2019, 1, 28), # shifted because 26 Jan is a Saturday
        date(2020, 1, 27), # shifted because 26 Jan is a Sunday
        date(2021, 1, 26),

        # Good Friday
        date(2013, 3, 29),
        date(2014, 4, 18),
        date(2015, 4, 3),
        date(2016, 3, 25),
        date(2017, 4, 14),
        date(2018, 4, 30),
        date(2019, 4, 19),
        date(2020, 4, 10),
        date(2021, 4, 2),

        # Easter Saturday, now called "the day after Good Friday"
        date(2013, 3, 30),
        date(2014, 4, 19),
        date(2015, 4, 4),
        date(2016, 3, 26),
        date(2017, 4, 15),
        date(2018, 3, 31),
        date(2019, 4, 20),
        date(2020, 4, 11),
        date(2021, 4, 3),

        # Easter Sunday (added 2017)
        date(2017, 4, 16),
        date(2018, 4, 1),
        date(2019, 4, 21),
        date(2020, 4, 12),
        date(2021, 4, 4),

        # Easter Monday
        date(2013, 4, 1),
        date(2014, 4, 21),
        date(2015, 4, 6),
        date(2016, 3, 28),
        date(2017, 4, 14),
        date(2018, 4, 2),
        date(2019, 4, 22),
        date(2020, 4, 13),
        date(2021, 4, 5),

        # ANZAC Day
        date(2013, 4, 25),
        date(2014, 4, 25),
        date(2015, 4, 25),
        date(2016, 4, 25),
        date(2017, 4, 25),
        date(2018, 4, 25),
        date(2019, 4, 25),
        date(2020, 4, 25),
        date(2021, 4, 26), # shifted because 25 Apr is a Sunday

        # Labour Day
        date(2013, 10, 7),
        date(2014, 10, 6),
        date(2015, 10, 5),
        date(2016, 5, 2),
        date(2017, 5, 1),
        date(2018, 5, 7),
        date(2019, 5, 6),
        date(2020, 5, 4),
        date(2021, 5, 3),

        # Queen's Birthday
        date(2013, 6, 10),
        date(2014, 6, 9),
        date(2015, 6, 8),
        date(2016, 10, 3),
        date(2017, 10, 2),
        date(2018, 10, 1),
        date(2019, 10, 7),
        date(2020, 10, 5),
        date(2021, 10, 4),

        # Christmas Day
        date(2013, 12, 25),
        date(2014, 12, 25),
        date(2015, 12, 25),
        date(2016, 12, 25),
        date(2016, 12, 27),  # extra because 25 Dec is a Sunday
        date(2017, 12, 25),
        date(2018, 12, 25),
        date(2019, 12, 25),
        date(2020, 12, 25),
        date(2021, 12, 25),
        date(2021, 12, 27),  # extra because 25 Dec is a Saturday

        # Boxing Day
        date(2013, 12, 26),
        date(2014, 12, 26),
        date(2015, 12, 26),
        date(2015, 12, 28),  # extra because 26 Dec is a Sunday
        date(2016, 12, 26),
        date(2017, 12, 26),
        date(2018, 12, 26),
        date(2019, 12, 26),
        date(2020, 12, 26),
        date(2020, 12, 28),  # extra because 26 Dec is a Saturday
        date(2021, 12, 26),
        date(2021, 12, 28),  # extra because 26 Dec is a Sunday
    ]

    def isholiday(self, dt):
        if dt.year < self._coverage_start_year or dt.year > self._coverage_end_year:
            raise NotImplementedError(
                'QueenslandPublicHolidays only covers the years %s to %s' %
                (self._coverage_start_year, self._coverage_end_year))
        return any(holiday == dt for holiday in self.holidays)


class BrisbanePublicHolidays(QueenslandPublicHolidays):

    holidays = QueenslandPublicHolidays.holidays + [
        # Royal Queensland Show Day
        date(2013, 8, 14),
        date(2014, 8, 13),
        date(2015, 8, 12),
        date(2016, 8, 10),
        date(2017, 8, 16),
        date(2018, 8, 15),
        date(2019, 8, 14),
        date(2020, 8, 12),
        date(2021, 8, 11),

        # G20 (2014 only)
        date(2014, 11, 14),
    ]
