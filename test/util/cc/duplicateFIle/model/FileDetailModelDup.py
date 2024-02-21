# -*- coding: utf-8 -*-
import datetime
from test.util.cc.duplicateFIle.model.Datasetup import engine ,Base
from sqlalchemy import Column, Integer, String, DateTime,Index,Float
# # 绑定引擎
# Session = sessionmaker(bind=engine)
# # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# # 内部会采用threading.local进行隔离
# session = scoped_session(Session)

class FileDetailModelDup(Base):
    __table_args__ = {"extend_existing": True}  # < new
    __tablename__ = 'filedetails_dup'  # 表名
    id = Column(Integer, primary_key=True)
    hcode = Column(String(50))
    isdir = Column(Integer)
    path= Column(String(500))
    filename= Column(String(500))
    filetype = Column(String(10))
    belong = Column(String(45))
    keyword = Column(String(200))
    systemdriver=Column(String(50))
    platformscan = Column(String(10))
    filesize =Column(Float,default=0.0000)

    creattime= Column(DateTime, default=datetime.datetime.now, comment="扫描文件时间")
    modifiedtime= Column(DateTime, default=datetime.datetime.now, comment="文件修改时间")
    __table__args__ = (
        # Index("hcode", "path", "filename", unique=True),  # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} hcode:{self.hcode} isdir:{self.isdir}  " \
               f"path:{self.path} filename:{self.filename} filetype:{self.filetype} " \
               f"belong:{self.belong} keyword:{self.keyword} systemdriver:{self.systemdriver} " \
               f"platformscan:{self.platformscan}  filesize:{self.filesize}" \
               f"creattime:{self.creattime} modifiedtime:{self.modifiedtime}>"
        # 初始化中给对象属性赋值

    def __init__(self, hcode, isdir, path, filename, filetype,
                 systemdriver, platformscan,
                 keyword, belong, filesize):
        self.hcode = hcode
        self.isdir = isdir
        self.path = path
        self.filename = filename
        self.filetype = filetype
        self.systemdriver = systemdriver
        self.platformscan = platformscan
        self.keyword = keyword
        self.belong = belong
        self.filesize = filesize
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