businesstime
============

.. image:: https://badge.fury.io/py/businesstime.png
    :target: http://badge.fury.io/py/businesstime

.. image:: https://travis-ci.org/seatgeek/businesstime.png?branch=master
        :target: https://travis-ci.org/seatgeek/businesstime

BusinessTime is a simple utility for calculating business time aware timedeltas between two datetimes. BusinessTime's understanding of weekends, holidays and business hours can be easily configured in code.

.. code-block:: pycon

    >>> datetime(2013, 12, 26, 5) - datetime(2013, 12, 23, 12)
    datetime.timedelta(2, 61200)
    >>> bt = businesstime.BusinessTime(holidays=businesstime.holidays.usa.USFederalHolidays())
    >>> bt.businesstimedelta(datetime(2013, 12, 23, 12), datetime(2013, 12, 26, 5))
    datetime.timedelta(1, 18000)

Features
--------

- Simple, pythonic, business-time-aware datetime math
- A simple declarative format for defining holidays
- A number of useful iterators/predicate functions related to holidays/weekends/business hours
