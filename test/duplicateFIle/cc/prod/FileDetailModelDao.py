# -*- coding: utf-8 -*-

import datetime
import datasetup
import FileDetailModel
import FileDetailModelDup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
import logger, strutil
from sqlalchemy.sql import text
import  datetime,os
datasetup=datasetup.Datasetup()
engine=datasetup.engine
# import sqlalchemy
# print(sqlalchemy.__version__)
osseparator=os.path.sep
# # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# # 内部会采用threading.local进行隔离
# session = scoped_session(Session)

file_detail_model=FileDetailModel.FileDetailModel
file_detail_dup_model=FileDetailModelDup.FileDetailModelDup
# # 绑定引擎
Session = sessionmaker(bind=engine)
#根据 hcode filename 查询是否存在记录
def queryfilebycodefn(hcode :str , filename:str):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        filelist = session.query(file_detail_model).filter_by(file_detail_model.hcode == hcode,
                                                            file_detail_model.filetype == filename).all()
    if filelist is None or len(filelist)==0:#这里好像判断没啥用，不如直接返回
        return  None
    else:
        return filelist



def queryfilebycode(hcode :str ):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(file_detail_model).filter_by(file_detail_model.hcode==hcode,file_detail_model.filetype==filename).all()
        file = session.query(file_detail_model).\
            filter(file_detail_model.hcode == hcode
                   ).first()

    return file

def updateFileBycode(hcode:str):
    with Session() as se:
        file=se.query(file_detail_model).filter(file_detail_model.hcode == hcode).first()
        logger.log.info("update before " + str(file))
        dupfile=se.query(file_detail_dup_model).filter(file_detail_dup_model.hcode == hcode).first()
        file=convertDupFile2File(file,dupfile)
        logger.log.info("update after " + str(file))
        se.commit()
# def delDupFileByID(id:str,hcode:str):
#     with Session as session:
#         logger.log.info("delete   done  id:" + id+" hcode:"+hcode)
#         session.query(file_detail_dup_model).filter(file_detail_dup_model.id == id ,
#                                             file_detail_dup_model.hcode==hcode)\
#             .first().delete()
#         session.commit()
def delDupFileByID(id:str,hcode:str):
    logger.log.info("delete   done  id:" + str(id) + " hcode:" + hcode)
    with Session() as session:
        dupfile=session.query(file_detail_dup_model).filter(file_detail_dup_model.id == id ,
                                            file_detail_dup_model.hcode==hcode).first()
        if(dupfile == None):
            logger.log.info("delDupFileByID   not exist  " + id + "  " + hcode)
            return None
        else:
            logger.log.info("delete   done  " + str(dupfile))
            session.delete(dupfile)
            session.commit()


def querydupfilebycode(hcode :str ):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        file = session.query(file_detail_dup_model).filter(file_detail_dup_model.hcode == hcode).first()

    return file
#获取数量
def querydupfileCounts():
    num=0
    # Create a session to interact with the database
    with Session() as session:
        num=session.query(func.count(file_detail_model.id)).scalar()
    return num



def truncatetables(tablename):
    sql="truncate table "+tablename
    with Session() as session:
        # filelist=session.query(file_detail_model).filter_by(file_detail_model.hcode==hcode,file_detail_model.filetype==filename).all()
        filelist = session.execute(text(sql))
        session.commit()
        logger.log.info("sql " + sql + " is done")

@strutil.getDbTime
def addBatch(list):#todo 唯一性失败，优化细分
    # logger.log.info("add batch "+str(len(list)))
    filedetailmodeList=iter(list)
    se=Session()
    try:
        se.bulk_save_objects(filedetailmodeList)
        se.commit()
    except SQLAlchemyError as e:
        print('SQLAlchemyError '+str(e))
        se.rollback()
        # clearDuplicatRecorders(list)
    except	IntegrityError as e:
        print('IntegrityError ' + str(e))
        se.rollback()

    finally:
        se.close()




