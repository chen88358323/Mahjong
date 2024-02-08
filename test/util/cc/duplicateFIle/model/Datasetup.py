# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from test.util.cc.duplicateFIle.Conf import  Conf



config= Conf()
engine = create_engine("mysql+pymysql://"+
                       config.readDbConf( "db_user")+":"
                       +config.readDbConf( "db_pass")
                       +"@"+config.readDbConf( "db_host")+":"+
                       config.readDbConf( "db_port")+"/"+config.readDbConf( "db_dabase"))
    # ,
    # encoding='utf8',
    # # 超过链接池大小外最多创建的链接
    # max_overflow=0,
    # # 链接池大小
    # pool_size=5,
    # # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    # pool_timeout=10,
    # # 多久之后对链接池中的链接进行一次回收
    # pool_recycle=1,
    # # 查看原生语句（未格式化）
    # echo=True)
# 基础类
Base = declarative_base()  # 生成orm基类


# Create a function to define the connection creator
def connection_creator():
    return engine.connect()
pool = QueuePool(creator=connection_creator, pool_size=5)

# 绑定引擎
# Session = sessionmaker(bind=engine)
# session = scoped_session(Session)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
