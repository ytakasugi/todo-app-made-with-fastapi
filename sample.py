import imp
import locale
from datetime import datetime, timedelta
import calendar

today = datetime.now()
next_week = today + timedelta(days = 7)

print(locale.getlocale(locale.LC_TIME))
print(today.strftime('%Y/%m/%d'))
print(next_week.strftime('%Y/%m/%d'))

locale.setlocale(locale.LC_TIME, 'C.UTF-8')

print(locale.getlocale(locale.LC_TIME))
print(today.strftime('%Y/%m/%d'))
print(next_week.strftime('%Y/%m/%d'))
print(calendar.calendar(today.year))
