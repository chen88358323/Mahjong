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
import loggerTemplate

loger= loggerTemplate.log
TORR_ERROR_DIRNAME='errorbak'
HALF_NAME_PREFIX='HALF-'
logpath='D:\\temp\\0555\\'

array = ['【01axg.xyz】.jpg', '02AXG.XYZ.png', '03axg.XYZ.png', '8axg.xyz.png',
         'duplicatedirtyData.txt'
         ]
def removeFiles(filepath):
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath + "\\" + filename
                loger.info(absPath)
                os.remove(absPath)
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
            return None
    except IndexError:
        loger.info("error " + torrpath)
        return None

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
    files =os.listdir(filepath)
    # clearMacConfigFile(dirList)
    # 根据种子路径生成词典  key 种子名称   val 种子路径 todo  key修改为hcode
    torrDict=geneTorrentDic(torrpath)
    torrlist=torrDict.keys()
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
#有些种子文件，结尾有\r\n导致，解析错误，扫描一遍，将有错误的文件重新生成一遍
#torrdir  c:\\ttt
def pre_slove_error_torrs(torrdir):
    for filename in os.listdir(torrdir):
        file_path = os.path.join(torrdir, filename)

        portion = os.path.splitext(filename)
        if portion[1] == ".torrent":
            fix_torrent(file_path)

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

if __name__ == '__main__':
    getTorrDetail('D:\\360Downloads\\1228\\')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b35', r'G:\down\0555\b35\un', 'y')
    clearXunleiFile("D:\\temp\\")
    findTorrentByHashcodeInDir(r"D:\temp\0555\2022-03-01",r"D:\temp\0555\tttt")