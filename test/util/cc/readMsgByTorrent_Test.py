from torrentool.api import Torrent
# from torrentool.api import TorrentFile
from torrentool.exceptions import BencodeDecodingError
import os
import shutil
# import mysqlTemplate as dbtool
import queue, threading
import loggerTemplate

loger = loggerTemplate.log

HALF_NAME_PREFIX = 'HALF-'
logpath = 'D:\\temp\\0555\\'

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
    prefix = '(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            absPath = dirpath + filename
            if (absPath.endswith(prefix)):
                loger.info(absPath)


def findTorrListByStr(strlist, path):
    if strlist is None:
        return
    else:
        for str in strlist:
            loger.info('*************************' + str + '查找开始*******************************')
            getTorrentByDetails(str, path)
            loger.info('*************************' + str + '查找结束*******************************')


# 加载种子，如果种子错误或者内容为空，返回空
def loadTorr(torrpath):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return my_torrent
    except BencodeDecodingError:
        loger.info("error " + torrpath)
    except IndexError:
        loger.info("error " + torrpath)
    return None


# def rename(path):
#     for dirpath, dirnames, filenames in os.walk(path):
#         for filename in filenames:
#
#


def getTorrentByDetails(str, filepath):
    dirs = []
    # try:
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                path = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                try:
                    my_torrent = Torrent.from_file(path)
                    for torrfile in my_torrent.files:
                        # loger.info('name:'+torrfile.name)
                        if (torrfile.name.startswith(str)):
                            loger.info('t:==>' + path)
                            dirs.append(path)
                            # loger.info(my_torrent.total_size / len)
                            loger.info('str:==>' + str)
                            # loger.info(my_torrent.files)
                            break
                except BencodeDecodingError:
                    loger.info("error " + filename)
                    continue
                except IndexError:
                    loger.info("error " + filename)
                    continue


# finally:
# loger.info('dirs',dirs)

def editXunleiFile(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix):
                loger.info('dirpath:' + dirpath)
                new = filename.replace(xunleisuffix, "")
                oldfile = filepath + os.sep + filename
                newfile = filepath + os.sep + new
                loger.info("修改前:" + oldfile)
                loger.info("修改后:" + newfile)
                os.renames(oldfile, newfile)


def clearXunleiFile(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix):
                fullname = os.path.join(dirpath, filename)
                try:
                    loger.info('file: ' + fullname)
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
        path = filepath + i + os.path.sep
        if os.path.isdir(path):
            loger.info("writeTorrDetail path=====" + path)
            getTorrDetail(path)


