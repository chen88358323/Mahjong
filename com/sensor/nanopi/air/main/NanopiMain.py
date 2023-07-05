
import time
import datetime
import NanopiDBMoudle as  dbMoudle
import NanopiTEMPMoudle as temperMoudle
import NanopiCo2Moudle as co2Moudle
site = "阳台" # 传感器安装位置

# m分钟采集一次. 最大频率为6分钟一次
def record_by_minute(m):
    # sensor = Adafruit_DHT.DHT22
    # pin = 4 #GPIO4

    # con = pymysql.connect(
    #     host='localhost',
    #     port = 3306,
    #     user = 'root',
    #     password = '111111',
    #     db = 'sunpeng',
    #     charset = 'utf8'
    # )
    humidity, temperature = temperMoudle.main()
    co2val=co2Moudle.mh_z19()
    print("Temperature: %-3.1f C" % temperature)
    print("Humidity: %-3.1f %%" % humidity)
    if humidity is not None and temperature is not None and co2val is not None:
        dbMoudle.recorder(co2val,'-1',temperature,humidity)
        # time.sleep(60)
    else:
        print('Failed to get data from Adafruit_DHT22!')
        time.sleep(1)

#异常关闭，目前只有 GPIO 以及db连接需要
def destroy():
    temperMoudle.destroy()
    dbMoudle.destroy()


if __name__ == '__main__':
    try:
        while True:
            record_by_minute(5)
    except KeyboardInterrupt:
        destroy()
    except:
        destroy()


