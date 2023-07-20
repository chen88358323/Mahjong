import time
from datetime import datetime
def test():
    millis = int(round(time.time() * 1000))
    print(millis)


    print("Current date:", datetime.utcnow())
    date = datetime.utcnow() - datetime(1970, 1, 1)
    print("Number of days since epoch:", date)
    seconds = (date.total_seconds())
    milliseconds = round(seconds * 1000)
    print("Milliseconds since epoch:", milliseconds)



def convert2millsec(str):
    ts = int(time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S")))
    print(ts)
if __name__ == '__main__':
    convert2millsec('2023-07-11 00:10:30')
    convert2millsec('2023-07-11 03:10:30')
    test()