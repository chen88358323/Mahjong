# -*- coding: utf-8 -*-

from test.util.cc.duplicateFIle.model.datasetup import engine ,Base
from test.util.cc.duplicateFIle.model.FileDetailModel import FileDetailModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from test.util.cc.duplicateFIle import logger

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

def addBatch(filedetailmodeList):#todo 唯一性失败，优化细分
    logger.log.info("add batch "+str(len(filedetailmodeList)))
    filedetailmodeList=iter(filedetailmodeList)
    se=Session()
    try:
        se.bulk_save_objects(filedetailmodeList)
        se.commit()
    except SQLAlchemyError as e:
        print('SQLAlchemyError '+str(e))
        se.rollback()
        clearDuplicatRecorders(filedetailmodeList)
    except	IntegrityError as e:
        print('IntegrityError ' + str(e))
        se.rollback()

    finally:
        se.close()
#批量插入会有重复数据，需要进行清理
def clearDuplicatRecorders(filedetailmodeList):
    hashs = []
    for filedetails in filedetailmodeList:
        hashs.append(filedetails.hcode)
    with Session() as se:
        rows=se.query(FileDetailModel).filter(FileDetailModel.hcode.in_(hashs)).all()
        # [Shoe.query.filter_by(id=id).one() for id in my_list_of_ids]
        # res=[row.to_dict() for row in rows]
    if rows is not None and len(rows)>0:
        for dbrecoder in rows:
            logger.log.error("dulicate dbrecoder  hcode:"+dbrecoder.hcode+'  filename'+dbrecoder.filename)
            idx=hashs.index(dbrecoder.hcode)
            hashs.pop(idx)
            removefd=filedetailmodeList.pop(idx)
            logger.log.error("scan filedetail is  hcode:" + removefd.hcode + '  filename' + removefd.filename)
        if(filedetailmodeList is not None and len(filedetailmodeList)>0):#清理后还有待插入项
            addBatch(filedetailmodeList)
        else:
            logger.log.error("去重后该批次没有需要插入的数据")
    else:
        logger.log.error("该批次没有需要插入的数据")