from test.util.cc.duplicateFIle.cc.model import FileDetailModelDao, ESv2
from test.util.cc.duplicateFIle.cc.utils import logger


def add_dup_Idx():
    #1.query filedetails_dup data
    num = FileDetailModelDao.querydupfileCounts()
    if (num > 0):
        print('show result duplicate num:' + str(num))
        # 1.获取重复数据列表
        dupfilelist = FileDetailModelDao.queryAlldupfiles()
        if dupfilelist is not None and len(dupfilelist) > 0:
            for dupfile in dupfilelist:
                # 2.query es data
                logger.log.warning("start index  " + ESv2.es_filedetaildup_name)
                # 3.add or update es data
                ESv2.createESIdx(ESv2.es_filedetaildup_name, dupfile,dupfile.id)
        else:
            logger.log.warning("*******************************************")
            logger.log.warning("filedetail_dup 无数据")


    else:
        print('filedetail_dup 无重复数据')

    #for add  es
def creatDoc():
    logger.log.warning("*************start creatDoc****************")
    ESv2.creatDoc(ESv2.es_filedetail_name)
    ESv2.creatDoc(ESv2.es_filedetaildup_name)
    logger.log.warning("*************end creatDoc****************")

def queryfiledetails_dup():
    logger.log.warning("*************start queryAll****************")
    ESv2.queryAll(ESv2.es_filedetaildup_name)
    logger.log.warning("*************end queryAll****************")

def delDoc():
    logger.log.warning("*************start delDoc****************")
    ESv2.delDoc(ESv2.es_filedetaildup_name)
    logger.log.warning("*************end delDoc****************")
if __name__ == '__main__':
    # creatDoc()
    # add_dup_Idx()
    queryfiledetails_dup()
    # delDoc()
