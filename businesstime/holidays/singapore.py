from datetime import date
from businesstime.holidays import Holidays


class SingaporePublicHolidays(Holidays):
    """    
    http://www.mom.gov.sg/newsroom/press-releases/2018/0404-public-holidays-for-2019

    Current coverage is only 2013-2019.
    """

    # Singapore public holidays 

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

        # Chinese New Year
        date(2013, 2, 10),
        date(2013, 2, 11),
        date(2013, 2, 12), # extra because 11 Feb is a Sunday
        date(2014, 1, 31),
        date(2014, 2, 1),
        date(2015, 2, 19),
        date(2015, 2, 20),
        date(2016, 2, 8),
        date(2016, 2, 9),
        date(2017, 1, 28),
        date(2017, 1, 29),
        date(2017, 1, 30),  # extra because 29 Jan is a Sunday
        date(2018, 2, 16),
        date(2018, 2, 17),
        date(2019, 2, 5),
        date(2019, 2, 6),

        # Good Friday
        date(2013, 3, 29),
        date(2014, 4, 18),
        date(2015, 4, 3),
        date(2016, 3, 25),
        date(2017, 4, 14),
        date(2018, 3, 30),
        date(2019, 4, 19),

        # Labour Day
        date(2013, 5, 1),
        date(2014, 5, 1),
        date(2015, 5, 1),
        date(2016, 5, 1), # extra because 1 May is a Sunday
        date(2016, 5, 2),
        date(2017, 5, 1),
        date(2018, 5, 7),
        date(2019, 5, 1),

        # Vesak Day holiday
        date(2013, 5, 24),
        date(2014, 5, 13),
        date(2015, 6, 1),
        date(2016, 5, 21),
        date(2017, 5, 10),
        date(2018, 5, 29),
        date(2019, 5, 19),
        date(2019, 5, 20), # extra because 19 May is a Sunday

        # Hari Raya Puasa holiday
        date(2013, 8, 8),
        date(2014, 7, 28),
        date(2015, 7, 17),
        date(2016, 7, 6),
        date(2017, 6, 25),
        date(2017, 6, 26), # extra because 25 June is a Sunday
        date(2018, 6, 15),
        date(2019, 6, 5),

        # National Day holiday
        date(2013, 8, 9),
        date(2014, 8, 9),
        date(2015, 8, 9),
        date(2015, 8, 10), # extra because 9 August is a Sunday
        date(2016, 8, 9),
        date(2017, 8, 9),
        date(2018, 8, 9),
        date(2019, 8, 9),

        # Hari Raya Haji holiday
        date(2013, 10, 15),
        date(2014, 10, 5),
        date(2014, 10, 6), # extra because 5 October is a Sunday
        date(2015, 9, 24),
        date(2016, 9, 12),
        date(2017, 9, 1),
        date(2018, 8, 22),
        date(2019, 8, 11),
        date(2019, 8, 12), # extra because 11 August is a Sunday

        # Deepavali holiday
        date(2013, 11, 3),
        date(2013, 11, 4), # extra because 3 Nov is a Sunday
        date(2014, 10, 23),
        date(2015, 11, 10),
        date(2016, 10, 29),
        date(2017, 10, 18),
        date(2018, 11, 6),
        date(2019, 10, 27),
        date(2019, 10, 28), # extra because 27 Oct is a Sunday

        # Christmas Day
        date(2013, 12, 25),
        date(2014, 12, 25),
        date(2015, 12, 25),
        date(2016, 12, 25),
        date(2016, 12, 27),  # extra because 25 Dec is a Sunday
        date(2017, 12, 25),
        date(2018, 12, 25),
        date(2019, 12, 25),
    ]

    def isholiday(self, dt):
        if dt.year < self._coverage_start_year or dt.year > self._coverage_end_year:
            raise NotImplementedError(
                'SingaporePublicHolidays only covers the years %s to %s' %
                (self._coverage_start_year, self._coverage_end_year))
        return any(holiday == dt for holiday in self.holidays)