#select  where  hcode in
@strutil.getDbTime
def queryFileDetailModelInHcode(hashs):
    with Session() as se:
        rows = se.query(file_detail_model).filter(file_detail_model.hcode.in_(hashs)).all()
    return  rows

#根据文件名，路径，hcode删除数据，与删除缓存同时使用
@strutil.getDbTime
def delBatchByHC_PATH_FN(hashs,pathes,filenames):#todo 唯一性失败，优化细分

    with Session() as se:
        rows = se.query(file_detail_model).filter(file_detail_model.hcode.in_(hashs),
                                                file_detail_model.path.in_(pathes),
                                                file_detail_model.filename.in_(filenames)
                                                ).delete(synchronize_session='fetch')
        se.commit()
    return rows, hashs

def convertDupFile2File(file,dupfile):
    file.path=dupfile.path
    file.filename=dupfile.filename
    file.filetype=dupfile.filetype
    file.systemdriver=dupfile.systemdriver
    file.platformscan=dupfile.platformscan
    file.virdriver=dupfile.virdriver
    file.filesize=dupfile.filesize
    file.creattime=dupfile.creattime
    file.modifiedtime=datetime.datetime.now()
    return file

#todo 出现递归异常了。。。
#批量插入会有重复数据，需要进行清理
# def clearDuplicatRecorders(filedetailmodeList):
#     hashs = []
#     for filedetails in filedetailmodeList:
#         hashs.append(filedetails.hcode)
#     rows=queryFileDetailModelInHcode(hashs)
#         # [Shoe.query.filter_by(id=id).one() for id in my_list_of_ids]
#         # res=[row.to_dict() for row in rows]
#     if rows is not None and len(rows)>0:#获取hcode重复数据
#         logger.log.info("数据插入中，该批次总数:"+str(len(filedetailmodeList))
#                         +"存在重复数据条数:"+str(len(rows)))
#         duplist=[]
#         for dbrecoder in rows:
#             logger.log.error("dulicate dbrecoder  hcode:" +
#                              dbrecoder.hcode + '  filename' + dbrecoder.filename)
#             idx=hashs.index(dbrecoder.hcode)
#             hashs.pop(idx)
#             removefd=filedetailmodeList.pop(idx)#FileDetailModel对象需要转化为file_detail_dup_model对象
#
#             dbpath=dbrecoder.systemdriver+dbrecoder.path+dbrecoder.filename
#             removedpath=removefd.systemdriver+removefd.path+removefd.filename
#             if dbpath!=removedpath:
#                 dupobj = convertDupFile2File(removefd)
#                 duplist.append(dupobj)
#                 logger.log.error("dbrecoder hcode:" + dbrecoder.hcode)
#                 logger.log.error("dbrecoder " + '  filename:' + dbrecoder.systemdriver + dbrecoder.path + osseparator + strutil.clearpath(dbrecoder.filename))
#                 logger.log.error("scanfile  " + '  filename:' + removefd.systemdriver + removefd.path + osseparator + strutil.clearpath(removefd.filename))
#             else:
#                 logger.log.error("重负扫描的数据，可忽略")
#
#             #TODO 将重复数据装入torr-dupilicate表
#         if(duplist is not None and len(duplist)>0):
#             logger.log.info("重复数据更新至filedetail_dup表中，数量" + str(len(duplist)))
#             FileDetailModelDupDao(duplist)
#             duplist.clear()
#         if(filedetailmodeList is not None and len(filedetailmodeList)>0):#清理后还有待插入项
#             logger.log.info("去重后该批次数据 " + str(len(filedetailmodeList)))
#             addBatch(filedetailmodeList)
#             filedetailmodeList.clear()
#         else:
#             logger.log.error("去重后该批次没有需要插入的数据")
#     else:
#         logger.log.error("数据插入中，该批次不存在重复数据")
