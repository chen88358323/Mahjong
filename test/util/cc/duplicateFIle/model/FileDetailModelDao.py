# -*- coding: utf-8 -*-

from test.util.cc.duplicateFIle.model.Datasetup import engine ,Base
from test.util.cc.duplicateFIle.model.FileDetailModel import FileDetailModel
from test.util.cc.duplicateFIle.model.FileDetailModelDup import FileDetailModelDup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from test.util.cc.duplicateFIle import logger
from test.util.cc.duplicateFIle.utils import  strutil
from sqlalchemy.sql import text
# # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# # 内部会采用threading.local进行隔离
# session = scoped_session(Session)


# # 绑定引擎
Session = sessionmaker(bind=engine)
#根据 hcode filename 查询是否存在记录
def queryfilebycodefn(hcode :str , filename:str):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        filelist = session.query(FileDetailModel).filter_by(FileDetailModel.hcode == hcode,
                                                            FileDetailModel.filetype == filename).all()
    if filelist is None or len(filelist)==0:#这里好像判断没啥用，不如直接返回
        return  None
    else:
        return filelist
def queryfilebycode(hcode :str ):
    # Create a session to interact with the database
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        file = session.query(FileDetailModel).filter(FileDetailModel.hcode == hcode).first()

    return file

#获取数量
def querydupfileCounts():
    num=0
    # Create a session to interact with the database
    with Session() as session:
        num=session.query(func.count(FileDetailModel.id)).scalar()
    return num

#off  表示 offset 偏移量
#lim  表示limit 查询数量
def queryAlldupfilesByOffset(off,lim):
    with Session() as session:
        num=session.query(FileDetailModelDup).offset(off).limit(lim)
    return num

def queryAlldupfiles():
    with Session() as session:
        dupfilelist=session.query(FileDetailModelDup).\
            order_by(FileDetailModelDup.creattime.desc()).all()
        print(type(dupfilelist))
        for f in dupfilelist:
            print(f)
    return dupfilelist

def truncatetables(tablename):
    sql="truncate table "+tablename
    with Session() as session:
        # filelist=session.query(FileDetailModel).filter_by(FileDetailModel.hcode==hcode,FileDetailModel.filetype==filename).all()
        filelist = session.execute(text(sql))
        logger.log.info("sql "+sql+" is done")


def addBatch(list):#todo 唯一性失败，优化细分
    logger.log.info("add batch "+str(len(list)))
    filedetailmodeList=iter(list)
    se=Session()
    try:
        se.bulk_save_objects(filedetailmodeList)
        se.commit()
    except SQLAlchemyError as e:
        print('SQLAlchemyError '+str(e))
        se.rollback()
        clearDuplicatRecorders(list)
    except	IntegrityError as e:
        print('IntegrityError ' + str(e))
        se.rollback()

    finally:
        se.close()
        list.clear()

def convert2FileDetailModelDup(fileDetailModel):
    dupobj = FileDetailModelDup(fileDetailModel.hcode, fileDetailModel.isdir,
                                fileDetailModel.path, fileDetailModel.filename, fileDetailModel.filetype,
                                fileDetailModel.systemdriver,fileDetailModel.platformscan,None,None)
    return dupobj


#批量插入会有重复数据，需要进行清理
def clearDuplicatRecorders(filedetailmodeList):
    hashs = []
    for filedetails in filedetailmodeList:
        hashs.append(filedetails.hcode)
    with Session() as se:
        rows=se.query(FileDetailModel).filter(FileDetailModel.hcode.in_(hashs)).all()
        # [Shoe.query.filter_by(id=id).one() for id in my_list_of_ids]
        # res=[row.to_dict() for row in rows]
    if rows is not None and len(rows)>0:#获取hcode重复数据
        logger.log.info("数据插入中，该批次存在重复数据")
        duplist=[]
        for dbrecoder in rows:
            logger.log.error("dulicate dbrecoder  hcode:"+dbrecoder.hcode+'  filename'+dbrecoder.filename)
            idx=hashs.index(dbrecoder.hcode)
            hashs.pop(idx)
            removefd=filedetailmodeList.pop(idx)#FileDetailModel对象需要转化为FileDetailModelDup对象

            dbpath=dbrecoder.systemdriver+dbrecoder.path+dbrecoder.filename
            removedpath=removefd.systemdriver+removefd.path+removefd.filename
            if dbpath!=removedpath:
                dupobj = convert2FileDetailModelDup(removefd)
                duplist.append(dupobj)
                logger.log.error("dbrecoder hcode:" + dbrecoder.hcode + '  filename:' + strutil.clearpath(dbrecoder.filename))
                logger.log.error("scanfile  hcode:" + removefd.hcode + '  filename' + strutil.clearpath(removefd.filename))
            #TODO 将重复数据装入torr-dupilicate表
        if(duplist is not None and len(duplist)>0):
            logger.log.info("重复数据更新至filedetail_dup表中，数量"+str(len(duplist)))
            addBatch(duplist)
            duplist.clear()
        if(filedetailmodeList is not None and len(filedetailmodeList)>0):#清理后还有待插入项
            logger.log.info("去重后该批次数据 "+str(len(filedetailmodeList)))
            addBatch(filedetailmodeList)
            filedetailmodeList.clear()
        else:
            logger.log.error("去重后该批次没有需要插入的数据")
    else:
        logger.log.error("数据插入中，该批次不存在重复数据")
