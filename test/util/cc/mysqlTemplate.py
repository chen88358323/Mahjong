import pymysql
import loggerTemplate

loger=loggerTemplate.log
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
	loger.info(recorder+path)
	sql="insert into torrents(creattime,hcode,path," \
		"filename) " \
		"values(now(),'%s','%s','%s')"
	cur.execute(sql %(hcode ,path, filename))
	# cur.executemany(sql %(hcode ,path, filename))
	con.commit()
	cur.close()

def recorderDulicateTorrent(hcode, path, filename):
	try:
		loger.info('recorderDulicateTorrent '+filename+'  '+path)
		cur = con.cursor()
		sql = "insert into torrents_dup(creattime,hcode,path," \
			  "filename) " \
			  "values(now(),%s,%s,%s)"
		cur.execute(sql ,(hcode, path, filename))
	# cur.executemany(sql %(hcode ,path, filename))
		con.commit()
	except Exception as e:
		loger.info("recorderDulicateTorrent插入失败 Exception" + hcode+'  '+path+'  '+ filename)
		loger.info("recorderDulicateTorrent插入失败 Exception"+str(e))
		return  False
	except pymysql.err.IntegrityError as due:
		loger.info("recorderDulicateTorrent插入失败 Exception" + hcode + '  ' + path + '  ' + filename)
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		loger.info("recorderDulicateTorrent插入失败 IntegrityError"+str(due))
		return False
	finally:
		cur.close()


# def queryTorrentsInHcode():

def delDulicateTorrent(hashs):
	res=True
	cur=con.cursor()
	try:
		sql = "delete from torrents_dup  where torrents_dup.id in ('{}')".format("','".join(hashs))
		cur.execute(sql)
		con.commit()
		# 获取查询结果
		# results = cur.fetchall()
		#loger.info("query result:" + str(results))
	except Exception as e:
		res = False
		con.rollback()
		loger.info("queryByHashCode失败 Exception"+str(e))
	except pymysql.err.IntegrityError as due:
		res = False
		con.rollback()
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		loger.info("queryByHashCode IntegrityError"+str(due))

	finally:
		# con.close()
		cur.close()
		return res



#@return  format   list [id ,hcode,path,filename,time]
def queryduplicatetor():
	results=[]
	cur=con.cursor()
	try:
		sql = "select * from torrents_dup  "
			  # ' (' + ','.join('?'*len(hashs)) + ')'
		cur.execute(sql)
		# 获取查询结果
		results = cur.fetchall()
		#loger.info("query result:" + str(results))
	# if results is not None and len(results) >0:
	# 	for data in results:
	except Exception as e:
		loger.info("queryByHashCode失败 Exception"+str(e))
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		loger.info("queryByHashCode IntegrityError"+str(due))

	finally:
		# con.close()
		cur.close()
		return results
#@return  format   list [id ,hcode,path,filename,time]
#根据hcode 文件名查询是否存在记录
def querydupTorrByHcodeAndFnAndPath(hcode,fn,fpath):
	results=[]
	cur=con.cursor()
	try:
		sql = "select * from torrents_dup td  where td.hcode =%s " \
			  "and td.filename=%s" \
			  "and td.path=%s"
		conditionval=(hcode,fn,fpath)
			  # ' (' + ','.join('?'*len(hashs)) + ')'
		cur.execute(sql,conditionval)
		# 获取查询结果
		results = cur.fetchall()
		#loger.info("query result:" + str(results))
	# if results is not None and len(results) >0:
	# 	for data in results:
	except Exception as e:
		loger.info("queryByHashCode失败 Exception"+str(e))
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		loger.info("queryByHashCode IntegrityError"+str(due))

	finally:
		# con.close()
		cur.close()
		return results

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
		loger.debug("批量插入失败 Exception" + str(list))
		loger.info("批量插入失败 Exception"+str(e))
		return  False
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		con.rollback()
		loger.debug("批量插入失败 IntegrityError"+str(due))
		return False
	finally:
		# con.close()
		cur.close()
def truncateTable():
	cur = con.cursor()
	try:
		sql = "truncate torrents"
		cur.execute(sql)
		sql = "truncate torrents_dup"
		cur.execute(sql)
		con.commit()
	except Exception as e:
		con.rollback()
		loger.info("truncateTable Exception" + str(list))
		loger.info("truncateTable Exception" + str(e))
	finally:
		# con.close()
		cur.close()
# def truncateTable(tablename):
# 	try:
# 		with con.cursor() as cursor:
# 			# SQL TRUNCATE TABLE 语句
# 			sql = "TRUNCATE TABLE `{}`".format(tablename)
# 			cursor.execute(sql)
#
# 		# 提交事务
# 		con.commit()
#
# 	except pymysql.MySQLError as e:
# 		loger.info("Error: unable to truncate table", e)
# 		loger.info("truncateTable Exception" + str(tablename))
# 		loger.info("truncateTable Exception" + str(e))
# 		# 关闭数据库连接
# 		# cursor.close()
# 		# con.close()




def queryByHashCode(hashs):
	cur=con.cursor()
	rs=[]
	try:
		sql = "select * from  torrents  where  torrents.hcode in ('{}')".format("','".join(hashs))
			  # ' (' + ','.join('?'*len(hashs)) + ')'
		cur.execute(sql)
		# 获取查询结果
		results = cur.fetchall()

		rs=[list(row) for row in results]

		#loger.info("query result:" + str(results))
	# if results is not None and len(results) >0:
	# 	for data in results:
	except Exception as e:
		loger.info("queryByHashCode失败 Exception"+str(e))
	except pymysql.err.IntegrityError as due:
		# Map some error codes to IntegrityError, since they seem to be
		# misclassified and Django would prefer the more logical place.
		loger.info("queryByHashCode IntegrityError"+str(due))

	finally:
		# con.close()
		cur.close()
		return rs



if __name__ == '__main__':
	truncateTable('')
	recorderDulicateTorrent('111', 'D:\temp\b31\2', '11')
	recorderDulicateTorrent('121','D:\\temp\\b31\\2','11')
	truncateTable('')
	# truncateTable('torrents')
# 增加告警信息
#msg 错误信息 site 位置
# def addAlartLog(msg,site):
# 	cur = con.cursor()
# 	loger.info('alert msg'+msg+'  site:'+site)
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

