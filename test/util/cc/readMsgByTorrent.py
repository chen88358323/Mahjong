from torrentool.api import Torrent
from torrentool.api import TorrentFile
from torrentool.exceptions import BencodeDecodingError
import os
import  shutil
import mysqlTemplate as dbtool
import time
import queue,threading
import sys
from typing import Any, Tuple

#入库查重批次个数
batchsize=50
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
'草榴最新地址.mht'

         ]
def removeFiles(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'

    # prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath + "\\" + filename
                print(absPath)
                os.remove(absPath)
            # torr = os.path.join(dirpath, filename)
            # absPath = dirpath + filename
            # if(absPath.endswith(prefix)):
            #     print(absPath)


def getDulicateFiles():
    filepath = 'D:\\temp\\593254315050521\\'
    prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            absPath = dirpath + filename
            if(absPath.endswith(prefix)):
                print(absPath)

def getTorrentByDetails(str,filepath):
    dirs = []
    # try:
    for i in os.listdir(filepath):
        path = filepath + r'\\' + i
        if os.path.isdir(path):
            if ((path in dirs) == False and path.endswith('y')):
                # print('add ' + path)
                dirs.append(dirs)
            print('path*****'+i+'   '+path)
            getTorrentByDetails(str, path)
        elif os.path.isfile(path) and path.find(".torrent"):
            my_torrent = Torrent.from_file(path)
            for torrfile in my_torrent.files:
                # print('name:'+torrfile.name)
                if (str in torrfile.name):
                    dirs.append(path)
                    # print(my_torrent.total_size / len)
                    print('t:==>' + path)
                    print(my_torrent.files)
                    break
# finally:
# print('dirs',dirs)

def editXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith('.bt.xltd'):
                print('dirpath:'+dirpath)
                new = filename.replace(".bt.xltd", "")
                oldfile=filepath + os.sep + filename
                newfile=filepath + os.sep + new
                print("修改前:" + oldfile)
                print("修改后:" + newfile)
                os.renames(oldfile, newfile)

def clearXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith('.bt.xltd'):
                fullname=os.path.join(dirpath,filename)
                try:
                    print('file: '+fullname)
                    os.remove(fullname)
                except UnicodeEncodeError:
                    # non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    # fullname=fullname.translate(non_bmp_map)
                    print('full: ' + fullname)
                    os.remove(fullname)

'''
批量写子文件内容
'''
def writeTorrDetail(filepath):
    for i in os.listdir(filepath):
        path = filepath +  i+r'\\'
        if os.path.isdir(path):
            print("writeTorrDetail path====="+path)
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
                print('torr==' + torr)
                my_torrent = Torrent.from_file(torr)
                fileSize=my_torrent.total_size
                print('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr,torrBigFilePath+filename)
                    print('大文件')
                    bigfiles.append(my_torrent.name)
    print('bigfiles size:' + str(len(bigfiles)))
    print('bigfiles:'+str(bigfiles))

# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
def filterDownFiles(torrpath,filepath,subDirName):
    # for dirpath, dirnames, filenames in os.walk(filepath):
    #     for dirname in dirnames:
    #         print('dir:   ' +dirname)
    dirList=[]
    #搜集已下载文件列表
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
            dirList.append(filename)
            print('dirname   '+filename)
        # else:
        #     portion = os.path.splitext(filename)
        #     print('00000  ' + portion[0])
        #     dirList.append(portion[0])

    # clearMacConfigFile(dirList)

    torrDict=geneTorrentDic(torrpath)
    torrlist=torrDict.keys()

    #print('dict===='+str(torrDict))
    reset=set(dirList)&set(torrlist)
    #print('dirList'+str(dirList))
    #print('torrlist' + str(torrlist))
    rslist=list(reset)
    print("  =====================  ")
    print(rslist)

    torrDonePath = torrpath+subDirName
    mkdirs(torrDonePath)

    finishFilePath = filepath+subDirName
    mkdirs(finishFilePath)

    for samefile in rslist:
        print(" ****   ")
        #print(torrDict[samefile])
        print(os.path.basename(torrDict[samefile]))
        newTorrFile = torrDonePath+os.path.basename(torrDict[samefile])

        finishFile = finishFilePath+samefile
        #已经移动了，删除原有的
        if os.path.isfile(newTorrFile):
            os.remove(torrDict[samefile])
        else: #移动种子
            shutil.move(torrDict[samefile],newTorrFile)
        #移动完成文件
        shutil.move(filepath+samefile,finishFile)
        print('finishFile:' + finishFile)

    print('移动种子文件：'+str(len(rslist)))

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
def geneTorrentDic(torrpath):
    torrlist = []
    torrNamelist = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # print('torr=='+torr)
                my_torrent = Torrent.from_file(torr)
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
        print('mkdir:' + path)
        os.mkdir(path)

def getTorrDetail(filepath):
    dirname = os.path.dirname(filepath)
    #文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath=filepath+basename+'.txt'
    print( 'basename==>'+basename)
    print('dirname==>'+dirname)
    print('txtfile===>'+txtpath)

    txtfile=open(txtpath,'w+',encoding='utf-8')

    len=1024*1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("================================="+'\r')
            # txtfile.writelines(portion)
            # print("=================================")
            # print(portion)
            # 如果后缀是.xltd
            # if portion[1] == ".xltd":
            #     print("need change")
            #     newnamee=portion[0].replace('.bt','')
            #     os.renames(filepath+portion[0]+portion[1],filepath+newnamee)
            if portion[1] == ".torrent":
                # print(torr)
                txtfile.writelines(torr+'\r')
                my_torrent = Torrent.from_file(torr)
                tlen=my_torrent.total_size / len
                txtfile.writelines(str(tlen)+'\r')
                txtfile.writelines(my_torrent.info_hash+'\r')

                # print(my_torrent.total_size / len)
                # print(my_torrent.comment)
                print(portion[0]  +'          '+ my_torrent.name)
                for torrfile in my_torrent.files:
                    if(torrfile.length>100*len):
                        txtfile.writelines(str(torrfile)+'\r')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()

#数据库插入缓冲池
dbqueue = queue.Queue()
#根据目录获取种子路径列表
def getTorListByDir(torrdir):
    datalist = []

    sum = 0
    for dirpath, dirnames, filenames in os.walk(torrdir):
        i=0

        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            #print("=================================")
            #print(portion)
            if portion[1] == ".torrent":
                sum+=1
                # print("================torrent conteng=================" + '\r\n')
                # print(torr)
                try:
                    my_torrent = Torrent.from_file(torr)
                except BencodeDecodingError:
                    #种子下载失败了
                    print('error file '+torr)
                    errorpath=dirpath+'/errfiles'
                    mkdirs(errorpath)
                    shutil.move(torr,errorpath+'/'+filename)
                    continue
                except IndexError:
                    print('error file ' + torr)
                    continue

                hash = my_torrent.info_hash
                path = os.path.dirname(torr)
                tobj = [hash, path, filename]
                datalist.append(tobj)
                if i == batchsize:
                    i = 0
                    dbqueue.put(datalist)
                    print("put 2 queue" + str(datalist))

                    datalist = []
                i += 1
        if (datalist is not None and len(datalist) > 0):
            dbqueue.put(datalist)
            print("put 2 queue" + str(datalist))
    print("sum:"+str(sum))

#torrPathlist 种子路径列表
# 列表每条记录包括 hcode ,path, filename
def converDatalist2DB():
    count=0
    while True:
        # if count==20:
        #     break
        if dbqueue.empty():
            count+=1
            print("dbqueue is empty")
            time.sleep(3)
        else:
            datalist=dbqueue.get()
            count+=batchsize
            tag = dbtool.recoderbatch(datalist)
            if(not tag):#插入失败
                hashs=[]
                for arr in datalist:
                    #[hash, path, filename]
                    hashs.append(arr[0])
                    #result dataset  [id ,hcode,path,filename,time]
                result=dbtool.queryByHashCode(hashs)
                datalist2=filterDirtyData(datalist,result)
                if datalist2 is not None and len(datalist2) >0:
                    dbtool.recoderbatch(datalist2)

                # 获得重复数据，写日志
                # dupilicatelist = list(set(datalist).difference(set(datalist2)))
                # writer = log("D:\\temp\\0555\\", "findDupulicate", True)
                # writer.writelines("*************************" + '\r\n')
                # writer.close()
        print("count:"+str(count))



#reslist 查询数据库返回的重复数据
#data待过滤数据集，过滤后插入数据库
#return 返回待插入的数据集
def filterDirtyData(datalist ,reslist):
    list=[]


    if reslist is not None and len(reslist) > 0:

        for r in reslist:
            # print("r[1]"+r[1])
            list.append(r[1])
        for scr in datalist:
            if scr[0] in list:#做分支，是否转移种子文件
                #判断是否为相同文件，相同直接去除，不相同的同源种子，进行位置转移
                datalist.remove(scr)
                index = list.index(scr[0])
                compareTorfile(scr,reslist[index])
                # [hash, path, filename]
        print("filterDirtyData重新插入数据datalist"+str(datalist))

        return  datalist
    else:
        return


    ####
    # res is dbTorFile
    #    format    [id ,hcode,path,filename,time]
    # tar is scan file
    # [hash, path, filename]
    # @return True 表示同源文件可以忽略
    # @return False 表示不同文件需要处理
    # ###
def compareTorfile(tar,res):


    if tar[0]==res[1]:
        tarfile=tar[1]+tar[2]
        dbtfile=res[2]+res[3]
        if tarfile==dbtfile:
            return  True
        else:
            duplicateDir = tar[1] + '\\duplicate\\'
            writer = log(duplicateDir, "dirtyData", True)
            writer.writelines("**********dirtyData   start***************" + '\r\n')
            writer.writelines("扫描文件:" + str(tar))
            writer.writelines("数据库文件:" + str(res))
            writer.writelines("**********dirtyData   done***************" + '\r\n')
            writer.close()
            #移动文件
            mkdirs(duplicateDir)
            shutil.move(tar[1]+'/'+tar[2],duplicateDir+tar[2])

            #插入数据库  也有可能重复
            dbtool.recorderDulicateTorrent(tar[0],tar[1],tar[2])

            return  False



def findTorrentByHashcode(srctorrpath,tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcode',False)
    tarlist=[]
    #遍历待查找的种子，生成集合
    for i in len(tarlist):
        tarlist[i]=tarlist[i].lower()
    txt.writelines("************************待查找************  " + '\r\n')

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
                    print('error file ' + srctorrpath)
                    continue
                except IndexError:
                    print('error file ' + srctorrpath)
                    continue

                srccode=srctorrent.info_hash.lower()
                if srccode in tarlist:
                    txt.writelines("hashcode  " + srccode + '\r\n')
                    txt.writelines("dirpath  " + dirpath + '\r\n')
                    txt.writelines("filename  " + filename + '\r\n')


    txt.close()

def log(filepath, name,append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + name + '.txt'
    # print('basename==>' + basename)
    # print('dirname==>' + dirname)
    print('txtfile===>' + txtpath)

    if(append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile
#根据路径名扫描入库,判断种子是否重复
def scanTorrentsIntoDB(torrDir):
    p1 = threading.Thread(target=getTorListByDir, args=(torrDir,))

    p1.start()
    time.sleep(3)
    c1 = threading.Thread(target=converDatalist2DB)
    c1.start()


def clearduplicateTorr():
    idlist=[]
    relist=dbtool.queryduplicatetor()
    if relist is not None and len(relist)>0:
        for res in relist:
            idlist.append(res[0])
            # [id, hcode, path, filename, time]
            # 1.文件迁移
            torrpath=res[2]+'\\'+res[3]
            #https://blog.csdn.net/zffustb/article/details/131236802
            moveduplicateTorr(torrpath)
            #2.查询主表，并生成日志
            #todo 先使用   SELECT * FROM duplicatetor d, torrents t where t.hcode=d.hcode;
        # 3. 删除记录
        delTag=dbtool.delDulicateTorrent(idlist)
        if delTag:
            print("*************delDulicateTorrent*****************")
            print(str(idlist))
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
#                 print("tfile:"+tfile)
#                 print("root:"+root)
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
#     #     downloadfilelist[i]=downloadfilelist[i].replace(r'\\\\',r'\\')
#     print('downloadfilelist:'+str(downloadfilelist))
#     my_torrent.files
#     tfiles=my_torrent.files
#     for file in tfiles:  # 遍历种子文件   #TorrentFile(name='134\\204V\\1 (1).mp4', length=13583369)
#         ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
#         # tfilename = file.name.replace('\\', '')
#         # print('tfilename'+tfilename)
#
#         subpath = file.name.split('\\', 1)[1]#截取359目录，由于可能会改名，所以
#         # if(subpath.endswith('1 (1).mp4')):  #test code
#         #     print('')
#         if subpath.__contains__('\\'):
#             subname = subpath.split('\\', 1)[1]
#         else:
#             subname=subpath
#         #subpath \尖叫视频.mht
#         # subpath = subpath.replace('\\', '\\\\')
#         print('subpath :'+str(subpath))
#
#         if subname.__contains__('如果您看到此文件，请升级到BitComet'):
#             print(subname)
#         elif subpath in downloadfilelist:
#
#             txtfile.writelines("subpath :" + subpath)
#             tfiles.remove(TorrentFile(file.name,file.length))
#     txtfile.close()
#     tf=tfile.replace(downdir ,'')
#     tf=downdir+'\\'+HALF_NAME_PREFIX+tf[2:]
#     my_torrent.files=tfiles
#     my_torrent.to_file(tf)
#     print('gen file '+tf)



#用来扫描half文件夹下所有待扫描的半下载文件
# downdir 下载目录，包含了种子文件的头目录
def countHalfFiles(downdir):
    for root, dirs, files_list in os.walk(downdir):
        for file_name in files_list:
            if file_name.endswith('torrent') and not  str(file_name).startswith(HALF_NAME_PREFIX):
                tfile=os.path.join(root, file_name)
                print("tfile:"+tfile)
                print("root:"+root)
                comparefiles(tfile,root)

### downdir 下载目录，包含了种子文件的头目录
### 日志文件
def scanDownloadingFiles(downdir,txtfile):
    downloadmap = {}
    for dirpath, dirnames, filenames in os.walk(downdir):
        txtfile.writelines('dirpath'+dirpath + '\r\n')
        # print('dirpath'+dirpath)
        # print('dirnames' + dirnames)
        for filename in filenames:
            portion = os.path.splitext(filename)
            #print("portion[1] "+portion[1])
            if portion[1] != ".bt":#处理待下载文件，
                fullname= os.path.join(dirpath, filename)
                fsize=os.path.getsize(fullname)
                #print("full path:"+fullname)
                # fullname=os.path.join(dirpath, ' '+filename)#torrent的file会有空格， 很奇怪
                torrfilepath=fullname.replace(downdir ,'')
                if str(torrfilepath).startswith('\\'):#fix py版本兼容性问题
                    torrfilepath= torrfilepath[1:]
                #txtfile.writelines("download :" + torrfilepath+ '\r\n')
                #print("size"+str(round(fsize/m,2))+'mb')
                downloadmap.setdefault(torrfilepath,fsize)#生成文件列表

    return downloadmap


    #tfiles 种子里的文件，
    #downdir 下载目录，包含了种子文件的头目录
    #todo  写日志
def comparefiles(tfile,downdir):
    txtfile = log(downdir, 'comparefiles',False)
    txtfile.writelines('tfile' + tfile + '\r\n')
    txtfile.writelines('downdir' + downdir + '\r\n')
    print('downdir' + downdir)
    torrentmap = {}
    my_torrent = Torrent.from_file(tfile)

    for file in my_torrent.files:  # 遍历种子文件
        ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
        tfilename = file.name.replace('\\\\', '\\')
        # print('tfilename'+tfilename)
        #截取359目录，由于可能会改名，所以
        subpath = tfilename.split('\\', 1)[1]
        if subpath.__contains__('\\'):
            subname = subpath.split('\\', 1)[1]
        else:
            subname=subpath
        #subpath \尖叫视频.mht
        #print('subpath'+str(subpath))

        if subname not in array:
            if subname.__contains__('如果您看到此文件，请升级到BitComet'):
                print(subname)
            else:
                txtfile.writelines("subpath :" + subpath)
                torrentmap.setdefault(subpath, file.length)
        ## 待增加过滤无用文件实现




    downloadmap=scanDownloadingFiles(downdir,txtfile)
    m=1024*1024

        #print(tfilename)
        #print(str(file))
    downloadfilelist = list(downloadmap.keys())
    tfiellist=list(torrentmap.keys())
    #txtfile.writelines(str(tfiellist))
    txtfile.writelines('*************************************************')
    txtfile.writelines('downloadfilelist'+str(len(downloadfilelist))+'   '+ '\r\n')#+str(downloadfilelist)
    # for dfile in downloadfilelist:
    #print('tfiellist bf' + str(len(tfiellist)) + '   ' + str(tfiellist))
    tfiellist=getUndownFileList(tfiellist,downloadfilelist)
    # for cleanfile in downloadfilelist:
    #     if cleanfile in tfiellist:
    #         tfiellist.remove(cleanfile)
    #print('tfiellist af' + str(len(tfiellist)) + '   ' + str(tfiellist))
    downloadfilesize=0
    txtfile.writelines("********************v1.0 已下载文件个数" + str(len(downloadfilelist)) + "个***************************" + '\r\n')
    txtfile.writelines("********************v1.0 待下载文件列表"+ str(len(tfiellist))+"个***************************"+ '\r\n')
    for needdownfile in tfiellist:

        tfsize=torrentmap.get(needdownfile)
        downloadfilesize+=tfsize
        tfsize =round(tfsize / m, 2)
        txtfile.writelines(needdownfile+ '\r\n')
        txtfile.writelines('size:'+str(tfsize)+"mb"+ '\r\n')
    txtfile.writelines('总占用空间":'+str(round(downloadfilesize / m, 2))+"mb"+ '\r\n')
    txtfile.close()

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
#     print("list1"+str(list1))
if __name__ == '__main__':
    #test()
    #clearXunleiFile("D:\\temp\\")
   # print('C5AEA8F99A520790D421FEB7162DDF7A77BD297B'.lower())

    findTorrentByHashcodeInDir("D:\\temp\\0555\\2022-03-01\\","D:\\temp\\backup\\find\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b25\\")
    #scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\normal\\")
    #countHalfFiles('D:\\temp\\chachong\\193-性感美女顶级调教 狂操捆绑 强制高潮 爆菊 滴蜡 K9训犬 群P毒龙 乱交露出\\')
    # genhalfTorrent('D:\\temp\\chachong\\')
    #
    #scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b15\\")
    #clearduplicateTorr()

    # removeFiles('e:\\')
    # removeFiles('f:\\')
    # removeFiles('g:\\')
    # removeFiles('h:\\')

   # removeFiles('E:\\PDF\\')
    #removeFiles('G:\\CC\\BOOKS\\')

    #scanTorrentsIntoDB("C:\\Users\\Administrator\\Downloads\\best\\")

    # scanTorrentsIntoDB("D:\\temp\\0555\\t\\0555\\b12\\")
    # tormd5("C:\\Users\\Administrator\\Downloads\\best\\推特网红大屁股骚货kbamspbam，怀孕了还能挺着个大肚子拍照拍视频挣钱，太敬业了，奶头变黑 但白虎粉穴依然粉嫩.torrent")
    #os._exit(0)
    # getDulicateFiles()
    #getTorrDetail('i:\\done\\')
    # getTorrDetail('D:\\temp\\best2\\best4\\')
    #getTorrDetail('D:\\360Downloads\\1228\\')
    # writeTorrDetail('D:\\temp\\1228\\')
    #filterBigfiles('D:\\360Downloads\\test\\', 1000)
    # filterDownFiles('D:\\360Downloads\\1228\\8\\','D:\\temp\\1228\\','y\\')
    # writeTorrDetail('D:\\360Downloads\\1228\\')

    # getTorrDetail('D:\\temp\\593254315050521\\1210-best\\1\\')

    # getTorrentByDetails('D:\\360Downloads\\1228\\5\\')

    # for i in range(51):
    #     dirpath='D:\\temp\\593254315050521\\alltorr\\'+str(i)+'\\'+str(i)+'\\y'
    #     if(os.path.isdir(dirpath)):
    #         # print('D is '+dirpath)
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
