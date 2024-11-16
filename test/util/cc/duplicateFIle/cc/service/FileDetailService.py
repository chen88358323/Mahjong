import copy
from test.util.cc.duplicateFIle.cc.model import FileDetailModelDup, FileDetailModel, FileDetailModelDao,FileDetailModelDupDao
from test.util.cc.duplicateFIle.cc.utils import logger,encryutil,dirutil,strutil
import json
def convert2FileDetailModelDup(fileDetailModel):
    dupobj = FileDetailModelDup.FileDetailModelDup(fileDetailModel.hcode, fileDetailModel.isdir,
                                fileDetailModel.path, fileDetailModel.filename, fileDetailModel.filetype,
                                fileDetailModel.systemdriver,fileDetailModel.platformscan,None,None,
                                fileDetailModel.filesize,fileDetailModel.virdriver)
    print('******FFFFFFFFFFF******'+str(dupobj))
    return dupobj
#查询重复文件总数
def queryDupFileCount():
    return  FileDetailModelDao.querydupfileCounts()

def queryAlldupfiles():
    limit=queryDupFileCount()
    return  FileDetailModelDupDao.queryAlldupfilesByOffset(0,limit)

def truncateTables():
    FileDetailModelDao.truncatetables(FileDetailModel.FileDetailModel.__tablename__)
    FileDetailModelDao.truncatetables(FileDetailModelDup.FileDetailModelDup.__tablename__)


def queryfilebycode(hcode):
    return FileDetailModelDao.queryfilebycode(hcode)

def updateFileBycode(hcode):
    FileDetailModelDao.updateFileBycode(hcode)

def delDupFileByID(id,hcode):
    FileDetailModelDao.delDupFileByID(id,hcode)
def addFileDetailDupBatch(list):#todo 唯一性失败，优化细分
    # logger.log.info("add batch "+str(len(list)))
    # filedetailmodeList=iter(list)
    fduplist=[]
    #1.clear 重复数据
    for filedup in list:
        rs=FileDetailModelDupDao.querydupfiledetail(filedup.hcode,filedup.virdriver,
                           filedup.systemdriver,filedup.path,
                           filedup.filename)
        if not rs:
            fduplist.append(filedup)
    logger.log.info("插入fildetaildup表数据，总数:" + str(len(list))
                    + "实际数据条数:" + str(len(fduplist))
                    )# + "重复数据条数:" + str(len(rs))
    if fduplist is not None and len(fduplist)>0:
        FileDetailModelDupDao.addDBatch(fduplist)

#FileDetailModelDup对象转json
# def FileDuptoJson(obj):
#     json=FileDetailModelDup.to_json(obj)
#     print('convert json '+json)
#
# def loadJson2FileDup(json):
#     dic=json.loads(json)
#     fdmd= FileDetailModelDup.from_json(dic)
#     print('convert str 2 obj'+str(fdmd))
def delBatchByHC_PATH_FN(hashs,pathes,filenames):
    FileDetailModelDao.delBatchByHC_PATH_FN(hashs,pathes,filenames)

#从filedetail对象列表中，抽取hcode
def build_HashList_FromFileDetaiList(filedetailmodeList):
    hashs = []
    for filedetails in filedetailmodeList:
        hashs.append(filedetails.hcode)
    return  hashs

#
def addFileDetailBatch(filedetailmodeList):
    #抽取hcode 生成list
    hashs = build_HashList_FromFileDetaiList(filedetailmodeList)
    #使用hcodelist 查询数据库中对应的数据
    rows = FileDetailModelDao.queryFileDetailModelInHcode(hashs)
    if rows is not None and len(rows) > 0:  # 存在重复数据
        logger.log.info("数据插入中，该批次总数:" + str(len(filedetailmodeList))
                        + "存在重复数据条数:" + str(len(rows)))
        duplist = []
        # 返回值，在该列表删除重复数据，保证删除元素，不会修改index号
        rslist=copy.deepcopy(filedetailmodeList)
        for dbrs in rows:
            logger.log.error("dulicate dbrow  hcode:" +
                             dbrs.hcode + '  filename' + dbrs.filename)
            hash=dbrs.hcode
            index=hashs.index(hash)
            obj=filedetailmodeList[index]
            # print('hash '+hash+' index='+hash)
            # print('filedetailmodeList len '+str(len(filedetailmodeList)))
            # print('rslist len ' + str(len(rslist)))

            rslist=[rs for rs in rslist if not (
                    rs.virdriver == obj.virdriver and
                    rs.hcode == obj.hcode and
                    rs.path == obj.path and
                    rs.systemdriver == obj.systemdriver and
                    rs.filename == obj.filename
            )]

            #rslist.pop(obj)#报错，所以有了上面的推导式
            # 因为遍历会乱index，所以只能找出对象再删除影子队列

            dupobj=compare_filedetail_with_dbrecoder(obj,dbrs)
            if dupobj is not None:
                duplist.append(dupobj)

        if (duplist is not None and len(duplist) > 0):
            FileDetailModelDupDao.addFileDetailDupBatch(duplist)
            duplist.clear()
        if (rslist is not None and len(rslist) > 0):  # 清理后还有待插入项
            logger.log.info("插入fildetail表数据总数 " + str(len(rslist)))
            FileDetailModelDao.addBatch(rslist)
            rslist.clear()
        else:
            logger.log.error("去重后该批次没有需要插入的数据")
    else:#不存在重复数据
        logger.log.info("插入fildetail表数据总数 " + str(len(filedetailmodeList)))
        FileDetailModelDao.addBatch(filedetailmodeList)
        filedetailmodeList.clear()

