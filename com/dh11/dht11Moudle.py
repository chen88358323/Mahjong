# from https://www.jianshu.com/p/3297a81e5eae
import threading

import RPi.GPIO as GPIO
import dht11
import time
import datetime
import co2Moudle as co2
import dataMoudle as db
import windSpeedRs485Moudle as windspeed

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
# read data using pin 14
# pin24 bpio.bcm 8
instance = dht11.DHT11(pin=8)

try:
    while True:
        co2val = co2.mh_z19()
        print("co2:" + str(co2val))
        result = instance.read()
        speed = windspeed.read_data()

        if(speed.startswith('风速仪端口打开失败')):
            db.addAlartLog("speed sensor error，msg:"+speed, "阳台")

        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            #add alert log
            db.addAlartLog("TEMP&&HUMIDITY sensor error","阳台")


        db.recorder(co2val, speed, result.temperature, result.humidity)

        # check data is too high
        db.checkData(result.temperature,result.humidity,co2val)
        time.sleep(30)#测试30秒打印，现场环境5分钟

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
    db.close()
