#1
from datetime import datetime, timedelta

today = datetime.now()
days_ago = today - timedelta(days=5)

print(today)
print( days_ago)
#2
from datetime import datetime, timedelta

today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(yesterday)
print(today)
print(tomorrow)
#3
from datetime import datetime

now = datetime.now()
no_microseconds = now.replace(microsecond=0)

print(now)
print( no_microseconds)
#4
from datetime import datetime

date1 = datetime(2026, 2, 26, 10, 0, 0)
date2 = datetime(2026, 2, 28, 12, 0, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print(seconds)