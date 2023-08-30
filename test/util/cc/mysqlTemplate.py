
import pymysql

con = pymysql.connect(
	host='localhost',
	port=3306,
	user='root',
	password='111111',
	db='torr',
	charset='utf8'
)
def recorder(hcode ,path, filename):
	cur=con.cursor()

	sql="insert into torrents(creattime,hcode,path," \
		"filename) " \
		"values(now(),'%s','%s','%s')"
	cur.execute(sql %(hcode ,path, filename))
	# cur.executemany(sql %(hcode ,path, filename))
	con.commit()
	cur.close()

def recorderDulicateTorrent(hcode, path, filename):
	try:
		cur = con.cursor()
		sql = "insert into duplicatetor(creattime,hcode,path," \
			  "filename) " \
			  "values(now(),%s,%s,%s)"
		cur.execute(sql , (hcode, path, filename))
	# cur.executemany(sql %(hcode ,path, filename))
		con.commit()
	except Exception as e:
		con.rollback()
		print("recorderDulicateTorrent插入失败 Exception"+str(e))
		return  False
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		con.rollback()
		print("recorderDulicateTorrent插入失败 IntegrityError"+str(due))
		return False
	finally:
		cur.close()

def recoderbatch(list):
	cur = con.cursor()
	try:
		sql = "insert into torrents(creattime,hcode,path," \
			  "filename) " \
			  "values(now(),%s,%s,%s)"

		cur.executemany(sql, list)
		con.commit()
		return True
	except Exception as e:
		con.rollback()
		print("批量插入失败 Exception"+str(e))
		return  False
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		con.rollback()
		print("批量插入失败 IntegrityError"+str(due))
		return False
	finally:
		# con.close()
		cur.close()



def queryByHashCode(hashs):
	results=[]
	cur=con.cursor()
	try:
		sql = "select * from  torrents  where  torrents.hcode in ('{}')".format("','".join(hashs))
			  # ' (' + ','.join('?'*len(hashs)) + ')'
		cur.execute(sql)
		# 获取查询结果
		results = cur.fetchall()
		#print("query result:" + str(results))
	# if results is not None and len(results) >0:
	# 	for data in results:
	except Exception as e:
		print("queryByHashCode失败 Exception"+str(e))
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		print("queryByHashCode IntegrityError"+str(due))

	finally:
		# con.close()
		cur.close()
		return results





# 增加告警信息
#msg 错误信息 site 位置
# def addAlartLog(msg,site):
# 	cur = con.cursor()
# 	print('alert msg'+msg+'  site:'+site)
# 	sql = "insert into log(starttime,site,msg," \
# 		  ") " \
# 		  "value(now(),'%s','%s')"
# 	cur.execute(sql % (site, msg))
# 	con.commit()
# 	cur.close()
# #温度大于80摄氏度，湿度大于90% ,二氧化碳浓度大于3000进行报警
# def checkData(temperature,humidity,co2val):
# 	if(temperature>80 or temperature<-30):
# 		addAlartLog('temp is too high,'+temperature,'阳台')
# 	if(humidity>90):
# 		addAlartLog('Humidity is too high,' + temperature, '阳台')
# 	if(co2val>3000):
# 		addAlartLog('co2 is too high,' + temperature, '阳台')
# ###根据时间段删除历史数据
# def delByTimeAndSite(sttime,endtime,site):
# 	con = pymysql.connect(
# 		host='localhost',
# 		port=3306,
# 		user='root',
# 		password='111111',
# 		db='torr',
# 		charset='utf8'
# 	)
# 	cur = con.cursor()
# 	if(sttime is not None and endtime is not None):
# 		cur.execute("delete from  sensordata where site ='%s' and  create_time  between (%s,%s)  " % (
# 			site, sttime, endtime))
#
# 	else:#全部删除
# 		cur.execute("delete from  sensordata")
# 	con.commit()
# 	cur.close()

