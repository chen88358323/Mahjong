from torrentool.api import Torrent
from pathlib import Path

# from torrentool.api import TorrentFile
from torrentool.exceptions import BencodeDecodingError
import os
import  shutil

import time,copy
import queue,threading
import loggerTemplate
import mysqlTemplate as dbtool
import loggerTemplate as tlog
loger= tlog.log
TORR_ERROR_FILE='errorbak'
TORR_REWRITE_FILE='rewrite'
HALF_NAME_PREFIX='HALF-'
logpath='D:\\temp\\0555\\'

#根据路径名扫描入库,判断种子是否重复
def scanTorrentsIntoDB(torrDir):
    load_torr_thread_start(torrDir)
    time.sleep(3)
    parse_torr_thread_start()

def load_torr_thread_start(torrDir):
    p1 = threading.Thread(target=convert_torr_and_get_torr_list, args=(torrDir,))
    p1.start()
def parse_torr_thread_start():
    c1 = threading.Thread(target=consumMsg)
    c1.start()

def convert_torr_and_get_torr_list(torrDir):
    get_tor_list_by_dir(torrDir)


#解决种子异常问题
# 1.修复种子数据内容，通常为结尾\r\n造成读取异常，直接去除\r\n即可
# 2.种子小于1k，通常为异常文件，迁移到异常目录
#file_path 全路径
#filename 文件名称，含后缀
#err_back_path 异常文件夹
def fix_torrent(dirname,file_path,error_count):
    if(error_count>2):
        return  None
    else:
        recreate_torrent(dirname,file_path)
        return loadTorr_and_fixed(dirname,file_path,error_count)

#异常种子处理，写日志，转移到异常文件夹
def move_error_torrent(torr,err_back_path):
    mkdirs(err_back_path)
    txt = tlog.file_writer_straght(err_back_path, TORR_ERROR_FILE, True)
    txt.writelines("************************待查找************  " + '\r\n')
    txt.writelines(torr + " is error ，need redownload" + '\r\n')
    txt.close()
    shutil.copy(torr, err_back_path)

#重写文件，即删除最后的\r\n
def recreate_torrent(dirname,file_path):
    # 读取文件内容
    with open(file_path, 'rb') as file:
        file_content = file.read()
        # 检查文件是否以 \r\n 结尾
        if file_content.endswith(b'\r\n'):
            txt = tlog.file_writer_straght(dirname, TORR_REWRITE_FILE, True)
            txt.writelines("************************文件解析异常************  " + '\r\n')
            txt.writelines(file_path + " is rewrite " + '\r\n')
            txt.close()
            new_content = file_content[:-2]
            with open(file_path, 'wb') as file:
                file.write(new_content)
#加载种子，如果种子错误或者内容为空，返回空
#dirname 为文件目录
#torrpath 种子全路径
#error_count 错误重试次数
def loadTorr_and_fixed(dirname,torrpath,error_count):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return  my_torrent
    except BencodeDecodingError:
        error_count+=1
        loger.info("error " + torrpath)
        fix_torrent(dirname,torrpath,error_count)
        # slove_bencode_torr(torrpath)
        return None
    except IndexError:
        loger.info("error " + torrpath)
        return None


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
                hashs=gethashlist(datalist)
                    #[hash, path, filename]

                #1.1同一批次中，有重复的hcode，做一次过滤
                loger.info('-------------clearDupTorrHandler-----------')
                # # datalist 生成map对象，key 为hash val 为#[hash, path, filename]
                datalist,hashs=clear_dup_torr_inlist(datalist, hashs)
                # #2.查询重复数据表，hcode path filename 都相同才
                # loger.info('-------------filterDirtyData----------')
                # datalist=filterDirtyData(dataDict ,dbrs)
                datalist=clear_dup_torr_indb(datalist,hashs)
                batch_torrlist_indb(datalist)
            else:

                loger.info('数据批量插入成功!!!')
                loger.info("count:"+str(count))
            datalist.clear()

def batch_torrlist_indb(datalist):
    if datalist is not None and len(datalist) > 0:
        dbtool.recoderbatch(datalist, 2)
