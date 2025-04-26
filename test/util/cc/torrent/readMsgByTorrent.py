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

array = ['【01axg.xyz】.jpg', '02AXG.XYZ.png', '03axg.XYZ.png', '8axg.xyz.png',
         '04axg.xyz.png', '05axg.xyz.png', '06axg.xyz.png',
         '( 1024网址PC端发布器 3.0 ).chm',
         '( 1024网址PC端发布器 20.chm',
         '( 1024社区手机网址发布器 3.1 ).apk',
         '( 1024社区手机网址发布器 3.0 ).apk',
         '( 1024社区手机网址发布器 2.0).apk',
         '( 扫码下载1024安卓APP_3.0 ).png',
         '( 扫码下载1024安卓APP_2.0 ).png',
        '(_1【av8.la】。原版无水印-网络热搜门事件，每日更新！.mhtml',
         'gc2048.com-最新国产日韩欧美新片合集发布.htm',
         'gc2048.com-(_2048免翻墙地址发布.htm',
         'gc2048.com-2022年国产汇总2048论坛.htm',
'sis百万国产原创作品.png',
         '(_1024手机发布器.apk',
         '(_1024手机版网址.png',
         '(_1024社区免翻墙网址.chm',
         '(_扫码下载1024手机网址发布器.png',
         '暗香阁地址发布器.CHM',
         '暗香阁最新地址.png',
         '暗香阁综合论坛.png',
         '【01axg.xyz】_副本.jpg',
         '获取最新地址邮箱，无需翻墙.txt',
         '免费资源实时更新.png',
         '(_1【av8.la】。原版无水印-网络热搜门事件，每日更新！.html',
         '抖淫短视频边看边赚钱的APP.url',
         '黑料社，第一手吃瓜APP.url',
         '解压错误请下载。原版无水印资源.txt', '.DS_Store',
'小黄片.mht',
'_性视界.chm',
'_性视界.html',
'_性视界.jpg',
'_性视界.mht',
'小黄片.chm',
'小黄片.html',
'小黄片.jpg',
'小黄片.mht',
'_尖叫视频.html',
'_尖叫视频.jpg',
'尖叫视频.chm',
'尖叫视频.mht',
'_萌萝社.chm',
'_萌萝社.html',
'_萌萝社.jpg',
'_萌萝社.mht',
'(  1024社区最新地址_3.0 ).htm',
'(  最新bt合集_3.0 ).html',
'( 1024网址PC端发布器 3.0 ).chm',
'( 扫码下载1024安卓APP_3.0 ).png',
'( 1024社区手机网址发布器 3.1 ).apk',
'( 1024网址PC端发布器 3.1 ).chm',
'( 扫码下载1024安卓APP_3.1 ).png',
'1024草榴社区t66y.com.jpg',
'18p2p by.txt',
'2048社区 每天更新 同步日韩.html',
'SEX169 论坛.url',
'SEX8.cc杏吧_性吧_sex8_杏吧有你春暖花开-.txt',
'WK綜合論壇 - WaiKeung.net.url',
'av狼永久地址.url',
'id16151274@SexInSex.net.txt',
'公仔箱論壇.url',
'桃花族论坛.url',
'比思永久地址.url',
'草榴最新地址.mht',
'duplicatedirtyData.txt'
         ]
def removeFiles(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'

    # prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath + "\\" + filename
                loger.info(absPath)
                os.remove(absPath)
            # torr = os.path.join(dirpath, filename)
            # absPath = dirpath + filename
            # if(absPath.endswith(prefix)):
            #     loger.info(absPath)


def getDulicateFiles():
    filepath = 'D:\\temp\\593254315050521\\'
    prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            absPath = dirpath + filename
            if(absPath.endswith(prefix)):
                loger.info(absPath)

def findTorrListByStr(strlist,path):
    if strlist is None:
        return
    else:
        for str in strlist:
            loger.info('*************************'+str+'查找开始*******************************')
            getTorrentByDetails(str,path)
            loger.info('*************************' + str + '查找结束*******************************')

#加载种子，如果种子错误或者内容为空，返回空
def loadTorr(torrpath):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return  my_torrent
    except BencodeDecodingError:
        loger.info("error " + torrpath)
        # slove_bencode_torr(torrpath)
        return None
    except IndexError:
        loger.info("error " + torrpath)
        return None
#加载种子，如果种子错误或者内容为空，返回空
#加载种子次数，如果查过一次就放弃
def loadTorr_and_fixTorr(torrpath,count):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return  my_torrent
    except BencodeDecodingError:
        count+=1
        loger.info("error " + torrpath)
        if(count<2 and os.path.getsize(torrpath)>1024):
            return slove_bencode_torr(torrpath)
        else:
            #直接move返回空

            return None
    except IndexError:
        loger.info("error " + torrpath)
        return None
# def rename(path):
#     for dirpath, dirnames, filenames in os.walk(path):
#         for filename in filenames:
#
#
#文件解析获取编码错误BencodeDecodingError，先进行去除结尾的\r\n
#c:\test.torrent==>
# 然后重新解析一次，再报错就不处理了
#torrfile
def slove_bencode_torr(torrfile):
    fix_torrent(torrfile)
    return loadTorr(torrfile)

def get_errordir_filename_from_fullpath(fullpath):
    file_path = Path(fullpath)
    # 获取文件名（含扩展名）
    file_name = file_path.name
    # 获取父目录路径
    error_path = file_path.parent.joinpath(TORR_ERROR_DIRNAME)  # 输出:路径
    return file_name,error_path,file_path.parent
def getTorrentByDetails(str,filepath):
    dirs = []
    # try:
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
                portion = os.path.splitext(filename)
                if portion[1] == ".torrent":
                    path = os.path.join(dirpath, filename)
                    # loger.info('torr=='+torr)
                    my_torrent = loadTorr(path)
                    if my_torrent is not None:
                        for torrfile in my_torrent.files:
                            # loger.info('name:'+torrfile.name)
                            if (torrfile.name.startswith(str)):
                                loger.info('t:==>' + path)
                                dirs.append(path)
                                # loger.info(my_torrent.total_size / len)
                                loger.info('str:==>' + str)
                                # loger.info(my_torrent.files)
                                break
# finally:
# loger.info('dirs',dirs)

def editXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix):
                loger.info('dirpath:'+dirpath)
                new = filename.replace(xunleisuffix, "")
                oldfile=filepath + os.sep + filename
                newfile=filepath + os.sep + new
                loger.info("修改前:" + oldfile)
                loger.info("修改后:" + newfile)
                os.renames(oldfile, newfile)

def clearXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix) or filename.endswith(fdmsuffix)\
                    or filename.endswith(btcomet_suffix):
                fullname=os.path.join(dirpath,filename)
                try:
                    loger.info('file: '+fullname)
                    os.remove(fullname)
                except UnicodeEncodeError:
                    # non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    # fullname=fullname.translate(non_bmp_map)
                    loger.info('full: ' + fullname)
                    os.remove(fullname)

'''
批量写子文件内容
'''
def writeTorrDetail(filepath):
    for i in os.listdir(filepath):
        path = filepath +  i+os.path.sep
        if os.path.isdir(path):
            loger.info("writeTorrDetail path====="+path)
            getTorrDetail(path)

#过滤大文件
#filterLen 过滤文件大小单位G
def filterBigfiles(torrpath,filterLen):
    torrBigFilePath = torrpath + 'big\\'
    mkdirs(torrBigFilePath)
    lenG=filterLen*1024*1024
    bigfiles = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                loger.info('torr==' + torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                fileSize=my_torrent.total_size
                loger.info('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr,torrBigFilePath+filename)
                    loger.info('大文件')
                    bigfiles.append(my_torrent.name)
    loger.info('bigfiles size:' + str(len(bigfiles)))
    loger.info('bigfiles:'+str(bigfiles))

#判断pdf是否存在，存在， 转移至新路径
def movePdf(oldpdfpath,tarpath):
    oldpdf=nameTorr2Pdf(oldpdfpath)
    if os.path.isfile(oldpdf):
        #存在pdf 转移
        pdf_name=os.path.basename(oldpdf)
        shutil.move(oldpdf,tarpath+os.sep+pdf_name)
# 将种子路径转化为pdf路径
def nameTorr2Pdf(torrfullpath):
    if(torrfullpath  is None):
        return
    else:

        path ,ext=os.path.splitext(torrfullpath)
        pdfpath=path+'.pdf'
        return pdfpath
# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
#1.scan torr path,get dict  key 种子名称   val 种子路径
#2. find same move

###Q1. 需要给我hcode处理，单文件也需要处理
def filterDownFiles(torrpath,filepath,subDirName):
    # for dirpath, dirnames, filenames in os.walk(filepath):
    #     for dirname in dirnames:
    #         loger.info('dir:   ' +dirname)
    dirList=[]
    #搜集已下载文件列表 TODO 增加单文件支持
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
            dirList.append(filename)
            loger.info('dirname   '+filename)
        # else:
        #     portion = os.path.splitext(filename)
        #     loger.info('00000  ' + portion[0])
        #     dirList.append(portion[0])
    files =os.listdir(filepath)
    # clearMacConfigFile(dirList)
    # 根据种子路径生成词典  key 种子名称   val 种子路径 todo  key修改为hcode
    torrDict=geneTorrentDic(torrpath)
    torrlist=torrDict.keys()

    #loger.info('dict===='+str(torrDict))
    reset=set(dirList)&set(torrlist)
    #loger.info('dirList'+str(dirList))
    #loger.info('torrlist' + str(torrlist))
    rslist=list(reset)
    loger.info("  =====================  ")
    loger.info(rslist)

    torrDonePath = torrpath+os.path.sep+subDirName+ os.path.sep
    mkdirs(torrDonePath)

    finishFilePath = filepath+os.path.sep+subDirName+ os.path.sep
    mkdirs(finishFilePath)

    for samefile in rslist:
        loger.info(" ****   ")
        #loger.info(torrDict[samefile])
        loger.info(os.path.basename(torrDict[samefile]))
        newTorrFile = torrDonePath+os.path.basename(torrDict[samefile])

        finishFile = finishFilePath+samefile
        #已经移动了，删除原有的 并打印提示信息
        if os.path.isfile(newTorrFile):
            loger.error("****************有已经下载过得文件******************")
            loger.error("****************种子文件**************************")
            loger.error(newTorrFile)
            loger.error("****************重复文件**************************")
            loger.error(str(filepath+ os.path.sep+samefile)+"   "+str(finishFile))
            os.remove(torrDict[samefile])
        else: #移动种子
            loger.debug("********原种子地址*************")
            loger.debug(torrDict[samefile])
            loger.debug("********新种子地址*************")
            loger.debug(newTorrFile)
            shutil.move(torrDict[samefile],newTorrFile)

        #文件已经下载过了，重新命名复制
        if os.path.exists(finishFile):
            finishFile=finishFile+'_new'
            # base, ext = os.path.splitext(finishFile)
            # finishFile = f"{base}_new{ext}"  # 修改文件名以避免冲突
            mkdirs(finishFile)
        #移动完成文件
        shutil.move(filepath+ os.path.sep+samefile,finishFile)
        loger.debug("********原文件地址*************")
        loger.debug(filepath+ os.path.sep+samefile)
        loger.debug("********新文件地址*************")
        loger.debug(finishFile)
        # 判断pdf是否存在，存在， 转移至新路径
        movePdf(torrDict[samefile], finishFile)

    loger.info('移动种子文件：'+str(len(rslist)))

    #计算文件的大小，下载比例
def countFile(torrpath,filepath):
    # 搜集下载中文件列表
    namelist=[]
    sizelist=[]
    for filename in os.listdir(filepath):
        namelist.append(filename)
        path = os.path.join(filepath, filename)
        sizelist.append(cal_size(path))
    fileDict = dict(zip(namelist,sizelist))

    torrDict = geneTorrentDic(torrpath)
    #todo


#根据种子路径生成词典  key 种子名称   val 种子路径
#原则上不会有重复，毕竟文件名不可能重复
def geneTorrentDic(torrpath):
    torrlist = []
    torrNamelist = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                torrlist.append(my_torrent.name)
                torrNamelist.append(torr)
    torrDict = dict(zip(torrlist, torrNamelist))
    return torrDict

    #计算文件夹file_path的大小
def cal_size(self,file_path):
    sum = 0
    try:
        os.listdir(file_path)
    except:
        pass
    else:
        for f in os.listdir(file_path):
            abspath=os.path.join(file_path,f)
            if os.path.isfile(abspath):
                portion = os.path.splitext(abspath)
                if portion[1] != ".xltd":
                    sum += os.path.getsize(abspath)
            elif os.path.isdir(abspath):
                sum += self.cal_size(abspath)
    return sum

def mkdirs(path):
    if (not os.path.exists(path)):
        loger.info('mkdir:' + str(path))
        os.mkdir(path)

def getTorrDetail(filepath):
    filepath=filepath+os.path.sep
    dirname = os.path.dirname(filepath)
    #文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath=filepath+basename+'.txt'
    loger.info( 'basename==>'+basename)
    loger.info('dirname==>'+dirname)
    loger.info('txtfile===>'+txtpath)

    txtfile=open(txtpath,'w+',encoding='utf-8')

    len=1024*1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        # 跳过指定目录（修改dirnames列表）
        if TORR_ERROR_DIRNAME in dirnames:
            dirnames.remove(TORR_ERROR_DIRNAME)  # 从待遍历列表中移除，避免进入该目录

        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("================================="+'\r')
            # txtfile.writelines(portion)
            # loger.info("=================================")
            # loger.info(portion)
            # 如果后缀是.xltd
            # if portion[1] == ".xltd":
            #     loger.info("need change")
            #     newnamee=portion[0].replace('.bt','')
            #     os.renames(filepath+portion[0]+portion[1],filepath+newnamee)
            if portion[1] == ".torrent":
                # loger.info(torr)
                txtfile.writelines(torr+'\r')
                my_torrent = loadTorr_and_fixTorr(torr,0)
                if my_torrent is None or os.path.getsize(torr)<500:
                    continue
                tlen=my_torrent.total_size / len
                txtfile.writelines(str(tlen)+'\r')
                txtfile.writelines(str(my_torrent.files) + '\r\n')
                txtfile.writelines(my_torrent.info_hash+'\r')

                # loger.info(my_torrent.total_size / len)
                # loger.info(my_torrent.comment)
                loger.info(portion[0]  +'          '+ my_torrent.name)
                for torrfile in my_torrent.files:
                    if(torrfile.length>100*len):
                        txtfile.writelines(str(torrfile)+'\r')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()
#数据库插入缓冲池
dbqueue = queue.Queue()
#有些种子文件，结尾有\r\n导致，解析错误，扫描一遍，将有错误的文件重新生成一遍
#torrdir  c:\\ttt
def pre_slove_error_torrs(torrdir):
    # err_back_path=torrdir+'\errorbak'

    # if not os.path.exists(err_back_path):
    #     os.makedirs(err_back_path)
    for filename in os.listdir(torrdir):
        file_path = os.path.join(torrdir, filename)

        portion = os.path.splitext(filename)
        if portion[1] == ".torrent":
            fix_torrent(file_path)

    # zip_and_clear(torrdir)

#修复种子数据内容，通常为结尾\r\n造成读取异常
#file_path 全路径
#filename 文件名称，含后缀
#err_back_path 异常文件夹
def fix_torrent(file_path):
    filename, err_back_path,dirpath=get_errordir_filename_from_fullpath(file_path)
    # 检查是否为文件
    if os.path.isfile(file_path) and file_path.endswith('.torrent'):

        if os.path.getsize(file_path)>1000:
            # 读取文件内容
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # 检查文件是否以 \r\n 结尾
            if file_content.endswith(b'\r\n'):
                mkdirs(err_back_path)
                txt = log(str(dirpath), 'error', True)
                # 备份文件到 error 文件夹
                backup_path = os.path.join(err_back_path, filename)
                # if not os.path.exists(backup_path):
                    # shutil.copy(file_path, backup_path)
                # 去除 \r\n 后重新生成源文件
                txt.writelines("************************待查找************  " + '\r\n')
                txt.writelines(file_path+" is deleteed \\r\\n" + '\r\n')
                txt.close()
                new_content = file_content[:-2]
                with open(file_path, 'wb') as file:
                    file.write(new_content)
        else:
            mkdirs(err_back_path)
            txt = log(str(dirpath), 'error', True)
            txt.writelines("************************待查找************  " + '\r\n')
            txt.writelines(file_path + " is error ，need redownload" + '\r\n')
            txt.close()
            shutil.copy(file_path, err_back_path)




#将异常种子，进行转移压缩备份
def zip_and_clear(torrdir):
    err_back_path = torrdir +os.sep+ TORR_ERROR_DIRNAME
    err_back_zip = torrdir + '\errorbak.zip'
    # 压缩错误文件夹
    with zipfile.ZipFile(err_back_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(err_back_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, start=err_back_path))

    # 删除错误文件夹
    # shutil.rmtree(err_back_path)


#根据目录获取种子路径列表
def getTorListByDir(torrdir):
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
                    dbqueue.put(datalist)
                    loger.info("put 2 data" + str(datalist))
                    loger.info("put 2 queue" + str(len(datalist)))
                    loger.info("put 2 queue sum" + str(sum))
                    datalist =[]
                i += 1
        if (datalist is not None and len(datalist) > 0):
            dbqueue.put(datalist)
            loger.info("put 2 data" + str(datalist))
            loger.info("put 2 queue" + str(len(datalist)))
            loger.info("put 2 queue sum" + str(sum))
            datalist=[]
            # loger.info("put 2 queue")
            # loger.info("put 2 queue" + str(datalist))
    loger.info("sum:"+str(sum))
    loger.info("broken_num:"+str(broken_num))


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

#生成map对象，key 为hash val 为#[hash, path, filename]
def build_torrObj_dic(datalist):
    dict = {}
    if datalist is not None and len(datalist)>0:
        for data in datalist:
            dict[data[0]]=data
    return  dict
#torrlist 重复数据清理
def clearDupTorrHandler(datalist,hashs):
    hashset=set(hashs)
    rslist=copy.deepcopy(datalist)
    if(len(hashset)!=len(hashs)):
        st= set()
        #表示该列表有重复hcode的数据
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
            addDupData(dup[0], dup[1], dup[2], msg)
        return rslist,list(st)
    else:
        return datalist,hashs


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
            # todo nothing
            return
        else:
            # 1.写日志
            msg = "扫描文件:" + fpath + Enter + "数据库文件:" + dpath + Enter
            loger.info('comparefile scan diff  file Res')
            loger.info(msg)

            addDupData(torrhcode, torrpath, torrfilename, msg)
            # todo move the file
            # writeDupLog(torrpath, msg)
            # #2.move 种子至重复文件夹
            # newtorrpath = torrpath + DUP_DIRNAME#该变量为新路径，包含配置的重复文件夹
            # mkdirs(newtorrpath)
            # if os.path.isfile(fpath):
            #     loger.info('move'+fpath+'to '+newtorrpath + torrfilename)
            #     shutil.move(fpath, newtorrpath + torrfilename)
            # rs=dbtool.querydupTorrByHcodeAndFnAndPath(torrhcode,torrfilename,torrpath)
            # if rs is not None or len(rs)>0:
            #
            #     #重复路径存在
            #     return
            # else:#重复记录表不存在该记录，直接插入
            #     #记录新路径，并存放
            #     # loger.info(torrhcode)
            #     # loger.info( newtorrpath)
            #     # loger.info( torrfilename)
            #     dbtool.recorderDulicateTorrent(torrhcode,newtorrpath,torrfilename)

            # 2.make dupdir and move file
    else:  # bug
        loger.info("出现bug")
        # loger.info("出现bug")


# 写日志，插入torrentdup表中，将重复种子移动到duplicate文件夹种
# torrent表or Torrentdup存在,则不做处理
def addDupData(torrhcode, torrpath, torrfilename, msg):
    loger.debug('addDupData ' + torrhcode + '  ' + torrpath + '  ' + torrfilename)
    torr_filepath = torrpath + os.path.sep + torrfilename
    # msg = "重复文件:" +torrhcode+ torrpath+os.path.sep + torrfilename
    # 1.写日志
    writeDupLog(torrpath, msg)
    # 2.move 种子至重复文件夹
    newtorrpath = torrpath  # 该变量为新路径，包含配置的重复文件夹

    if os.path.isfile(torr_filepath) and not torrpath.endswith(DUP):  # 文件夹已经是重复文件夹名称了，不做处理
        newtorrpath = torrpath + DUP_DIRNAME
        mkdirs(newtorrpath)
        loger.info('move  ' + torr_filepath + Enter + 'to  ' + newtorrpath + torrfilename)
        shutil.move(torr_filepath, newtorrpath + torrfilename)

    rs = dbtool.querydupTorrByHcodeAndFnAndPath(torrhcode, torrfilename, torrpath)

    if rs is not None and len(rs) > 0:
        # 存在需要对比路径，如果路径不同，需要edit ，因为之前move了
        loger.debug('重复记录已存在，不做处理' + torrhcode + '  ' + newtorrpath + '  ' + torrfilename)
        # 重复路径存在
        return
    else:  # 重复记录表不存在该记录，直接插入
        loger.debug('重复记录插入' + torrhcode + '  ' + newtorrpath + '  ' + torrfilename)
        dbtool.recorderDulicateTorrent(torrhcode, newtorrpath, torrfilename)


#dblist 查询数据库返回的重复数据
#datalist待过滤数据集，过滤后插入数据库
#return 返回待插入的数据集
def filterDirtyData(datadict ,dblist):
    if dblist is not None and len(dblist) > 0:
        data_hashlist=datadict.keys()
        rslist=list(datadict.values())
        #查询每条数据库记录
        for dbrs in dblist:
            # [id, hcode, path, filename, time]
            hcode=dbrs[1]

            if hcode in data_hashlist:#做分支，是否转移种子文件
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
        loger.info("filterDirtyData重新插入数据 清理前数据条数" + str(len(data_hashlist))+'  清理后数据条数'+str(len(rslist)))
        #loger.info("filterDirtyData重新插入数据datalist"+str(data_hashlist))
        return rslist
    else:
        return  list(datadict.values())


def gethashlist(datalist):
    hashs = []
    if datalist is not None or len(datalist)>0:
        for arr in datalist:
            # [hash, path, filename]
            hashs.append(arr[0])
    return hashs


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
    writer = log(duplicateDir, "dirtyData", True)
    writer.writelines("**********dirtyData   start***************" + '\r\n')
    # writer.writelines("扫描文件:" +filearry)
    # writer.writelines("数据库文件:" + dbarray)
    writer.writelines(msg+'\r\n')
    writer.writelines("**********dirtyData   done***************" + '\r\n')
    writer.close()



#判断种子文件是否存在
#如果两张表都不存在，只额吉插入torrentdup表中
#torrent表or Torrentdup存在,则不做处理
#返回结果True表示
            #todo move the file
            # writeDupLog(torrpath, msg)
            # #2.move 种子至重复文件夹
            # newtorrpath = torrpath + DUP_DIRNAME#该变量为新路径，包含配置的重复文件夹
            # mkdirs(newtorrpath)
            # if os.path.isfile(fpath):
            #     loger.info('move'+fpath+'to '+newtorrpath + torrfilename)
            #     shutil.move(fpath, newtorrpath + torrfilename)
            # rs=dbtool.querydupTorrByHcodeAndFnAndPath(torrhcode,torrfilename,torrpath)
            # if rs is not None or len(rs)>0:
            #
            #     #重复路径存在
            #     return
            # else:#重复记录表不存在该记录，直接插入
            #     #记录新路径，并存放
            #     # loger.info(torrhcode)
            #     # loger.info( newtorrpath)
            #     # loger.info( torrfilename)
            #     dbtool.recorderDulicateTorrent(torrhcode,newtorrpath,torrfilename)

            #2.make dupdir and move file


    ####
    #重复文件过滤，将db中重复的文件进行后置处理，
    #路径 hcode相同，则忽略
    #路径不同，则打算torrent_dup表中
    #在存放dup之前，进行一次过滤，重复忽略，不重复则插入
    # dbrs is dbTorFile
    #    format    [id ,hcode,path,filename,time]
    # tar is scan file
    # [hash, path, filename]
    # @return True 表示同源文件可以忽略
    # @return False 表示不同文件需要处理
    # ###
    #deprate
# def compareTorfile(tar,dbrs):
#     # dbrs is dbTorFile
#     # [id ,hcode,path,filename,time]
#     # tar is scan file
#     # [hash, path, filename]
#     if tar[0]==dbrs[1]:
#         tarfilepath=tar[1]+tar[2]
#         dbtfilepath=dbrs[2]+dbrs[3]
#         #路径相同，表示同一个文件
#         if tarfilepath==dbtfilepath:
#             return  True
#         else:
#             duplicateDir = tar[1] + '\\duplicate\\'
#             writer = log(duplicateDir, "dirtyData", True)
#             writer.writelines("**********dirtyData   start***************" + '\r\n')
#             writer.writelines("扫描文件:" + str(tar))
#             writer.writelines("数据库文件:" + str(dbrs))
#             writer.writelines("**********dirtyData   done***************" + '\r\n')
#             writer.close()
#             #移动文件
#             shutil.move(tar[1]+'/'+tar[2],duplicateDir+tar[2])
#
#             #插入数据库  也有可能重复
#             dbtool.recorderDulicateTorrent(tar[0],tar[1],tar[2])
#
#             return  False

#path 待扫描生成唯一hashcode的种子路径
def scan_torr_get_hashlist(path,txt):
    tarlist = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = Torrent.from_file(torr)
                hashcode=my_torrent.info_hash.lower()
                if txt is not None:
                    txt.writelines("hashcode  " + hashcode + '\r\n')
                tarlist.append(hashcode)

def findTorrentByHashcode(srctorrpath,tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcode',False)
    #遍历待查找的种子，生成集合
    tarlist=scan_torr_get_hashlist(tartorrpath,txt)
    txt.writelines("************************待查找************  " + '\r\n')
    srclist=scan_torr_get_hashlist(srctorrpath,None)

    dupdata = [dup for dup in tarlist if dup in srclist]
    for dirpath, dirnames, filenames in os.walk(srctorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                srctorrpath = os.path.join(dirpath, filename)
                srctorrent = Torrent.from_file(srctorrpath)
                srccode=srctorrent.info_hash.lower()
                if srccode in tarlist:
                    txt.writelines("hashcode  " + srccode + '\r\n')
                    txt.writelines("dirpath  " + dirpath + '\r\n')
                    txt.writelines("filename  " + filename + '\r\n')


    txt.close()

#srctorrpath  种子集散地
# tartorrpath  待查找种子
def findTorrentByHashcodeInDir(srctorrpath,tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcodeInDir',False)
    tarlist=[]
    #遍历待查找的种子，生成集合
    txt.writelines("************************待查找************  " + '\r\n')
    for dirpath, dirnames, filenames in os.walk(tartorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = Torrent.from_file(torr)
                hashcode=my_torrent.info_hash.lower()
                txt.writelines("torr  " + torr + '\r\n')
                txt.writelines("hashcode  " + hashcode + '\r\n')
                tarlist.append(hashcode)
    txt.writelines("************************待查找************  " + '\r\n')

    for dirpath, dirnames, filenames in os.walk(srctorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                srctorrpath = os.path.join(dirpath, filename)
                try:
                    srctorrent = Torrent.from_file(srctorrpath)
                    srccode = srctorrent.info_hash.lower()
                    if srccode in tarlist:
                        txt.writelines("hashcode  " + srccode + '\r\n')
                        txt.writelines("dirpath  " + dirpath + '\r\n')
                        txt.writelines("filename  " + filename + '\r\n')
                except AttributeError:
                    loger.info('error file ' + srctorrpath)
                    continue
                except BencodeDecodingError:
                    # 种子下载失败了
                    loger.info('error file ' + srctorrpath)
                    continue
                except IndexError:
                    loger.info('error file ' + srctorrpath)
                    continue




    txt.close()

def log(filepath, name,append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]

    loger.info('basename==>' + basename)
    loger.info('dirname==>' + dirname)
    txtpath = filepath +os.sep+ basename + name + '.txt'
    loger.info('txtfile===>' + txtpath)
    if(append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile

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

def clearduplicateTorr():
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
    #
#将重复文件移动至
def moveduplicateTorr(tfile):
    dir_path = os.path.dirname(tfile)
    filename=os.path.basename(tfile)
    dupilicatedir=dir_path+'duplicate\\'
    mkdirs(dupilicatedir)
    shutil.move(tfile,dupilicatedir+filename)


#扫描half文件夹下所有未下载文件，生成对应得种子文件
# downdir 下载目录，包含了种子文件的头目录
# def  genhalfTorrent(downdir):
#     for root, dirs, files_list in os.walk(downdir):
#         for file_name in files_list:
#             if file_name.endswith('torrent') and not  str(file_name).startswith(HALF_NAME_PREFIX):
#                 tfile=os.path.join(root, file_name)
#                 loger.info("tfile:"+tfile)
#                 loger.info("root:"+root)
#                 genNewTorr(tfile,root)
#
#
#
#
#     #tfiles 种子里的文件，
#     #downdir 下载目录，包含了种子文件的头目录
#     #todo  写日志
# def genNewTorr(tfile,downdir):
#     txtfile = log(downdir, 'genNewTorr', False)
#     txtfile.writelines('tfile' + tfile + '\r\n')
#     txtfile.writelines('downdir' + downdir + '\r\n')
#     my_torrent = Torrent.from_file(tfile)
#     downloadmap = scanDownloadingFiles(downdir, txtfile)
#     downloadfilelist = list(downloadmap.keys())#'204V\\1 (1).mp4'
#
#     # for i in range(len(downloadfilelist)):
#     #     downloadfilelist[i]=downloadfilelist[i].replace(r'\\\\',ros.path.sep)
#     loger.info('downloadfilelist:'+str(downloadfilelist))
#     my_torrent.files
#     tfiles=my_torrent.files
#     for file in tfiles:  # 遍历种子文件   #TorrentFile(name='134\\204V\\1 (1).mp4', length=13583369)
#         ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
#         # tfilename = file.name.replace(os.path.sep, '')
#         # loger.info('tfilename'+tfilename)
#
#         subpath = file.name.split(os.path.sep, 1)[1]#截取359目录，由于可能会改名，所以
#         # if(subpath.endswith('1 (1).mp4')):  #test code
#         #     loger.info('')
#         if subpath.__contains__(os.path.sep):
#             subname = subpath.split(os.path.sep, 1)[1]
#         else:
#             subname=subpath
#         #subpath \尖叫视频.mht
#         # subpath = subpath.replace(os.path.sep, '\\\\')
#         loger.info('subpath :'+str(subpath))
#
#         if subname.__contains__('如果您看到此文件，请升级到BitComet'):
#             loger.info(subname)
#         elif subpath in downloadfilelist:
#
#             txtfile.writelines("subpath :" + subpath)
#             tfiles.remove(TorrentFile(file.name,file.length))
#     txtfile.close()
#     tf=tfile.replace(downdir ,'')
#     tf=downdir+os.path.sep+HALF_NAME_PREFIX+tf[2:]
#     my_torrent.files=tfiles
#     my_torrent.to_file(tf)
#     loger.info('gen file '+tf)



#用来扫描half文件夹下所有待扫描的半下载文件
# downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def countHalfFiles(downdir,deltag):
    for root, dirs, files_list in os.walk(downdir):
        for file_name in files_list:
            if file_name.endswith('torrent') and not  str(file_name).startswith(HALF_NAME_PREFIX):
                tfile=os.path.join(root, file_name)
                loger.info("tfile:"+tfile)
                loger.info("root:"+root)
                comparefiles(tfile,root,deltag)

### downdir 下载目录，包含了种子文件的头目录
### 日志文件
    # deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def scanDownloadingFiles(downdir,deltag):
    downloadmap = {}
    for dirpath, dirnames, filenames in os.walk(downdir):
        loger.debug('dirpath'+dirpath + '\r\n')
        # loger.info('dirpath'+dirpath)
        # loger.info('dirnames' + dirnames)
        for filename in filenames:

            portion = os.path.splitext(filename)
            if deltag and filename.endswith(xunleisuffix):
                fullname = os.path.join(dirpath, filename)
                loger.debug("del path:" + fullname)
                os.remove(fullname)
            elif portion[1] != ".bt":#处理待下载文件，
                fullname= os.path.join(dirpath, filename)
                fsize=os.path.getsize(fullname)
                #loger.info("full path:"+fullname)
                # fullname=os.path.join(dirpath, ' '+filename)#torrent的file会有空格， 很奇怪
                torrfilepath=fullname.replace(downdir ,'')
                if str(torrfilepath).startswith(os.path.sep):#fix py版本兼容性问题
                    torrfilepath= torrfilepath[1:]
                #txtfile.writelines("download :" + torrfilepath+ '\r\n')
                #loger.info("size"+str(round(fsize/m,2))+'mb')
                downloadmap.setdefault(torrfilepath,fsize)#生成文件列表

    return downloadmap
xunleisuffix = '.bt.xltd'
fdmsuffix='.fdmdownload'
btcomet_suffix='.bc!'


dlcheck=DownLoadCheck()
# dlcheck.merge_blacklists(r".", "bl.json",False)
blacklist=dlcheck.load_blacklist(r"bl.json")
    #tfiles 种子里的文件，
    #downdir 下载目录，包含了种子文件的头目录
    # deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
    # todo  写日志
def comparefiles(tfile, downdir, deltag):
    # txtfile = log(downdir, 'comparefiles',False)
    loger.debug('tfile' + tfile + '\r\n')
    loger.debug('downdir' + downdir + '\r\n')
    loger.debug('downdir' + downdir)
    torrentmap = {}
    my_torrent = Torrent.from_file(tfile)


    for file in my_torrent.files:  # 遍历种子文件
        ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
        tfilename = file.name.replace('\\\\', os.path.sep)


        # loger.info('tfilename'+tfilename)
        #截取359目录，由于可能会改名，所以
        file_array=tfilename.split(os.path.sep, 1)
        if(len(file_array)==1):
            print('len1  tfilename==>'+tfilename)
            continue
        else:
            subpath = file_array[1]

        if subpath.__contains__(os.path.sep):
            subname = os.path.basename(subpath)
        else:
            subname=subpath
        #subpath \尖叫视频.mht
        #loger.info('subpath'+str(subpath))
        if subname in blacklist:
            continue
        if subname not in array:
            if subname.__contains__('如果您看到此文件，请升级到BitComet'):
                loger.info(subname)
            else:
                loger.debug("subpath :" + subpath)
                torrentmap.setdefault(subpath, file.length)
        ## 待增加过滤无用文件实现




    downloadmap=scanDownloadingFiles(downdir, deltag)
    m=1024*1024

    #loger.info(tfilename)
    #loger.info(str(file))
    downloadfilelist = list(downloadmap.keys())
    tfiellist=list(torrentmap.keys())
    #txtfile.writelines(str(tfiellist))
    loger.debug('*************************************************')
    loger.debug('downloadfilelist'+str(len(downloadfilelist))+'   '+ '\r\n')#+str(downloadfilelist)
    # for dfile in downloadfilelist:
    #loger.info('tfiellist bf' + str(len(tfiellist)) + '   ' + str(tfiellist))
    # for cleanfile in downloadfilelist:
    tfiellist=getUndownFileList(tfiellist,downloadfilelist)
    #     if cleanfile in tfiellist:
    #         tfiellist.remove(cleanfile)
    #loger.info('tfiellist af' + str(len(tfiellist)) + '   ' + str(tfiellist))
    downloadfilesize=0
    loger.debug("********************v1.0 已下载文件个数" + str(len(downloadfilelist)) + "个***************************" + '\r\n')
    loger.debug("********************v1.0 待下载文件列表"+ str(len(tfiellist))+"个***************************"+ '\r\n')
    if tfiellist is None or len(tfiellist)==0:
        return
    #未完成的文件列表，新建文件打印
    else:
        undone_file = log(""+downdir, '--undone', False)
        tfiellist=set(tfiellist)
        tfiellist_namelist = list()
        for needdownfile in tfiellist:
            tfsize=torrentmap.get(needdownfile)
            downloadfilesize+=tfsize
            tfsize =round(tfsize / m, 2)
            fname=os.path.basename(needdownfile)
            tfiellist_namelist.append(fname)
            undone_file.writelines("\""+fname+ "\","+'\r\n')
            # txtfile.writelines('size:'+str(tfsize)+"mb"+ '\r\n')
        undone_file.writelines('总占用空间":'+str(round(downloadfilesize / m, 2))+"mb"+ '\r\n')
        undone_file.close()
        dlcheck.gen_blacklist(tfiellist_namelist,None)
#tfiles  种子文件列表
# downedfiles  已下载文件列表
def getUndownFileList(tfiles,downedfiles):
    tmap={}#key 去除了路径中的所有空格， val原路径
    for tf in tfiles:
        ctf=tf.replace(" ","")
        tmap.setdefault(ctf,tf)
    tflist=tmap.keys()
    dmap={}
    for df in downedfiles:
        cdf=df.replace(" ","")
        dmap.setdefault(cdf,df)
    dflist=dmap.keys()
    for dfile in dflist:
        if dfile in tflist:
            tmap.pop(dfile)

    return  tmap.values()

# def test():
#     list1=[[1,2,3],[45,6,7],[8,65,44]]
#     list2=[2,33,44,55,66]
#     for l in list1:
#         if l[1] in list2:
#             list1.remove(l)
#     loger.info("list1"+str(list1))
if __name__ == '__main__':
    # test()
    # clearXunleiFile("D:\\temp\\")
    #loger.info('AD28E358EE8BF4C0FF00A53232C7BCA2407FA28A'.lower())
    # strlist=['[av8.la]HJ220517-10',
    #          '91大神FSG最新力作妈咪介绍新来的外围兼职萝莉女小团团的网红脸蛋 生活照1080P高清版',
    #          '【极品外围 性爱泄密】约啪高端外围美女各种私拍啪啪流出 操出高潮 爽出天际 完美露脸 高清私拍132P 高清720P版']
    # findTorrListByStr(strlist,r'D:\temp\0555\2022-03-01\0555')
    # findTorrListByStr(strlist, 'D:\\temp\\0555\\2022-03-01\\0555\\b20\errfiles\\')
    # countHalfFiles(r'G:\down\0555\b38\un\y\count-1', False)
    #getTorrDetail(r'D:\temp\0555\2022-03-01\0555\b54')
    #getTorrDetail(r'D:\temp\0555\2022-03-01\0555\b54\errfiles')
    # pre_slove_error_torrs(r'D:\temp\0555\2022-03-01\0555\b52\errfiles')
    #os._exit(0)
    # # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b30\\")
    # # os._exit(0)
    #
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b31', r'G:\down\0555\b31\un', 'y')
    # # filterDownFiles(r'D:\t7\2022-03-01\0555\b32', r'G:\down\0555\b32\un', 'y')
    # # filterDownFiles(r'D:\t7\2022-03-01\0555\b33', r'G:\down\0555\b33\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b34', r'G:\down\0555\b34\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b35', r'G:\down\0555\b35\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b36', r'G:\down\0555\b36\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b37', r'G:\down\0555\b37\un', 'y')
    # os._exit(0)
    # countHalfFiles(r'D:\temp\112\2', False)
    # os._exit(0)
    #getTorrDetail(r'D:\temp\0555\2022-03-01\43')
    scanTorrentsIntoDB(r'D:\temp\0555\2022-03-01\0333')
    #os._exit(0)
    #
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b31', r'G:\down\0555\b31\un', 'y')
    # #filterDownFiles(r'D:\t7\2022-03-01\0555\b32', r'G:\down\0555\b32\un', 'y')
    # #filterDownFiles(r'D:\t7\2022-03-01\0555\b33', r'G:\down\0555\b33\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b34', r'G:\down\0555\b34\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b35', r'G:\down\0555\b35\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b36', r'G:\down\0555\b36\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b37', r'G:\down\0555\b37\un', 'y')
    # os._exit(0)

    #G:\down\0555\others\un
    #F:\down\0555\other
    #findTorrentByHashcodeInDir(r"D:\temp\0555\2022-03-01",r"D:\temp\0555\tttt")

    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b25\\")
    #scanTorrentsIntoDB(r"D:\temp\0555\2022-03-01\0555\b54")

    # genhalfTorrent('D:\\temp\\chachong\\')
    #filterDownFiles(r'D:\temp\b31', r'D:\temp\sp', 'y')
    # writeTorrDetail('D:\\360Downloads\\1228\\')
    #os._exit(0)




    # path = r'D:\temp\0555\2022-03-01\0555\b54'
# path=r'D:\temp\b31y'
# removeFiles(path)
#truncatetable()
    # scanTorrentsIntoDB(path)

#removeFiles('f:\\')
# removeFiles('g:\\')
# removeFiles('h:\\')

   # removeFiles('E:\\PDF\\')
    #removeFiles('G:\\CC\\BOOKS\\')

    #scanTorrentsIntoDB("C:\\Users\\Administrator\\Downloads\\best\\")

    #scanTorrentsIntoDB("D:\\temp\\0555\\t\\0555\\b37\\")
    # tormd5("C:\\Users\\Administrator\\Downloads\\best\\推特网红大屁股骚货kbamspbam，怀孕了还能挺着个大肚子拍照拍视频挣钱，太敬业了，奶头变黑 但白虎粉穴依然粉嫩.torrent")
    #
    # getDulicateFiles()


    #getTorrDetail('D:\\360Downloads\\1228\\')
    # writeTorrDetail('D:\\temp\\1228\\')
    #filterBigfiles('D:\\360Downloads\\test\\', 1000)

    # getTorrDetail('D:\\temp\\593254315050521\\1210-best\\1\\')

    #getTorrentByDetails('','D:\\temp\\0555\\2022-03-01\\0555\\')

    # for i in range(51):
    #     dirpath='D:\\temp\\593254315050521\\alltorr\\'+str(i)+os.path.sep+str(i)+'\\y'
    #     if(os.path.isdir(dirpath)):
    #         # loger.info('D is '+dirpath)
    #         getTorrentByDetails('给哥哥买了新工具',dirpath )

# # Reading and modifying an existing file.
# my_torrent = Torrent.from_file('/home/idle/some.torrent')
# my_torrent.total_size  # Total files size in bytes.
# my_torrent.magnet_link  # Magnet link for you.
# my_torrent.comment = 'Your torrents are mine.'  # Set a comment.
# my_torrent.to_file()  # Save changes.
#
# # Or we can create a new torrent from a directory.
# new_torrent = Torrent.create_from('/home/idle/my_stuff/')  # or it could have been a single file
# new_torrent.announce_urls = 'udp://tracker.openbittorrent.com:80'
# new_torrent.to_file('/home/idle/another.torrent')
#
# with open('D:\\temp\\test.txt') as f:
#     for line in f.readlines()  :##readlines(),函数把所有的行都读取进来；
#         urk = line.strip(  )##删除行后的换行符，img_file 就是每行的内容啦
#         webbrowser.open(urk)
