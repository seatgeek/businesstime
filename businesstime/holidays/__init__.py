import math
import datetime
import calendar


class Holidays(object):

    rules = []

    def month_length(self, year,month):
        return calendar.monthrange(year,month)[1]

    def _day_rule_matches(self, rule, dt):
        return dt.month == rule.get("month") and dt.day == rule.get("day")

    def _weekday_rule_matches(self, rule, dt):
        if dt.month == rule.get("month") and dt.weekday() == rule.get("weekday"):
            # Check for +week specification
            if math.floor((dt.day - 1) / 7) == rule.get("week") - 1:
                return True
            # Check for -week specification
            length = self.month_length(dt.year,dt.month)
            if math.floor((length - dt.day) / 7) + 1 == rule.get("week") * -1:
                return True
        return False

    def isholiday(self, dt):
        for r in self.rules:
            if self._day_rule_matches(r, dt) or self._weekday_rule_matches(r, dt):
                return True
        return False

    def __call__(self, curr, end=None):
        while end is None or curr < end:
            if self.isholiday(curr):
                yield curr
            curr = curr + datetime.timedelta(days=1)