# 过滤大文件
# filterLen 过滤文件大小单位G
def filterBigfiles(torrpath, filterLen):
    torrBigFilePath = torrpath + 'big\\'
    mkdirs(torrBigFilePath)
    lenG = filterLen * 1024 * 1024
    bigfiles = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                loger.info('torr==' + torr)
                my_torrent = Torrent.from_file(torr)
                fileSize = my_torrent.total_size
                loger.info('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr, torrBigFilePath + filename)
                    loger.info('大文件')
                    bigfiles.append(my_torrent.name)
    loger.info('bigfiles size:' + str(len(bigfiles)))
    loger.info('bigfiles:' + str(bigfiles))


# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
# 1.scan torr path,get dict  key 种子名称   val 种子路径
# 2. find same move
def filterDownFiles(torrpath, filepath, subDirName):
    # for dirpath, dirnames, filenames in os.walk(filepath):
    #     for dirname in dirnames:
    #         loger.info('dir:   ' +dirname)
    dirList = []
    # 搜集已下载文件列表 TODO 增加单文件支持
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
            dirList.append(filename)
            loger.info('dirname   ' + filename)
        # else:
        #     portion = os.path.splitext(filename)
        #     loger.info('00000  ' + portion[0])
        #     dirList.append(portion[0])
    files = os.listdir(filepath)
    # clearMacConfigFile(dirList)
    # 根据种子路径生成词典  key 种子名称   val 种子路径
    torrDict = geneTorrentDic(torrpath)
    torrlist = torrDict.keys()

    # loger.info('dict===='+str(torrDict))
    reset = set(dirList) & set(torrlist)
    # loger.info('dirList'+str(dirList))
    # loger.info('torrlist' + str(torrlist))
    rslist = list(reset)
    loger.info("  =====================  ")
    loger.info(rslist)

    torrDonePath = torrpath + os.path.sep + subDirName+ os.path.sep
    mkdirs(torrDonePath)

    finishFilePath = filepath + os.path.sep + subDirName+ os.path.sep
    mkdirs(finishFilePath)

    for samefile in rslist:
        loger.info(" ****   ")
        # loger.info(torrDict[samefile])
        loger.info(os.path.basename(torrDict[samefile]))
        newTorrFile = torrDonePath + os.path.basename(torrDict[samefile])

        finishFile = finishFilePath + samefile
        # 已经移动了，删除原有的
        if os.path.isfile(newTorrFile):
            os.remove(torrDict[samefile])
        else:  # 移动种子
            shutil.move(torrDict[samefile], newTorrFile)
        # 移动完成文件
        shutil.move(filepath + os.path.sep + samefile, finishFile)
        loger.info('finishFile:' + finishFile)

    loger.info('移动种子文件：' + str(len(rslist)))

    # 计算文件的大小，下载比例


def countFile(torrpath, filepath):
    # 搜集下载中文件列表
    namelist = []
    sizelist = []
    for filename in os.listdir(filepath):
        namelist.append(filename)
        path = os.path.join(filepath, filename)
        sizelist.append(cal_size(path))
    fileDict = dict(zip(namelist, sizelist))

    torrDict = geneTorrentDic(torrpath)
    # todo


# 根据种子路径生成词典  key 种子名称   val 种子路径
# 原则上不会有重复，毕竟文件名不可能重复
def geneTorrentDic(torrpath):
    torrlist = []
    torrNamelist = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                try:
                    my_torrent = Torrent.from_file(torr)
                except BencodeDecodingError:
                    print("error " + torrpath)
                    continue
                except IndexError:
                    print("error " + torrpath)
                    continue
                torrlist.append(my_torrent.name)
                torrNamelist.append(torr)
    torrDict = dict(zip(torrlist, torrNamelist))
    return torrDict

    # 计算文件夹file_path的大小


def cal_size(self, file_path):
    sum = 0
    try:
        os.listdir(file_path)
    except:
        pass
    else:
        for f in os.listdir(file_path):
            abspath = os.path.join(file_path, f)
            if os.path.isfile(abspath):
                portion = os.path.splitext(abspath)
                if portion[1] != ".xltd":
                    sum += os.path.getsize(abspath)
            elif os.path.isdir(abspath):
                sum += self.cal_size(abspath)
    return sum


def mkdirs(path):
    if (not os.path.exists(path)):
        loger.info('mkdir:' + path)
        os.mkdir(path)


def getTorrDetail(filepath):
    filepath = filepath + os.path.sep
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + '.txt'
    loger.info('basename==>' + basename)
    loger.info('dirname==>' + dirname)
    loger.info('txtfile===>' + txtpath)

    txtfile = open(txtpath, 'w+', encoding='utf-8')

    len = 1024 * 1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("=================================" + '\r')
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
                txtfile.writelines(torr + '\r')
                try:
                    my_torrent = Torrent.from_file(torr)
                    tlen = my_torrent.total_size / len
                    txtfile.writelines(str(tlen) + '\r')

                except BencodeDecodingError:
                    txtfile.writelines('torrent file is error ')
                    txtfile.writelines('****************************')
                    print("error " + torr)
                    continue
                except IndexError:
                    txtfile.writelines('torrent file is error ')
                    txtfile.writelines('****************************')
                    print("error " + torr)
                    continue
                txtfile.writelines(str(my_torrent.files) + '\r\n')
                txtfile.writelines(my_torrent.info_hash + '\r')
                # loger.info(my_torrent.total_size / len)
                # loger.info(my_torrent.comment)
                loger.info(portion[0] + '          ' + my_torrent.name)
                for torrfile in my_torrent.files:
                    if (torrfile.length > 100 * len):
                        txtfile.writelines(str(torrfile) + '\r')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()


# 数据库插入缓冲池
dbqueue = queue.Queue()


# 根据目录获取种子路径列表
def getTorListByDir(torrdir):
    datalist = []
    sum = 0
    broken_num = 0
    # get_oswalk_desc 获取文件倒序
    for dirpath, dirnames, filenames in os.walk(torrdir):
        # for dirpath, dirnames, filenames in fu.get_oswalk_desc(torrdir):
        i = 0

        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            # loger.info("=================================")
            # loger.info(portion)
            if portion[1] == ".torrent":
                sum += 1
                # loger.info("================torrent conteng=================" + '\r\n')
                # loger.info(torr)
                try:
                    my_torrent = Torrent.from_file(torr)
                except BencodeDecodingError:
                    # 种子下载失败了
                    loger.error('error file ' + torr)
                    errorpath = dirpath + '/errfiles'
                    mkdirs(errorpath)
                    shutil.move(torr, errorpath + '/' + filename)
                    broken_num += 1
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
                    datalist = []
                i += 1
        if (datalist is not None and len(datalist) > 0):
            dbqueue.put(datalist)
            loger.info("put 2 data" + str(datalist))
            loger.info("put 2 queue" + str(len(datalist)))
            loger.info("put 2 queue sum" + str(sum))
            datalist = []
            # loger.info("put 2 queue")
            # loger.info("put 2 queue" + str(datalist))
    loger.info("sum:" + str(sum))
    loger.info("broken_num:" + str(broken_num))


# 入库查重批次个数
batchsize = 100


# 生成map对象，key 为hash val 为#[hash, path, filename]
def build_torrObj_dic(datalist):
    dict = {}
    if datalist is not None and len(datalist) > 0:
        for data in datalist:
            dict[data[0]] = data
    return dict


def gethashlist(datalist):
    hashs = []
    if datalist is not None or len(datalist) > 0:
        for arr in datalist:
            # [hash, path, filename]
            hashs.append(arr[0])
    return hashs




# dblist 查询数据库返回的重复数据
# datalist待过滤数据集，过滤后插入数据库
# return 返回待插入的数据集
def filterDirtyData(datadict, dblist):
    if dblist is not None and len(dblist) > 0:
        data_hashlist = datadict.keys()
        rslist = list(datadict.values())
        # 查询每条数据库记录
        for dbrs in dblist:
            # [id, hcode, path, filename, time]
            hcode = dbrs[1]

            if hcode in data_hashlist:  # 做分支，是否转移种子文件
                obj = datadict.get(hcode)
                try:
                    rslist = [tor for tor in rslist if not (
                            tor[0] == dbrs[1]
                        # and
                        # tor[1] == dbrs[2] and
                        # tor[2] == dbrs[3]
                    )]
                    # rslist.pop(obj)

                    # 判断是否为相同文件，相同直接去除，不相同的同源种子，进行位置转移
                    comparefile(obj[0], obj[1], obj[2],
                                dbrs[1], dbrs[2], dbrs[3])
                except TypeError:
                    loger.error('obj is ' + str(obj))
                    loger.error('rslist is ' + str(rslist))
                # [hash, path, filename]
        loger.info("filterDirtyData重新插入数据 清理前数据条数" + str(len(data_hashlist)) + '  清理后数据条数' + str(
            len(rslist)))
        # loger.info("filterDirtyData重新插入数据datalist"+str(data_hashlist))
        return rslist
    else:
        return list(datadict.values())


DUP = 'duplicate'
DUP_DIRNAME = os.path.sep + DUP + os.path.sep
Enter = '\r\n'


# torrpath 种子原始文件路径
# 新增文件夹，并写日志，打印
def writeDupLog(torrpath, msg):
    if (torrpath.endswith(DUP)):
        duplicateDir = torrpath
    else:
        duplicateDir = torrpath + DUP_DIRNAME
    writer = log(duplicateDir, "dirtyData", True)
    writer.writelines("**********dirtyData   start***************" + '\r\n')
    # writer.writelines("扫描文件:" +filearry)
    # writer.writelines("数据库文件:" + dbarray)
    writer.writelines(msg + '\r\n')
    writer.writelines("**********dirtyData   done***************" + '\r\n')
    writer.close()


# 判断种子文件是否存在
# 如果两张表都不存在，只额吉插入torrentdup表中
# torrent表or Torrentdup存在,则不做处理
# 返回结果True表示
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

    else:  # bug
        loger.info("出现bug")
        # loger.info("出现bug")




# path 待扫描生成唯一hashcode的种子路径
def scan_torr_get_hashlist(path, txt):
    tarlist = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = Torrent.from_file(torr)
                hashcode = my_torrent.info_hash.lower()
                if txt is not None:
                    txt.writelines("hashcode  " + hashcode + '\r\n')
                tarlist.append(hashcode)


def findTorrentByHashcode(srctorrpath, tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcode', False)
    # 遍历待查找的种子，生成集合
    tarlist = scan_torr_get_hashlist(tartorrpath, txt)
    txt.writelines("************************待查找************  " + '\r\n')
    srclist = scan_torr_get_hashlist(srctorrpath, None)

    dupdata = [dup for dup in tarlist if dup in srclist]
    for dirpath, dirnames, filenames in os.walk(srctorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                srctorrpath = os.path.join(dirpath, filename)
                srctorrent = Torrent.from_file(srctorrpath)
                srccode = srctorrent.info_hash.lower()
                if srccode in tarlist:
                    txt.writelines("hashcode  " + srccode + '\r\n')
                    txt.writelines("dirpath  " + dirpath + '\r\n')
                    txt.writelines("filename  " + filename + '\r\n')

    txt.close()


# srctorrpath  种子集散地
# tartorrpath  待查找种子
def findTorrentByHashcodeInDir(srctorrpath, tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcodeInDir', False)
    tarlist = []
    # 遍历待查找的种子，生成集合
    txt.writelines("************************待查找************  " + '\r\n')
    for dirpath, dirnames, filenames in os.walk(tartorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = Torrent.from_file(torr)
                hashcode = my_torrent.info_hash.lower()

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
                except BencodeDecodingError:
                    # 种子下载失败了
                    loger.info('error file ' + srctorrpath)
                    continue
                except IndexError:
                    loger.info('error file ' + srctorrpath)
                    continue

                srccode = srctorrent.info_hash.lower()
                if srccode in tarlist:
                    txt.writelines("hashcode  " + srccode + '\r\n')
                    txt.writelines("dirpath  " + dirpath + '\r\n')
                    txt.writelines("filename  " + filename + '\r\n')

    txt.close()


def log(filepath, name, append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + name + '.txt'
    # loger.info('basename==>' + basename)
    # loger.info('dirname==>' + dirname)
    # loger.info('txtfile===>' + txtpath)

    if (append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile




# 将重复文件移动至
def moveduplicateTorr(tfile):
    dir_path = os.path.dirname(tfile)
    filename = os.path.basename(tfile)
    dupilicatedir = dir_path + 'duplicate\\'
    mkdirs(dupilicatedir)
    shutil.move(tfile, dupilicatedir + filename)


# 扫描half文件夹下所有未下载文件，生成对应得种子文件
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


# 用来扫描half文件夹下所有待扫描的半下载文件
# downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def countHalfFiles(downdir, deltag):
    for root, dirs, files_list in os.walk(downdir):
        for file_name in files_list:
            if file_name.endswith('torrent') and not str(file_name).startswith(HALF_NAME_PREFIX):
                tfile = os.path.join(root, file_name)
                loger.info("tfile:" + tfile)
                loger.info("root:" + root)
                comparefiles(tfile, root)


### downdir 下载目录，包含了种子文件的头目录
### 日志文件
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def scanDownloadingFiles(downdir, txtfile, deltag):
    downloadmap = {}
    for dirpath, dirnames, filenames in os.walk(downdir):
        txtfile.writelines('dirpath' + dirpath + '\r\n')
        # loger.info('dirpath'+dirpath)
        # loger.info('dirnames' + dirnames)
        for filename in filenames:

            portion = os.path.splitext(filename)
            if deltag and filename.endswith(xunleisuffix):
                fullname = os.path.join(dirpath, filename)
                loger.info("del path:" + fullname)
                os.remove(fullname)
            elif portion[1] != ".bt":  # 处理待下载文件，
                fullname = os.path.join(dirpath, filename)
                fsize = os.path.getsize(fullname)
                # loger.info("full path:"+fullname)
                # fullname=os.path.join(dirpath, ' '+filename)#torrent的file会有空格， 很奇怪
                torrfilepath = fullname.replace(downdir, '')
                if str(torrfilepath).startswith(os.path.sep):  # fix py版本兼容性问题
                    torrfilepath = torrfilepath[1:]
                # txtfile.writelines("download :" + torrfilepath+ '\r\n')
                # loger.info("size"+str(round(fsize/m,2))+'mb')
                downloadmap.setdefault(torrfilepath, fsize)  # 生成文件列表

    return downloadmap


xunleisuffix = '.bt.xltd'


# tfiles 种子里的文件，
# downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
# todo  写日志
def comparefiles(tfile, downdir, deltag):
    txtfile = log(downdir, 'comparefiles', False)
    txtfile.writelines('tfile' + tfile + '\r\n')
    txtfile.writelines('downdir' + downdir + '\r\n')
    loger.info('downdir' + downdir)
    torrentmap = {}
    my_torrent = Torrent.from_file(tfile)

    for file in my_torrent.files:  # 遍历种子文件
        ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
        tfilename = file.name.replace('\\\\', os.path.sep)
        # loger.info('tfilename'+tfilename)
        # 截取359目录，由于可能会改名，所以
        file_array = tfilename.split(os.path.sep, 1)
        if (len(file_array) == 1):
            print('len1  tfilename==>' + tfilename)
            continue
        else:
            subpath = file_array[1]

        if subpath.__contains__(os.path.sep):
            subname = subpath.split(os.path.sep, 1)[1]
        else:
            subname = subpath
        # subpath \尖叫视频.mht
        # loger.info('subpath'+str(subpath))

        if subname not in array:
            if subname.__contains__('如果您看到此文件，请升级到BitComet'):
                loger.info(subname)
            else:
                txtfile.writelines("subpath :" + subpath)
                torrentmap.setdefault(subpath, file.length)
        ## 待增加过滤无用文件实现

    downloadmap = scanDownloadingFiles(downdir, txtfile, deltag)
    m = 1024 * 1024

    # loger.info(tfilename)
    # loger.info(str(file))
    downloadfilelist = list(downloadmap.keys())
    tfiellist = list(torrentmap.keys())
    # txtfile.writelines(str(tfiellist))
    txtfile.writelines('*************************************************')
    txtfile.writelines('downloadfilelist' + str(len(downloadfilelist)) + '   ' + '\r\n')  # +str(downloadfilelist)
    # for dfile in downloadfilelist:
    # loger.info('tfiellist bf' + str(len(tfiellist)) + '   ' + str(tfiellist))
    tfiellist = getUndownFileList(tfiellist, downloadfilelist)
    # for cleanfile in downloadfilelist:
    #     if cleanfile in tfiellist:
    #         tfiellist.remove(cleanfile)
    # loger.info('tfiellist af' + str(len(tfiellist)) + '   ' + str(tfiellist))
    downloadfilesize = 0
    txtfile.writelines("********************v1.0 已下载文件个数" + str(
        len(downloadfilelist)) + "个***************************" + '\r\n')
    txtfile.writelines(
        "********************v1.0 待下载文件列表" + str(len(tfiellist)) + "个***************************" + '\r\n')
    for needdownfile in tfiellist:
        tfsize = torrentmap.get(needdownfile)
        downloadfilesize += tfsize
        tfsize = round(tfsize / m, 2)
        txtfile.writelines(needdownfile + '\r\n')
        txtfile.writelines('size:' + str(tfsize) + "mb" + '\r\n')
    txtfile.writelines('总占用空间":' + str(round(downloadfilesize / m, 2)) + "mb" + '\r\n')
    txtfile.close()


# tfiles  种子文件列表
# downedfiles  已下载文件列表
def getUndownFileList(tfiles, downedfiles):
    tmap = {}  # key 去除了路径中的所有空格， val原路径
    for tf in tfiles:
        ctf = tf.replace(" ", "")
        tmap.setdefault(ctf, tf)
    tflist = tmap.keys()
    dmap = {}
    for df in downedfiles:
        cdf = df.replace(" ", "")
        dmap.setdefault(cdf, df)
    dflist = dmap.keys()
    for dfile in dflist:
        if dfile in tflist:
            tmap.pop(dfile)

    return tmap.values()
#todo loadTorr 使用
#todo scan error y 文件夹白名单
#scan big方法修改为  scan big small

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
    # loger.info('C5AEA8F99A520790D421FEB7162DDF7A77BD297B'.lower())
    # strlist=['爱剪辑-48.avi']
    # findTorrListByStr(strlist,'D:\\temp\\0555\\2022-03-01\\0555\\')
    # findTorrListByStr(strlist, 'D:\\temp\\0555\\2022-03-01\\0555\\b20\errfiles\\')

    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b30\\")
    # os._exit(0)
    # findTorrentByHashcodeInDir("D:\\temp\\0555\\2022-03-01\\","D:\\temp\\backup\\find\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b25\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\normal\\")
    # countHalfFiles('D:\\temp\\chachong\\193-性感美女顶级调教 狂操捆绑 强制高潮 爆菊 滴蜡 K9训犬 群P毒龙 乱交露出\\')
    # genhalfTorrent('D:\\temp\\chachong\\')
    # filterDownFiles(r'D:\temp\b31', r'D:\temp\sp', 'y')
    # writeTorrDetail('D:\\360Downloads\\1228\\')
    # os._exit(0)
    #filterDownFiles(r'C:\torrent\b39', r'E:\down\0555\b39', 'y')
    # filterDownFiles(r'C:\torrent\b39', r'E:\down\0555\b39\un', 'y')
    # getTorrDetail(r'C:\torrent\b39')
    getTorrDetail(r'D:\temp\0555\2022-03-01\0555\b43')
    os._exit(0)