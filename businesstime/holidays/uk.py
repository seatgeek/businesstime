from datetime import date
from businesstime.holidays import Holidays


class UKPublicHolidays(Holidays):
    """
    https://www.gov.uk/bank-holidays

    Current coverage is only 2013-2019.
    """

    # United Kingdom public holidays 

    _coverage_start_year = 2013
    _coverage_end_year = 2019

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

        # Good Friday
        date(2013, 3, 29),
        date(2014, 4, 18),
        date(2015, 4, 3),
        date(2016, 3, 25),
        date(2017, 4, 14),
        date(2018, 3, 30),
        date(2019, 4, 19),

        # Easter Monday
        date(2013, 4, 1),
        date(2014, 4, 21),
        date(2015, 4, 6),
        date(2016, 3, 28),
        date(2017, 4, 14),
        date(2018, 4, 2),
        date(2019, 4, 22),

        # Early May bank holiday
        date(2013, 5, 6),
        date(2014, 5, 5),
        date(2015, 5, 4),
        date(2016, 5, 2),
        date(2017, 5, 1),
        date(2018, 5, 7),
        date(2019, 5, 6),

        # Spring bank holiday
        date(2013, 5, 27),
        date(2014, 5, 26),
        date(2015, 5, 25),
        date(2016, 5, 30),
        date(2017, 5, 29),
        date(2018, 5, 28),
        date(2019, 5, 27),

        # Summer bank holiday
        date(2013, 8, 26),
        date(2014, 8, 21),
        date(2015, 8, 31),
        date(2016, 8, 29),
        date(2017, 8, 28),
        date(2018, 8, 27),
        date(2019, 8, 26),

        # Christmas Day
        date(2013, 12, 25),
        date(2014, 12, 25),
        date(2015, 12, 25),
        date(2016, 12, 25),
        date(2016, 12, 27),  # extra because 25 Dec is a Sunday
        date(2017, 12, 25),
        date(2018, 12, 25),
        date(2019, 12, 25),

        # Boxing Day
        date(2013, 12, 26),
        date(2014, 12, 26),
        date(2015, 12, 26),
        date(2015, 12, 28),  # extra because 26 Dec is a Sunday
        date(2016, 12, 26),
        date(2017, 12, 26),
        date(2018, 12, 26),
        date(2019, 12, 26),
    ]

    def isholiday(self, dt):
        if dt.year < self._coverage_start_year or dt.year > self._coverage_end_year:
            raise NotImplementedError(
                'UKPublicHolidays only covers the years %s to %s' %
                (self._coverage_start_year, self._coverage_end_year))
        return any(holiday == dt for holiday in self.holidays)