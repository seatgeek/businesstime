import datetime
from businesstime.holidays import Holidays


class USFederalHolidays(Holidays):
    """
    List from http://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/federal-holidays/
    """

    rules = [
        dict(name="New Year's Day", month=1, day=1),
        dict(name="Birthday of Martin Luther King, Jr.", month=1, weekday=0, week=3),
        dict(name="Washington's Birthday", month=2, weekday=0, week=3),
        dict(name="Memorial Day", month=5, weekday=0, week=-1),
        dict(name="Independence Day", month=7, day=4),
        dict(name="Labor Day", month=9, weekday=0, week=1),
        dict(name="Columbus Day", month=10, weekday=0, week=2),
        dict(name="Veterans Day", month=11, day=11),
        dict(name="Thanksgiving Day", month=11, weekday=3, week=4),
        dict(name="Christmas Day", month=12, day=25),
    ]

    def _day_rule_matches(self, rule, dt):
        """
        Day-of-month-specific US federal holidays that fall on Sat or Sun are
        observed on Fri or Mon respectively. Note that this method considers
        both the actual holiday and the day of observance to be holidays.
        """
        if dt.weekday() == 4:
            sat = dt + datetime.timedelta(days=1)
            if super(USFederalHolidays, self)._day_rule_matches(rule, sat):
                return True
        elif dt.weekday() == 0:
            sun = dt - datetime.timedelta(days=1)
            if super(USFederalHolidays, self)._day_rule_matches(rule, sun):
                return True
        return super(USFederalHolidays, self)._day_rule_matches(rule, dt)
