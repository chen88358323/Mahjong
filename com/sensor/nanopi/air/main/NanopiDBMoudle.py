# -*- coding: utf-8 -*-
import pymysql

con = pymysql.connect(
	host='127.0.0.1',
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

def queryByTime(starttime, endtime,site):
	cur=con.cursor()
	if (starttime is not None and endtime is not None):
		sql="select * from  sensordata  where site='%s' and createtime between ('%s','%s')"
		cur.execute(sql % (site, starttime, endtime))
	else:#默认获取近一个月的数据
		sql = "select * from  sensordata  where site='%s' and DATE_SUB(CURDATE(), INTERVAL 1 MONTH) <= date(now())"
		cur.execute(sql % (site, starttime))
	con.commit()
	cur.close()

# 增加告警信息
#msg 错误信息 site 位置
def addAlartLog(msg,site):
	cur = con.cursor()
	print('alert msg'+msg+'  site:'+site)
	sql = "insert into log(starttime,site,msg," \
		  ") " \
		  "value(now(),'%s','%s')"
	cur.execute(sql % (site, msg))
	con.commit()
	cur.close()
#温度大于80摄氏度，湿度大于90% ,二氧化碳浓度大于3000进行报警
def checkData(temperature,humidity,co2val):
	if(temperature>80 or temperature<-30):
		addAlartLog('temp is too high,'+temperature,'阳台')
	if(humidity>90):
		addAlartLog('Humidity is too high,' + temperature, '阳台')
	if(co2val>3000):
		addAlartLog('co2 is too high,' + temperature, '阳台')
###根据时间段删除历史数据
def delByTimeAndSite(sttime,endtime,site):
	# con = pymysql.connect(
	# 	host='localhost',
	# 	port=3306,
	# 	user='root',
	# 	password='111111',
	# 	db='sunpeng',
	# 	charset='utf8'
	# )
	cur = con.cursor()
	if(sttime is not None and endtime is not None):
		cur.execute("delete from  sensordata where site ='%s' and  create_time  between (%s,%s)  " % (
			site, sttime, endtime))

	else:#全部删除
		cur.execute("delete from  sensordata")
	con.commit()
	cur.close()

def destroy():
	if con is not None:
		print("close con =>"+str(con))
		cur=con.cursor
		if(cur is not None):
			print("close cur =>" + str(cur))
			cur.close
