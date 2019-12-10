from .businesstime import BusinessTime
import datetime


class VaryingHoursBusinessTime(BusinessTime):
    def __init__(self, business_hours=None, weekends=(5, 6), holidays=None):
        super(VaryingHoursBusinessTime, self).__init__(business_hours=None, weekends=weekends, holidays=holidays)

        if business_hours is None:
            business_hours = [(datetime.time(9), datetime.time(17)) for _ in range(7)]

        self.business_hours = business_hours

        # HACK: pick an arbitrary date so we can do math with datetime.time objects
        arbitrary_date = datetime.datetime(2014, 1, 26)
        self.open_hours = None

        assert len(self.business_hours) == 7, \
            "business_hours should be a List with length 7 of type (datetime.time(), datetime.time())"

        self.open_hours = []
        for day in business_hours:
            start = datetime.datetime.combine(arbitrary_date, day[0])
            end = datetime.datetime.combine(arbitrary_date, day[1])
            self.open_hours.append(end - start)

    def isduringbusinesshours(self, dt):
        dt_business_hours = self.business_hours[dt.weekday()]
        result = self.isbusinessday(dt) and dt_business_hours[0] <= dt.time() < dt_business_hours[1]
        return result

    def iterbusinessdays(self, d1, d2):
        """
        Date iterator returning dates in d1 <= x < d2, excluding weekends and holidays
        """
        assert d2 >= d1
        d1_business_hours = self.business_hours[d1.weekday()]
        d2_business_hours = self.business_hours[d2.weekday()]

        if d1.date() == d2.date() and d2.time() < d2_business_hours[0]:
            return
        first = True
        for dt in self.iterdays(d1, d2):
            if first and d1.time() > d1_business_hours[1]:
                first = False
                continue
            first = False
            if not self.isweekend(dt) and not self.isholiday(dt):
                yield dt

    def _build_spanning_datetimes(self, d1, d2):
        businessdays = list(self.iterbusinessdays(d1, d2))

        if len(businessdays) == 0:
            return businessdays

        # d1_business_hours = self.business_hours[d1.weekday()]
        d2_business_hours = self.business_hours[d2.weekday()]

        businessdays = [
            datetime.datetime.combine(d, self.business_hours[d.weekday()][0])
            for d in businessdays
        ]

        #  Check if d1 starts later than the start of the first business day.
        if d1 > businessdays[0]:
            businessdays[0] = d1

        if self.isbusinessday(d2) and d2 >= datetime.datetime.combine(
                d2, d2_business_hours[0]):
            businessdays.append(
                datetime.datetime.combine(d2, d2_business_hours[1]))
            if d2 < businessdays[-1]:
                businessdays[-1] = datetime.datetime.combine(
                    businessdays[-1], d2.time())
        else:
            if len(businessdays) == 1:
                businessdays.append(
                    datetime.datetime.combine(businessdays[0],
                                              self.business_hours[businessdays[0].weekday()][1]))
            else:
                businessdays[-1] = datetime.datetime.combine(
                    businessdays[-1], self.business_hours[businessdays[-1].weekday()][1])

        return businessdays

    def businesstimedelta(self, d1, d2):
        """
        Returns a datetime.timedelta with the number of business time between d1 and d2.
        The concept of full business days no longer makes sense when days have varying hours.
        """
        if d1 > d2:
            d1, d2, timedelta_direction = d2, d1, -1
        else:
            timedelta_direction = 1

        # d1_business_hours = self.business_hours[d1.weekday()]
        d2_business_hours = self.business_hours[d2.weekday()]

        businessdays = self._build_spanning_datetimes(d1, d2)
        time = datetime.timedelta()

        if len(businessdays) == 0:
            # HACK: manually handle the case when d1 is after business hours while d2 is during
            if self.isduringbusinesshours(d2):
                time += d2 - datetime.datetime.combine(d2,
                                                       d2_business_hours[0])

            # HACK: manually handle the case where d1 is on an earlier non-business day and d2 is after hours on a business day
            elif not self.isbusinessday(d1) and self.isbusinessday(d2):
                if d2.time() > d2_business_hours[1]:
                    time += datetime.datetime.combine(
                        d2,
                        d2_business_hours[1]) - datetime.datetime.combine(
                        d2, d2_business_hours[0])
                elif d2.time() > d2_business_hours[0]:
                    time += d2 - datetime.datetime.combine(
                        d2, d2_business_hours[0])

        else:
            for count, d in enumerate(businessdays):
                open_dt = datetime.datetime.combine(d, self.business_hours[d.weekday()][0])
                close_dt = datetime.datetime.combine(d, self.business_hours[d.weekday()][1])

                # HACK: Handle starting and ending in the same day
                if len(businessdays) == 2 and businessdays[0].date() == businessdays[1].date():
                    if open_dt <= d <= close_dt:
                        time += businessdays[1] - businessdays[0]
                        break

                if count == 0:
                    if open_dt <= d <= close_dt:
                        time += close_dt - d
                    elif d > close_dt:
                        time += close_dt - open_dt

                elif count == len(businessdays) - 1:
                    if open_dt <= d <= close_dt:
                        time += d - open_dt
                    elif d > close_dt:
                        time += close_dt - open_dt
                else:
                    time += close_dt - open_dt

        return time * timedelta_direction

    def businesstime_hours(self, d1, d2):
        """
        Returns a datetime.timedelta of business hours between d1 and d2,
        based on the length of the businessday
        """

        btd = self.businesstimedelta(d1, d2)
        return btd