#removefd filedetail对象 [重复或者插入重复表的对象]
#dbrow 数据库对象
#返回重复数据，为空表示数据库存在该数据，
# 不为空，表示需要查询dup表，确认是否新增还是忽略
def compare_filedetail_with_dbrecoder(removefd,dbrow):
    dbpath = dbrow.systemdriver + dbrow.path + dbrow.filename
    removedpath = removefd.systemdriver + removefd.path + removefd.filename
    if dbpath != removedpath:
        print('1')
        print(str(removefd))
        dupobj = convert2FileDetailModelDup(removefd)
        logger.log.error("dbrow hcode:" + dbrow.hcode)
        logger.log.error("dbrow " + '  filename:' + dbrow.systemdriver + dbrow.path + dirutil.osseparator + strutil.clearpath(
            dbrow.filename))
        logger.log.error(
            "scanfile  " + '  filename:' + removefd.systemdriver + removefd.path + dirutil.osseparator + strutil.clearpath(
                removefd.filename))
        return dupobj
    else:
        logger.log.error("重复扫描的数据，可忽略")
        return None
#@DEPRATE
# def addBatchFileDetails(filedetailmodeList):
#     hashs = build_HashList_FromFileDetaiList(filedetailmodeList)
#     rows=FileDetailModelDao.queryFileDetailModelInHcode(hashs)
#
#     if rows is not None and len(rows)>0:#获取hcode重复数据
#         logger.log.info("数据插入中，该批次总数:"+str(len(filedetailmodeList))
#                         +"存在重复数据条数:"+str(len(rows)))
#         duplist=[]
#
#         for dbrow in rows:
#             logger.log.error("dulicate dbrow  hcode:" +
#                              dbrow.hcode + '  filename' + dbrow.filename)
#             #todo has bug
#             idx=hashs.index(dbrow.hcode)
#             hashs.pop(idx)
#             removefd=filedetailmodeList.pop(idx)#FileDetailModel对象需要转化为FileDetailModelDup对象
#
#             dbpath=dbrow.systemdriver+dbrow.path+dbrow.filename
#             removedpath=removefd.systemdriver+removefd.path+removefd.filename
#             if dbpath!=removedpath:
#                 dupobj = convert2FileDetailModelDup(removefd)
#                 duplist.append(dupobj)
#                 logger.log.error("dbrow hcode:" + dbrow.hcode)
#                 logger.log.error("dbrow " + '  filename:' + dbrow.systemdriver + dbrow.path + osseparator + strutil.clearpath(dbrow.filename))
#                 logger.log.error("scanfile  " + '  filename:' + removefd.systemdriver + removefd.path + osseparator + strutil.clearpath(removefd.filename))
#             else:
#                 logger.log.error("重复扫描的数据，可忽略")
#
#             #TODO 将重复数据装入torr-dupilicate表
#         if(duplist is not None and len(duplist)>0):
#             FileDetailModelDupDao.addFileDetailDupBatch(duplist)
#             duplist.clear()
#         if(filedetailmodeList is not None and len(filedetailmodeList)>0):#清理后还有待插入项
#             logger.log.info("插入fildetail表数据总数 " + str(len(filedetailmodeList)))
#             FileDetailModelDao.addBatch(filedetailmodeList)
#             filedetailmodeList.clear()
#         else:
#             logger.log.error("去重后该批次没有需要插入的数据")
#     else:
#         logger.log.error("数据插入中，该批次不存在重复数据")
# r("数据插入中，该批次不存在重复数据")