# -*- coding: utf-8 -*-

from .Datasetup import engine
from .FileDetailModel import FileDetailModel
from .FileDetailModelDup import FileDetailModelDup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ..utils import strutil
from ..utils import logger
from sqlalchemy.sql import text
import  datetime,os

# import sqlalchemy
# print(sqlalchemy.__version__)
# # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# # 内部会采用threading.local进行隔离
# session = scoped_session(Session)



# # 绑定引擎
Session = sessionmaker(bind=engine)

#查询是否一致,该方法导致同一个文件win linux的查询结果不一致，TODO
def querydupfiledetail(hcode ,virtualdrive,systemdriver,fpath,filename ):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        file = session.query(FileDetailModelDup).\
            filter(FileDetailModelDup.hcode == hcode,
                   FileDetailModelDup.virdriver == virtualdrive,
                   FileDetailModelDup.systemdriver == systemdriver,
                   FileDetailModelDup.path == fpath,
                   FileDetailModelDup.filename == filename).first()

    return file
#获取数量
def querydupfileCounts():
    num=0
    # Create a session to interact with the database
    with Session() as session:
        num=session.query(func.count(FileDetailModel.id
                                     )).scalar()
    return num
#批量增加重复文件
#1.检查文件路径是否一致，虚拟驱动器是否一致
#2.一致的删除，不一致的插入
@strutil.getDbTime
def addFileDetailDupBatch(list):#todo 唯一性失败，优化细分
    # logger.log.info("add batch "+str(len(list)))
    # filedetailmodeList=iter(list)
    fduplist=[]
    #1.clear 重复数据
    for filedup in list:
        rs=querydupfiledetail(filedup.hcode,filedup.virdriver,
                           filedup.systemdriver,filedup.path,
                           filedup.filename)
        if not rs:
            fduplist.append(rs)
    logger.log.info("插入fildetaildup表数据，总数:" + str(len(list))
                    + "实际数据条数:" + str(len(fduplist))
                    )#+ "重复数据条数:" + str(len(rs))
    if fduplist is not None and len(fduplist)>0:
        addDBatch(fduplist)

@strutil.getDbTime
def addDBatch(list):#todo 唯一性失败，优化细分
    # logger.log.info("add batch "+str(len(list)))
    # fduplist=iter(list)
    # list=iter(list)
    se=Session()
    try:
        se.add_all(list)
        # se.bulk_save_objects(list)
        se.commit()
    except SQLAlchemyError as e:
        print('SQLAlchemyError '+str(e))
        se.rollback()
    except	IntegrityError as e:
        print('IntegrityError ' + str(e))
        se.rollback()

    finally:
        se.close()
#off  表示 offset 偏移量
#lim  表示limit 查询数量
def queryAlldupfilesByOffset(off,lim):
    with Session() as session:
        num=session.query(FileDetailModelDup).offset(off).limit(lim)
    return num
