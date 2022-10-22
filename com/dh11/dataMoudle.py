
import pymysql

con = pymysql.connect(
	host='localhost',
	port=3306,
	user='root',
	password='111111',
	db='sunpeng',
	charset='utf8'
)
site = "阳台" # 传感器安装位置
def recorder(co2v ,winspeed, temp, hum):
	cur=con.cursor()
	print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))

	sql="insert into sensordata(create_time,site,temperature," \
		"humidity,co2,windspeed) " \
		"value(now(),'%s','%s','%s','%s','%s')"
	cur.execute(sql %(site,temp,hum,co2v,winspeed))
	con.commit()
	cur.close()