import datetime

__version__ = "0.1.0"

class BusinessTime(object):
    """
    BusinessTime is essentially a calendar that can be queried for
    business time aware timedeltas between two datetimes.
    """

    def __init__(self, business_hours=None, weekends=(5,6), holidays=None):
        """
        business_hours: 2-tuple of datetime.time objects marking the start and close of business
        weekends: tuple of day indexes (Monday = 1, Sunday = 7) for what constitutes a weekend (not business day)
        holidays: tuple of dates which should not be considered business days, even if they are weekdays
        """
        # TODO: holidays should be a generator that can be lazily evaluated
        if business_hours is None:
            business_hours = (datetime.time(9), datetime.time(17))
        self.business_hours = business_hours

        # TODO: weekends should probably be a generator or a callable returning True/False
        self.weekends = weekends

        if holidays is None:
            holidays = []
        # TODO: normalize holidays into date objects
        self.holidays = holidays

        # HACK: pick an arbitrary date so we can do math with datetime.time objects
        arbitrary_date = datetime.datetime(2014, 1, 26)
        start = datetime.datetime.combine(arbitrary_date, business_hours[0])
        end = datetime.datetime.combine(arbitrary_date, business_hours[1])
        self.open_hours = end - start

    def isweekend(self, dt):
        return dt.weekday() in self.weekends

    def isholiday(self, dt):
        if type(dt) == datetime.datetime:
            dt = dt.date()
        return dt in self.holidays

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