def clear_dup_torr_indb(datalist, hashs):
    # 生成map对象，key 为hash val 为#[hash, path, filename]
    dataDict = build_torrObj_dic(datalist)
    # 1.2查询主数据表，hcode相同既相同
    # result dataset  [id ,hcode,path,filename,time]
    dbrs = dbtool.queryByHashCode(hashs)
    # 2.查询重复数据表，hcode path filename 都相同才
    loger.info('-------------filterDirtyData----------')

    datalist = filter_dirty_data(dataDict, dbrs)
    dataDict.clear()
    return datalist

def gethashlist(datalist):
    hashs = []
    if datalist is not None or len(datalist)>0:
        for arr in datalist:
            # [hash, path, filename]
            hashs.append(arr[0])
    return hashs
#torrlist 清理队列中重复数据
def clear_dup_torr_inlist(datalist, hashs):
    hashset=set(hashs)
    if (len(hashset) == len(hashs)):
        return datalist, hashs
    else:
    #表示该列表有重复hcode的数据  为啥不直接删除得到重复列表
        rslist=copy.deepcopy(datalist)
        st= set()
        duplist = list()
        for o in datalist:
            if o[0] in st:
                duplist.append(o)
                rslist.remove(o)
            else:
                st.add(o[0])
        #进行重复数据处理
        for dup in duplist:#todo 没有列出对比的重复文件
            msg="重复文件:" +dup[0]+ dup[1]+os.path.sep + dup[2]
            loger.info("队列本身存在重复文件"+msg)
            dup_torr_handle(dup[0], dup[1], dup[2], msg)
        return rslist,list(st)
#生成map对象，key 为hash val 为#[hash, path, filename]
def build_torrObj_dic(datalist):
    dict = {}
    if datalist is not None and len(datalist)>0:
        for data in datalist:
            dict[data[0]]=data
    return  dict

# 写日志，插入torrentdup表中，将重复种子移动到duplicate文件夹种
# torrent表or Torrentdup存在,则不做处理
def dup_torr_handle(torrhcode, torrpath, torrfilename, msg):
    loger.debug('dup_torr_handle ' + torrhcode + '  ' + torrpath + '  ' + torrfilename)
    torr_fullpath = torrpath + os.path.sep + torrfilename
    # msg = "重复文件:" +torrhcode+ torrpath+os.path.sep + torrfilename
    # 1.写文件
    writeDupLog(torrpath, msg)
    # 2.move 种子至重复文件夹,
    handle_duptorr(torrhcode,torr_fullpath,torrpath,torrfilename)

def handle_duptorr(torrhcode,torr_fullpath,torrpath,torrfilename):
    if not torrpath.endswith(DUP):#需要将种子，迁移目录，种子路径变化，进行同步修改返回
        torrpath=move_duptorr_dupdir(torr_fullpath, torrpath, torrfilename)
    # 已经是处理过得重复种子，不做处理
    dbset = dbtool.querydupTorrByHcodeAndFnAndPath(torrhcode, torrfilename, torrpath)

    if dbset is not None and len(dbset) > 0:
        # 存在需要对比路径，如果路径不同，需要edit ，因为之前move了
        loger.debug('重复记录已存在，不做处理' + torrhcode + '  ' + torrpath + '  ' + torrfilename)
        # 重复路径存在
        return
    else:  # 重复记录表不存在该记录，直接插入
        loger.debug('重复记录插入' + torrhcode + '  ' + torrpath + '  ' + torrfilename)
        dbtool.recorderDulicateTorrent(torrhcode, torrpath, torrfilename)

def move_duptorr_dupdir(torr_fullpath,torrpath,torrfilename):
    if os.path.isfile(torr_fullpath) and not torrpath.endswith(DUP):  # 文件夹已经是重复文件夹名称了，不做处理
        new_torrpath = torrpath + DUP_DIRNAME
        mkdirs(new_torrpath)
        loger.info('move  ' + torr_fullpath + Enter + 'to  ' + new_torrpath + torrfilename)
        new_torr_fullpath=new_torrpath + torrfilename
        shutil.move(torr_fullpath, new_torr_fullpath)
        return  new_torr_fullpath,new_torrpath
    else:
        return torr_fullpath,torrpath

