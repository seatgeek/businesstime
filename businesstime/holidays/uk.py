import datetime
import json
import os

from businesstime.holidays import Holidays


__all__ = (
    'EnglandHolidays', 'WalesHolidays', 'ScotlandHolidays',
    'NorthernIrelandHolidays',
)


PWD = os.path.dirname(os.path.realpath(__file__))
DEFAULT_HOLIDAYS_FILEPATH = os.path.join(PWD, 'data', 'uk-bank-holidays.json')


class UKHolidays(Holidays):
    """
    List from https://www.gov.uk/bank-holidays.json

    e.g. curl https://www.gov.uk/bank-holidays.json -o uk-bank-holidays.json
    """
    DIVISION_CHOICES = ('england-and-wales', 'scotland', 'northern-ireland', )
    division = None

    def __init__(self, *args, **kwargs):
        if self.division not in self.DIVISION_CHOICES:
            raise ValueError(
                "'division' class attribute must be one of {}. You picked: {}"
                .format(self.DIVISION_CHOICES, self.division)
            )
        self.holidays = kwargs.pop('holidays', None)
        holidays_filepath = kwargs.pop('holidays_filepath',
                                       DEFAULT_HOLIDAYS_FILEPATH)
        if self.holidays is None:
            self.holidays = self._get_holidays_from_filepath(holidays_filepath)
        super(UKHolidays, self).__init__(*args, **kwargs)

    @classmethod
    def _get_holidays_from_filepath(cls, filepath):
        with open(filepath) as f:
            return cls._parse_holidays_file(f)

    @classmethod
    def _parse_holidays_file(cls, holidays_file):
        _holidays = json.load(holidays_file)
        return [
            datetime.datetime.strptime(event['date'], "%Y-%m-%d").date()
            for event in _holidays[cls.division]['events']
        ]

    def isholiday(self, dt):
        if isinstance(dt, datetime.datetime):
            return dt.date() in self.holidays
        return dt in self.holidays


class EnglandHolidays(UKHolidays):
    division = 'england-and-wales'


class WalesHolidays(UKHolidays):
    division = 'england-and-wales'


class ScotlandHolidays(UKHolidays):
    division = 'scotland'


class NorthernIrelandHolidays(UKHolidays):
    division = 'northern-ireland'
