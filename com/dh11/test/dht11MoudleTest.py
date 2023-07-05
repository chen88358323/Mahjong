# from https://www.jianshu.com/p/3297a81e5eae
import threading

import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
#
GPIO.setmode(GPIO.BOARD)
# read data using pin 14
# pin24 bpio.bcm 8
instance = dht11.DHT11(pin=8)

try:
    while True:
        # co2val = co2.mh_z19()
        # print("co2:" + str(co2val))
        result = instance.read()
        # speed = windspeed.read_data()


        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
