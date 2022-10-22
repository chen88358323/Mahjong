#from https://www.jianshu.com/p/3297a81e5eae
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import co2Moudle as co2
# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
# read data using pin 14
instance = dht11.DHT11(pin=24)

try:
	while True:
		co2val = co2.mh_z19()
		print("co2:" + str(co2val))
	    result = instance.read()
	    if result.is_valid():
	        print("Last valid input: " + str(datetime.datetime.now()))
	        print("Temperature: %-3.1f C" % result.temperature)
	        print("Humidity: %-3.1f %%" % result.humidity)
	    time.sleep(6)
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()