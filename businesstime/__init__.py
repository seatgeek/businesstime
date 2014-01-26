import datetime
import math

__version__ = "0.1.1"

class BusinessTime(object):
    """
    BusinessTime is essentially a calendar that can be queried for
    business time aware timedeltas between two datetimes.
    """

    def __init__(self, business_hours=None, weekends=(5,6), holidays=None):
        if business_hours is None:
            business_hours = (datetime.time(9), datetime.time(17))
        self.business_hours = business_hours

        # TODO: weekends should maybe be a generator or a callable returning True/False
        self.weekends = weekends

        self.holidays = holidays
        if callable(self.holidays) or self.holidays is None:
            self._holidaysGeneratorStart = None
            self._holidaysGenerator = None
        else:
            self._holidays = self.holidays

        # HACK: pick an arbitrary date so we can do math with datetime.time objects
        arbitrary_date = datetime.datetime(2014, 1, 26)
        start = datetime.datetime.combine(arbitrary_date, business_hours[0])
        end = datetime.datetime.combine(arbitrary_date, business_hours[1])
        self.open_hours = end - start

    def isweekend(self, dt):
        return dt.weekday() in self.weekends

    def _ensureHolidaysSpanDatetime(self, dt):
        if callable(self.holidays):
            if self._holidaysGeneratorStart is None or dt < self._holidaysGeneratorStart:
                self._holidaysGeneratorStart = dt
                self._holidaysGenerator = self.holidays(dt)
                self._holidays = []
            while len(self._holidays) == 0 or dt > self._holidays[-1]:
                self._holidays.append(next(self._holidaysGenerator))

    def isholiday(self, dt):
        if type(dt) == datetime.datetime:
            dt = dt.date()
        self._ensureHolidaysSpanDatetime(dt)
        return dt in self._holidays

    def isbusinessday(self, dt):
        return not self.isweekend(dt) and not self.isholiday(dt)

    def isduringbusinesshours(self, dt):
        return self.isbusinessday(dt) and self.business_hours[0] <= dt.time() < self.business_hours[1]

    def iterdays(self, d1, d2):
        """
        Date iterator returning dates in d1 <= x < d2
        """
        curr = datetime.datetime.combine(d1, datetime.time())
        end = datetime.datetime.combine(d2, datetime.time())
        if d1.date() == d2.date():
            yield curr
            return
        while curr < end:
            yield curr
            curr = curr + datetime.timedelta(days=1)

    def iterweekdays(self, d1, d2):
        """
        Date iterator returning dates in d1 <= x < d2, excluding weekends
        """
        for dt in self.iterdays(d1, d2):
            if not self.isweekend(dt):
                yield dt

    def iterbusinessdays(self, d1, d2):
        """
        Date iterator returning dates in d1 <= x < d2, excluding weekends and holidays
        """
        first = True
        for dt in self.iterdays(d1, d2):
            if first and d1.time() > self.business_hours[1]:
                first = False
                continue
            first = False
            if not self.isweekend(dt) and not self.isholiday(dt):
                yield dt

    def _buildSpanningDatetimes(self, d1, d2):
        businessdays = list(self.iterbusinessdays(d1, d2))

        if len(businessdays) == 0:
            return businessdays

        businessdays = [datetime.datetime.combine(d, self.business_hours[0]) for d in businessdays]

        if d1 > businessdays[0]:
            businessdays[0] = d1

        if self.isbusinessday(d2) and d2 > datetime.datetime.combine(d2, self.business_hours[0]):
            businessdays.append(datetime.datetime.combine(d2, self.business_hours[1]))
            if d2 < businessdays[-1]:
                businessdays[-1] = datetime.datetime.combine(businessdays[-1], d2.time())
        else:
            if len(businessdays) == 1:
                businessdays.append(datetime.datetime.combine(businessdays[0], self.business_hours[1]))
            else:
                businessdays[-1] = datetime.datetime.combine(businessdays[-1], self.business_hours[1])

        return businessdays

    def businesstimedelta(self, d1, d2):
        """
        Returns a datetime.timedelta with the number of full business days
        and business time between d1 and d2
        """
        businessdays = self._buildSpanningDatetimes(d1, d2)

        time = datetime.timedelta()
        prev = None
        current = None
        count = 0
        for d in businessdays:
            if current is None:
                current = d
            current = datetime.datetime.combine(d, current.time())
            if prev is not None:
                if prev.date() != current.date():
                    time += datetime.timedelta(days=1)
                if count == len(businessdays) - 1:
                    if current > d:
                        # We went too far
                        time -= datetime.timedelta(days=1)
                        time += self.open_hours - (current - d)
                    else:
                        time += d - current
            count += 1
            prev = current

        return time


class Holidays(object):

    rules = []

    MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def isholiday(self, dt):
        for r in self.rules:
            if dt.month == r.get("month"):
                if dt.day == r.get("day"):
                    return True
                if dt.weekday() == r.get("weekday"):
                    # Check for +weekday specification
                    if math.floor((dt.day - 1) / 7) == r.get("week") - 1:
                        return True
                    # Check for -weekday specification
                    length = self.MONTH_LENGTHS[dt.month]
                    if math.floor((length - dt.day) / 7) + 1 == r.get("week") * -1:
                        return True
        return False

    def __call__(self, curr, end=None):
        while end is None or curr < end:
            if self.isholiday(curr):
                yield curr
            curr = curr + datetime.timedelta(days=1)


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
        dict(name="Chistmas Day", month=12, day=25),
    ]

