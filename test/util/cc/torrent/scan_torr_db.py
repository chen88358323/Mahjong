from torrentool.api import Torrent
import zipfile
from pathlib import Path

# from torrentool.api import TorrentFile
from torrentool.exceptions import BencodeDecodingError
from torrent_download_files_check import  DownLoadCheck
import os
import  shutil
import mysqlTemplate as dbtool
import time,copy
import queue,threading
import loggerTemplate

loger= loggerTemplate.log
TORR_ERROR_DIRNAME='errorbak'
HALF_NAME_PREFIX='HALF-'
logpath='D:\\temp\\0555\\'

#根据路径名扫描入库,判断种子是否重复
def scanTorrentsIntoDB(torrDir):
    p1 = threading.Thread(target=convert_torr_and_get_torr_list, args=(torrDir,))

    p1.start()
    time.sleep(3)
    c1 = threading.Thread(target=consumMsg)
    c1.start()

def convert_torr_and_get_torr_list(torrDir):
    pre_slove_error_torrs(torrDir)
    getTorListByDir(torrDir)

#数据库插入缓冲池
dbqueue = queue.Queue()
#入库查重批次个数
batchsize=100
#torrPathlist 种子路径列表
# 列表每条记录包括 hcode ,path, filename
def consumMsg():
    count=0

    while True:
        datalist = []
        # if count==20:
        #     break
        if dbqueue.empty():
            loger.info("dbqueue is empty")
            time.sleep(3)
        else:
            datalist=dbqueue.get()
            count+=len(datalist)
            loger.info("consum msg len=>:"+str(count))
            #1.批量插入数据
            tag = dbtool.recoderbatch(datalist,1)
            if(not tag):#插入失败
                # clearTorr()

                hashs=gethashlist(datalist)
                    #[hash, path, filename]

                #1.1同一批次中，有重复的hcode，做一次过滤
                loger.info('-------------clearDupTorrHandler-----------')
                datalist,hashs=clearDupTorrHandler(datalist,hashs)
                # 生成map对象，key 为hash val 为#[hash, path, filename]
                dataDict = build_torrObj_dic(datalist)
                #1.查询主数据表，hcode相同既相同
                # result dataset  [id ,hcode,path,filename,time]
                dbrs=dbtool.queryByHashCode(hashs)
                #2.查询重复数据表，hcode path filename 都相同才
                loger.info('-------------filterDirtyData----------')
                datalist=filterDirtyData(dataDict ,dbrs)
                if datalist is not None and len(datalist) >0:
                    dbtool.recoderbatch(datalist,2)
                    dataDict.clear()
                    datalist.clear()
            else:
                datalist.clear()
                loger.info('数据批量插入成功!!!')
                loger.info("count:"+str(count))
