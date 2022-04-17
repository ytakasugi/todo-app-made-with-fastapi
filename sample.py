import locale

print(locale.getlocale(locale.LC_TIME))

locale.setlocale(locale.LC_TIME, 'C.UTF-8')

print(locale.getlocale(locale.LC_TIME))