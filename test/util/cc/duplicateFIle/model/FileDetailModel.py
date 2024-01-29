# -*- coding: utf-8 -*-
import datetime
from test.util.cc.duplicateFIle.model.datasetup import engine ,Base
from sqlalchemy import Column, Integer, String, DateTime,Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
# # 绑定引擎
# Session = sessionmaker(bind=engine)
# # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# # 内部会采用threading.local进行隔离
# session = scoped_session(Session)

class FileDetailModel(Base):
    __tablename__ = 'filedetails'  # 表名
    id = Column(Integer, primary_key=True)
    hcode = Column(String(50))
    isdir = Column(Integer)
    path= Column(String(500))
    filename= Column(String(500))
    filetype = Column(String(10))
    creattime= Column(DateTime, default=datetime.datetime.now, comment="扫描文件时间")
    modifiedtime= Column(DateTime, default=datetime.datetime.now, comment="文件修改时间")
    __table__args__ = (
        # Index("hcode", "path", "filename", unique=True),  # 联合唯一索引
    )
    def __str__(self):
        return f"object : <id:{self.id} hcode:{self.hcode} isdir:{self.isdir}  " \
               f"path:{self.path} filename:{self.filename} filetype:{self.filetype} " \
               f"creattime:{self.creattime} modifiedtime:{self.modifiedtime}>"
        # 初始化中给对象属性赋值

    def __init__(self, hcode, isdir, path,filename,filetype):
        self.hcode=hcode
        self.isdir=isdir
        self.path=path
        self.filename=filename
        self.filetype=filetype
        # if creattime is None:
        #     self.creattime=datetime.datetime.now
        # else:
        #     self.creattime = creattime
        #
        # if modifiedtime is None:
        #     self.modifiedtime=datetime.datetime.now
        # else:
        #     self.modifiedtime = modifiedtime

# Base.metadata.create_all(engine)  # 创建表结构


# #根据 hcode filename 查询是否存在记录
# def queryfilebycodefn(hcode , filename):
#     session.query()