#dblist 查询数据库返回的重复数据
#datadict # 生成map对象，key 为hash val 为#[hash, path, filename]
#return 返回待插入的数据集
def filter_dirty_data(datadict, dblist):
    if dblist is not None and len(dblist) > 0:
        hashs=datadict.keys()
        rslist=list(datadict.values())
        #查询每条数据库记录
        for dbrs in dblist:
            # [id, hcode, path, filename, time]
            hcode=dbrs[1]

            if hcode in hashs:#做分支，是否转移种子文件
                obj=datadict.get(hcode)
                try:
                    rslist=[tor for tor in rslist if not (
                        tor[0]==dbrs[1]
                        # and
                        # tor[1] == dbrs[2] and
                        # tor[2] == dbrs[3]
                    )]
                    # rslist.pop(obj)

                    # 判断是否为相同文件，相同直接去除，不相同的同源种子，进行位置转移
                    comparefile(obj[0],obj[1],obj[2],
                                dbrs[1],dbrs[2],dbrs[3])
                except TypeError:
                    loger.error('obj is '+str(obj))
                    loger.error('rslist is ' + str(rslist))
                # [hash, path, filename]
        loger.info("filterDirtyData重新插入数据 清理前数据条数" + str(len(hashs))+'  清理后数据条数'+str(len(rslist)))
        #loger.info("filterDirtyData重新插入数据datalist"+str(data_hashlist))
        return rslist
    else:
        return  list(datadict.values())




def getTorListByDirxxx(torrdir):
    datalist = []
    sum = 0
    broken_num=0
    #get_oswalk_desc 获取文件倒序
    for dirpath, dirnames, filenames in os.walk(torrdir):
    # for dirpath, dirnames, filenames in fu.get_oswalk_desc(torrdir):
        i=0
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            #loger.info("=================================")
            #loger.info(portion)
            if portion[1] == ".torrent":
                sum+=1
                # loger.info("================torrent conteng=================" + '\r\n')
                # loger.info(torr)
                try:
                    my_torrent = Torrent.from_file(torr)
                except BencodeDecodingError:
                    #种子下载失败了
                    loger.error('error file '+torr)
                    errorpath=dirpath+'/errfiles'
                    mkdirs(errorpath)
                    shutil.move(torr,errorpath+'/'+filename)
                    broken_num+=1
                    continue
                except IndexError:
                    loger.error('error file ' + torr)
                    continue

                hash = my_torrent.info_hash
                path = os.path.dirname(torr)
                tobj = [hash, path, filename]
                # loger.info('put queue scan file ' + torr)
                # loger.info('put queue scan hash ' + hash)
                datalist.append(tobj)
                if i == batchsize:
                    i = 0
                    put2queue_andclear(datalist)
                i += 1
        if (datalist is not None and len(datalist) > 0):
            put2queue_andclear(datalist)
    loger.info("sum:"+str(sum))
    loger.info("broken_num:"+str(broken_num))

# 将数据集合放置队列，并清除
def put2queue_andclear(datalist):
    dbqueue.put(datalist)
    loger.info("put 2 data" + str(datalist))
    loger.info("put 2 queue" + str(len(datalist)))
    loger.info("put 2 queue sum" + str(sum))
    datalist = []
#根据目录获取种子路径列表
def get_tor_list_by_dir(torrdir):
    err_back_path = (torrdir +
                     os.path.sep +
                     TORR_ERROR_FILE)
    datalist = []
    sum = 0
    broken_num=0
    #get_oswalk_desc 获取文件倒序
    for dirpath, dirnames, filenames in os.walk(torrdir):
    # for dirpath, dirnames, filenames in fu.get_oswalk_desc(torrdir):
        i=0
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            #loger.info("=================================")
            #loger.info(portion)
            if portion[1] == ".torrent":
                sum+=1
                # loger.info("================torrent conteng=================" + '\r\n')
                # loger.info(torr)
                #种子文件小于1k说明可能是异常文件，需要重新下载
                if os.path.getsize(torr) < 1000:
                    #异常种子处理，写日志，转移到异常文件夹
                    move_error_torrent(torr, err_back_path)
                    continue
                else:
                    my_torrent=loadTorr_and_fixed(torrdir,torr,0)

                if my_torrent is not None:
                    hash = my_torrent.info_hash
                    tobj = [hash, torrdir, filename]
                    datalist.append(tobj)
                    if i == batchsize:
                        i = 0
                        put2queue_andclear(datalist)
                    i += 1
        if (datalist is not None and len(datalist) > 0):
            put2queue_andclear(datalist)
    loger.info("sum:"+str(sum))
    loger.info("broken_num:"+str(broken_num))

