import datetime


class BusinessTime(object):
    """
    BusinessTime is essentially a calendar that can be queried for
    business time aware timedeltas between two datetimes.
    """

    def __init__(self, business_hours=None, weekends=(5, 6), holidays=None):
        if business_hours is None:
            business_hours = (datetime.time(9), datetime.time(17))
        self.business_hours = business_hours

        # TODO: weekends should maybe be a generator or a callable returning True/False
        self.weekends = weekends

        self.holidays = holidays
        if callable(self.holidays) or self.holidays is None:
            self._holidaysGeneratorStart = None
            self._holidaysGenerator = None
            self._holidays = []
        else:
            self._holidays = self.holidays

        # HACK: pick an arbitrary date so we can do math with datetime.time objects
        arbitrary_date = datetime.datetime(2014, 1, 26)
        start = datetime.datetime.combine(arbitrary_date, business_hours[0])
        end = datetime.datetime.combine(arbitrary_date, business_hours[1])
        self.open_hours = end - start

    def isweekend(self, dt):
        return dt.weekday() in self.weekends

    def _ensure_holidays_span_datetime(self, dt):
        if callable(self.holidays):
            if self._holidaysGeneratorStart is None or dt < self._holidaysGeneratorStart:
                self._holidaysGeneratorStart = dt
                self._holidays = []
                self._holidaysGenerator = self.holidays(dt)
            while len(self._holidays) == 0 or dt > self._holidays[-1]:
                self._holidays.append(next(self._holidaysGenerator))

    def isholiday(self, dt):
        if type(dt) == datetime.datetime:
            dt = dt.date()
        self._ensure_holidays_span_datetime(dt)
        return dt in self._holidays

    def isbusinessday(self, dt):
        return not self.isweekend(dt) and not self.isholiday(dt)

    def isduringbusinesshours(self, dt):
        return self.isbusinessday(dt) and self.business_hours[0] <= dt.time(
        ) < self.business_hours[1]

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
        assert d2 >= d1
        if d1.date() == d2.date() and d2.time() < self.business_hours[0]:
            return
        first = True
        for dt in self.iterdays(d1, d2):
            if first and d1.time() > self.business_hours[1]:
                first = False
                continue
            first = False
            if not self.isweekend(dt) and not self.isholiday(dt):
                yield dt

    def _build_spanning_datetimes(self, d1, d2):
        businessdays = list(self.iterbusinessdays(d1, d2))
        if len(businessdays) == 0:
            return businessdays

        businessdays = [
            datetime.datetime.combine(d, self.business_hours[0])
            for d in businessdays
        ]

        if d1 > businessdays[0]:
            businessdays[0] = d1

        if self.isbusinessday(d2) and d2 >= datetime.datetime.combine(
                d2, self.business_hours[0]):
            businessdays.append(
                datetime.datetime.combine(d2, self.business_hours[1]))
            if d2 < businessdays[-1]:
                businessdays[-1] = datetime.datetime.combine(
                    businessdays[-1], d2.time())
        else:
            if len(businessdays) == 1:
                businessdays.append(
                    datetime.datetime.combine(businessdays[0],
                                              self.business_hours[1]))
            else:
                businessdays[-1] = datetime.datetime.combine(
                    businessdays[-1], self.business_hours[1])
        return businessdays

    def businesstimedelta(self, d1, d2):
        """
        Returns a datetime.timedelta with the number of full business days
        and business time between d1 and d2
        """

        if d1 > d2:
            d1, d2, timedelta_direction = d2, d1, -1
        else:
            timedelta_direction = 1
        businessdays = self._build_spanning_datetimes(d1, d2)
        time = datetime.timedelta()

        if len(businessdays) == 0:
            # HACK: manually handle the case when d1 is after business hours while d2 is during
            if self.isduringbusinesshours(d2):
                time += d2 - datetime.datetime.combine(d2,
                                                       self.business_hours[0])

            # HACK: manually handle the case where d1 is on an earlier non-business day and d2 is after hours on a business day
            elif not self.isbusinessday(d1) and self.isbusinessday(d2):
                if d2.time() > self.business_hours[1]:
                    time += datetime.datetime.combine(
                        d2,
                        self.business_hours[1]) - datetime.datetime.combine(
                        d2, self.business_hours[0])
                elif d2.time() > self.business_hours[0]:
                    time += d2 - datetime.datetime.combine(
                        d2, self.business_hours[0])

        else:
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

        return time * timedelta_direction

    def businesstime_hours(self, d1, d2):
        """
        Returns a datetime.timedelta of business hours between d1 and d2,
        based on the length of the businessday
        """
        open_hours = self.open_hours.seconds / 3600
        btd = self.businesstimedelta(d1, d2)
        btd_hours = btd.seconds / 3600
        return datetime.timedelta(hours=(btd.days * open_hours + btd_hours))