def mkdirs(path):
    if (not os.path.exists(path)):
        loger.info('mkdir:' + str(path))
        os.mkdir(path)

#根据路径名称，生成
def get_errordir_filename_from_fullpath(torrpath):
    file_path = Path(torrpath)
    # 获取文件名（含扩展名）
    file_name = file_path.name
    # 获取父目录路径
    error_path = file_path.parent.joinpath(TORR_ERROR_FILE)  # 输出:路径
    return file_name,error_path,file_path.parent


def comparefile(torrhcode, torrpath, torrfilename,
                dbhcode, dbpath, dbfilename):
    loger.info('---------------------------------')
    loger.info('comparefile  scanfile==> ' + torrhcode + '   ' + torrpath + torrfilename)
    loger.info('comparefile  dbdbfile==> ' + dbhcode + '   ' + dbpath + dbfilename)
    loger.info('---------------------------------')
    if (torrhcode == dbhcode):
        fpath = torrpath + os.path.sep + torrfilename
        dpath = dbpath + os.path.sep + dbfilename
        if fpath == dpath:  # 同一个文件 TODO
            loger.info('comparefile scan same file skip it!')
            # 不错处理，忽略
            return
        else:
            # 1.写日志
            msg = "扫描文件:" + fpath + Enter + "数据库文件:" + dpath + Enter
            loger.info('comparefile scan diff  file Res')
            loger.info(msg)
            # 2.处理路径不同的重复种子
            dup_torr_handle(torrhcode, torrpath, torrfilename, msg)

    else:  # bug
        loger.info("出现bug")
        # loger.info("出现bug")

DUP='duplicate'
DUP_DIRNAME= os.path.sep+DUP+ os.path.sep
Enter='\r\n'
#torrpath 种子原始文件路径
#新增文件夹，并写日志，打印
def writeDupLog(torrpath,msg):
    if( torrpath.endswith(DUP)):
        duplicateDir=torrpath
    else:
        duplicateDir = torrpath + DUP_DIRNAME
    writer =tlog.file_writer(duplicateDir, "dirtyData", True)
    writer.writelines("**********dirtyData   start***************" + '\r\n')
    # writer.writelines("扫描文件:" +filearry)
    # writer.writelines("数据库文件:" + dbarray)
    writer.writelines(msg+'\r\n')
    writer.writelines("**********dirtyData   done***************" + '\r\n')
    writer.close()


def clear_duplicate_torr():
    idlist=[]
    relist=dbtool.queryduplicatetor()
    if relist is not None and len(relist)>0:
        for res in relist:
            idlist.append(res[0])
            # [id, hcode, path, filename, time]
            # 1.文件迁移
            torrpath=res[2]+os.path.sep+res[3]
            #https://blog.csdn.net/zffustb/article/details/131236802
            moveduplicateTorr(torrpath)
            #2.查询主表，并生成日志
            #todo 先使用   SELECT * FROM duplicatetor d, torrents t where t.hcode=d.hcode;
        # 3. 删除记录
        delTag=dbtool.delDulicateTorrent(idlist)
        if delTag:
            loger.info("*************delDulicateTorrent*****************")
            loger.info(str(idlist))

    # 将重复文件移动至
def moveduplicateTorr(tfile):
    dir_path = os.path.dirname(tfile)
    filename = os.path.basename(tfile)
    dupilicatedir = dir_path + 'duplicate\\'
    mkdirs(dupilicatedir)
    shutil.move(tfile, dupilicatedir + filename)


if __name__ == '__main__':
    scanTorrentsIntoDB(r"D:\temp\0555\2022-03-01\0555\b55")