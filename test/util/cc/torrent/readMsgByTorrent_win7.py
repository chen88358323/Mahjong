# -*- coding: utf-8 -*-
from torrentool.api import Torrent
import threading
import shutil
from torrentool.exceptions import BencodeDecodingError
import os
import loggerTemplate
loger = loggerTemplate.log
from torrent_download_files_check import  DownLoadCheck


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
                print(absPath)


def getTorrentByDetails(str, filepath):
    dirs = []
    # try:
    for i in os.listdir(filepath):
        path = filepath + r'\\' + i
        if os.path.isdir(path):
            if ((path in dirs) == False and path.endswith('y')):
                # print('add ' + path)
                dirs.append(dirs)
            print('path*****' + i + '   ' + path)
            getTorrentByDetails(str, path)
        elif os.path.isfile(path) and path.find(".torrent"):
            my_torrent =  loadTorr(path)
            if my_torrent is not None:
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




xunleisuffix='.bt.xltd'
def editXunleiFile(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix):
                print('dirpath:' + dirpath)
                new = filename.replace(xunleisuffix, "")
                oldfile = filepath + os.sep + filename
                newfile = filepath + os.sep + new
                print("修改前:" + oldfile)
                print("修改后:" + newfile)
                os.renames(oldfile, newfile)


'''
批量写子文件内容
'''


def writeTorrDetail(filepath):
    for i in os.listdir(filepath):
        path = filepath + i + r'\\'
        if os.path.isdir(path):
            print("writeTorrDetail path=====" + path)
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
                print('torr==' + torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                fileSize = my_torrent.total_size
                print('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr, torrBigFilePath + filename)
                    print('大文件')
                    bigfiles.append(my_torrent.name)
    print('bigfiles size:' + str(len(bigfiles)))
    print('bigfiles:' + str(bigfiles))


# 根据文件夹路径，生成扫描文件，并写入结果
def log(filepath, name,append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + name + '.txt'
    print('basename==>' + basename)
    print('dirname==>' + dirname)
    print('txtfile===>' + txtpath)
    if (append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile
# 根据文件夹路径，生成扫描文件，并写入结果
# append 是否追加，追加True 新建False
def log(filepath, name,append):
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + name + '.txt'
    print('basename==>' + basename)
    print('dirname==>' + dirname)
    print('txtfile===>' + txtpath)
    if(append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile

def findTorrentByDirNameMulti(torrpath, findstr,threadid):
    thread = threading.Thread(target=findTorrentByDirName, args=(torrpath, findstr, threadid))
    thread.start()
#加载种子，如果种子错误或者内容为空，返回空
def loadTorr(torrpath):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return  my_torrent
    except BencodeDecodingError:
        print("error " + torrpath)
    except IndexError:
        print("error " + torrpath)
    return None
# 根据已下载文件名查找对那个的种子文件，值查找目录，查找每个文件使用findTorrentByTxt
def findTorrentByDirName(torrpath, findstr,threadid):

    txt = log(torrpath, 'search'+threadid,True)
    txt.writelines('*****************'+findstr+'*****************\r\n')
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # print('torr==' + torr)
                my_torrent = loadTorr(torr)
                if(my_torrent!=None):
                    tfiles = my_torrent.files
                    if (tfiles is not None):
                        for file in tfiles:
                            torrentpath = file.name
                            if (findstr in torrentpath):
                                str = torrpath + filename
                                txt.writelines('*****************')
                                txt.writelines('\n')
                                txt.writelines('dirpath' + dirpath)
                                txt.writelines('\n')
                                txt.writelines('----------------------')
                                txt.writelines(dirpath+'\\' + filename)
                                torrentFiles2str(tfiles, txt)
                                break
                                # txt.writelines('tfiles' + str(tfiles))
    txt.close()



# 与findTorrentByDirName 区别，该方法查找种子中的每个文件命名
def findTorrentByTxt(torrpath, *findstrs):
    txt = log(torrpath, 'search',False)
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # print('torr==' + torr)
                my_torrent = loadTorr(torr)
                if (my_torrent != None):
                    tfiles = my_torrent.files
                    if (tfiles is not None):
                        for file in tfiles:
                            torrentpath = file.name
                            for findstr in findstrs:
                                if (findstr in torrentpath):
                                    str = torrpath + filename
                                    txt.writelines('*****************')
                                    txt.writelines('\n')
                                    txt.writelines('dirpath' + dirpath)
                                    txt.writelines('\n')
                                    txt.writelines('----------------------')
                                    txt.writelines(dirpath+'\\' + filename)
                                    torrentFiles2str(tfiles, txt)
                            # txt.writelines('tfiles' + str(tfiles))


    txt.close()


def torrentFiles2str(tfiles, log):
    log.writelines('\n')
    count=0
    for f in tfiles:
        # if(count>10):
        #     break
        log.writelines(f.name)
        log.writelines('\n')
        count+=1



#srctorrpath  种子集散地
# tartorrpath  待查找种子
def findTorrentByHash(thash,tartorrpath):
    thash=thash.lower()
    #遍历待查找的种子，生成集合
    for dirpath, dirnames, filenames in os.walk(tartorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = Torrent.from_file(torr)
                hashcode=my_torrent.info_hash.lower()
                print('hashcode '+hashcode)
                if thash== hashcode:
                    print("hashcode hash find  "  + '\r\n')
                    print("************************************  " + '\r\n')
                    print(torr)

# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
def filterDownFiles(torrpath, filepath, subDirName):
    # for dirpath, dirnames, filenames in os.walk(filepath):
    #     for dirname in dirnames:
    #         print('dir:   ' +dirname)
    dirList = []
    # 搜集已下载文件列表
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
            dirList.append(filename)
            loger.info('dirname   ' + filename)
        # else:
        #     portion = os.path.splitext(filename)
        #     print('00000  ' + portion[0])
        #     dirList.append(portion[0])

    # clearMacConfigFile(dirList)

    torrDict = geneTorrentDic(torrpath,True)
    torrlist = torrDict.keys()

    # print('dict===='+str(torrDict))
    reset = set(dirList) & set(torrlist)
    # print('dirList'+str(dirList))
    # print('torrlist' + str(torrlist))
    rslist = list(reset)
    loger.info("  =====================  ")
    loger.info(rslist)

    torrDonePath = torrpath + os.path.sep + subDirName + os.path.sep
    mkdirs(torrDonePath)

    finishFilePath = filepath+os.path.sep+subDirName+ os.path.sep
    mkdirs(finishFilePath)

    for samefile in rslist:
        loger.info(" ****   ")
        # print(torrDict[samefile])
        loger.info(os.path.basename(torrDict[samefile]))#文件名
        newTorrFile = torrDonePath + os.path.basename(torrDict[samefile])

        finishFile = finishFilePath + samefile
        # 已经移动了，删除原有的
        if os.path.isfile(newTorrFile):
            loger.error("****************有已经下载过得文件******************")
            loger.error("****************种子文件**************************")
            loger.error(newTorrFile)
            loger.error("****************重复文件**************************")
            loger.error(filepath + os.path.sep + samefile+  finishFile)
            os.remove(torrDict[samefile])
        else:  # 移动种子
            loger.debug("********原种子地址*************")
            loger.debug(torrDict[samefile])
            loger.debug("********新种子地址*************")
            loger.debug(newTorrFile)
            shutil.move(torrDict[samefile], newTorrFile)
            # 文件已经下载过了，重新命名复制
        if os.path.exists(finishFile):
            finishFile = finishFile + '_new'
            # base, ext = os.path.splitext(finishFile)
            # finishFile = f"{base}_new{ext}"  # 修改文件名以避免冲突
            mkdirs(finishFile)
        # 移动完成文件
        shutil.move(filepath + os.path.sep + samefile, finishFile)
        loger.debug("********原文件地址*************")
        loger.debug(filepath + os.path.sep + samefile)
        loger.debug("********新文件地址*************")
        loger.debug(finishFile)
        # 判断pdf是否存在，存在， 转移至新路径
        movePdf(torrDict[samefile], finishFile)
        # 移动完成文件

    loger.info('移动种子文件：' + str(len(rslist)))
# 将种子路径转化为pdf路径
def nameTorr2Pdf(torrfullpath):
    if(torrfullpath  is None):
        return
    else:
        path ,ext=os.path.splitext(torrfullpath)
        pdfpath=path+'.pdf'
        return pdfpath
# 判断pdf是否存在，存在， 转移至新路径
def movePdf(oldpdfpath, tarpath):
    oldpdf = nameTorr2Pdf(oldpdfpath)
    if os.path.isfile(oldpdf):
        # 存在pdf 转移
        pdf_name = os.path.basename(oldpdf)
        shutil.move(oldpdf, tarpath + os.sep + pdf_name)
# 将种子路径转化为pdf路径
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

    torrDict = geneTorrentDic(torrpath,False)
    # todo


# 根据种子路径生成词典  key 种子名称   val 种子路径
# skipTag 是否跳过Y文件夹
def geneTorrentDic(torrpath,skipTag):
    torrlist = []
    torrNamelist = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            if skipTag and dirpath.__contains__('\\y'):  # 跳过已经处理的文件夹中的种子遍历
                print('skip path'+dirpath)
                continue
            else:
                portion = os.path.splitext(filename)
                if portion[1] == ".torrent":
                    torr = os.path.join(dirpath, filename)
                    # print('torr=='+torr)
                    my_torrent = loadTorr(torr)
                    if my_torrent is None:
                        continue
                    torrlist.append(my_torrent.name)
                    torrNamelist.append(torr)

    #返回字典对象 ，key 种子文件路径  种子对应下载文件列表
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
    txtfile = log(filepath, '',True)

    len = 1024 * 1024
    hundredmb=100*len
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("=================================" + '\r')
            torname=repr(portion)#解决包含转义字符的问题
            txtfile.writelines(torname)
            print("=================================")
            print(portion)
            # 如果后缀是.xltd  用于解决下载99%的问题，
            # 但考虑到会有下载99%异常的问题，关闭此功能
            # if portion[1] == ".xltd":
            #     print("need change")
            #     newnamee = portion[0].replace('.bt', '')
            #     os.renames(filepath + portion[0] + portion[1], filepath + newnamee)
            if portion[1] == ".torrent":
                print("================torrent conteng=================" + '\r\n')
                print(torr)
                txtfile.writelines(torr + '\r\n')
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                txtfile.writelines(my_torrent.info_hash + '\r\n')
                tlen = my_torrent.total_size / len
                txtfile.writelines(str(tlen) +'mb'+ '\r\n')

                # print(my_torrent.total_size / len)
                # print(my_torrent.comment)
                print(str(my_torrent.files)+ '\r\n')
                print(portion[0] + '          ' + my_torrent.name)
                for torrfile in my_torrent.files:
                    if (torrfile.length > hundredmb):
                        tlen=round(torrfile.length / len, 2)
                        txtfile.writelines(str(tlen) +'mb'+ '\r\n')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()
    #对比文件完成度
# def comparefiles(torrpath, downfilesdir,threadid):
#
#     txt = log(torrpath, 'compare'+threadid,True)
#     txt.writelines('*****************'+downfilesdir+'*****************\r\n')
#     for dirpath, dirnames, filenames in os.walk(torrpath):
#         for filename in filenames:
#             looptag = False
#             portion = os.path.splitext(filename)
#             if portion[1] == ".torrent":
#                 torr = os.path.join(dirpath, filename)
#                 # print('torr==' + torr)
#                 my_torrent = Torrent.from_file(torr)
#                 tfiles = my_torrent.files
#                 if (tfiles is not None):
#                     for file in tfiles:
#                         torrentpath = file.name
#                         if (findstr in torrentpath):
#                             if looptag:
#                                 break
#                             str = torrpath + filename
#                             txt.writelines('*****************')
#                             txt.writelines('\n')
#                             txt.writelines('dirpath' + dirpath)
#                             txt.writelines('\n')
#                             txt.writelines('----------------------')
#                             txt.writelines(torrpath + filename)
#                             torrentFiles2str(tfiles, txt)
#                             # txt.writelines('tfiles' + str(tfiles))
#                             looptag = True
#     txt.close()

filterfileArray=['小黄片.mht',
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
'( 1024社区手机网址发布器 3.0 ).apk',
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


]

#用来扫描half文件夹下所有待扫描的半下载文件
# downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def countHalfFiles(downdir,deltag):
    for root, dirs, files_list in os.walk(downdir):
        for file_name in files_list:
            if file_name.endswith('torrent'):
                tfile=os.path.join(root, file_name)
                loger.info("tfile:"+tfile)
                loger.info("root:"+root)
                comparefiles(tfile,root,deltag)

dlcheck = DownLoadCheck()
dlcheck.merge_blacklists(r".", "bl.json",False)
blacklist=dlcheck.load_blacklist(r"bl.json")

    #tfiles 种子里的文件，
    #downdir 下载目录，包含了种子文件的头目录
    # deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
    #todo  写日志
def comparefiles(tfile,downdir,deltag):
    # txtfile = log(downdir, '---comparefiles',False)
    loger.debug('tfile  ' + tfile + '\r\n')
    loger.debug('downdir  ' + downdir + '\r\n')
    loger.debug('downdir  ' + downdir)
    torrentmap = {}
    my_torrent = Torrent.from_file(tfile)

    for file in my_torrent.files:  # 遍历种子文件
        ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
        tfilename = file.name.replace('\\\\', '\\')
        # print('tfilename'+tfilename)
        #截取359目录，由于可能会改名，所以
        try:
            subpath = tfilename.split('\\', 1)[1]
        except IndexError:
            print('subpath is none ==>'+tfilename)
            continue
        if subpath.__contains__('\\'):
            subname = subpath.split('\\', 1)[1]
        else:
            subname=subpath
        #subpath \尖叫视频.mht
        #print('subpath'+str(subpath))
        if subname in blacklist:
            continue
        if subname not in filterfileArray:
            if subname.__contains__('如果您看到此文件，请升级到BitComet'):
                loger.info(subname)
            else:
                loger.debug("subpath :" + subpath)
                torrentmap.setdefault(subpath, file.length)
        ## 待增加过滤无用文件实现




    downloadmap={}
    m=1024*1024
    for dirpath, dirnames, filenames in os.walk(downdir):
        # txtfile.writelines('dirpath'+dirpath + '\r\n')
        # print('dirpath'+dirpath)
        # print('dirnames' + dirnames)
        for filename in filenames:
            portion = os.path.splitext(filename)
            #print("portion[1] "+portion[1])

            if deltag and filename.endswith(xunleisuffix):
                fullname = os.path.join(dirpath, filename)
                os.remove(fullname)
            elif portion[1] != ".bt":#处理待下载文件，
                fullname= os.path.join(dirpath, filename)
                fsize=os.path.getsize(fullname)
                #print("full path:"+fullname)
                # fullname=os.path.join(dirpath, ' '+filename)#torrent的file会有空格， 很奇怪
                torrfilepath=fullname.replace(downdir ,'')
                torrfilepath = clearPath(torrfilepath)
                #print("size"+str(round(fsize/m,2))+'mb')
                downloadmap.setdefault(torrfilepath,fsize)#生成文件列表

        #print(tfilename)
        #print(str(file))
    downloadfilelist = list(downloadmap.keys())
    tfiellist=list(torrentmap.keys())
    loger.debug('downloadfilelist'+str(len(downloadfilelist))+'   '+ '\r\n')#+str(downloadfilelist)
    # for dfile in downloadfilelist:
    #print('tfiellist bf' + str(len(tfiellist)) + '   ' + str(tfiellist))
    tfiellist=getUndownFileList(tfiellist,downloadfilelist)
    # if deltag:
    #     for cleanfile in downloadfilelist:
    #         if cleanfile in tfiellist and cleanfile.endswith(xunleisuffix):
    #             print('cleanfile del' + cleanfile)
    #             tfiellist.remove(cleanfile)

    downloadfilesize=0#待下载文件总大小
    loger.debug("********************v1.0 待下载文件列表"+ str(len(tfiellist))+"个***************************"+ '\r\n')

    if tfiellist is None or len(tfiellist)==0:
        return
        # 未完成的文件列表，新建文件打印
    else:
        undone_file = log("" + downdir, '--undone', False)
        tfiellist = set(tfiellist)
        tfiellist_namelist = list()
        for needdownfile in tfiellist:

            tfsize=torrentmap.get(needdownfile)
            downloadfilesize+=tfsize
            tfsize =round(tfsize / m, 2)
            fname = os.path.basename(needdownfile)
            tfiellist_namelist.append(fname)
            undone_file.writelines("\"" + fname + "\"," + '\r\n')

        undone_file.writelines('总占用空间":' + str(round(downloadfilesize / m, 2)) + "mb" + '\r\n')
        undone_file.close()
        dlcheck.gen_blacklist(tfiellist_namelist, None)

#解决py3.7 兼容性问题，py3.10可以不使用此方法
def clearPath(tfilepath):
    if str(tfilepath).startswith('\\'):
        return tfilepath[1:]
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
fdmsuffix='.fdmdownload'
def clearXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix) or filename.endswith(fdmsuffix):
                fullname=os.path.join(dirpath,filename)
                try:
                    loger.info('file: '+fullname)
                    os.remove(fullname)
                except UnicodeEncodeError:
                    # non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    # fullname=fullname.translate(non_bmp_map)
                    loger.info('full: ' + fullname)
                    os.remove(fullname)


if __name__ == '__main__':
    # test()
    #getTorrDetail(r'D:\temp\0555\2022-03-01\1229\hj')
    #os._exit(0)
    # lger.info('C5AEA8F99A520790D421FEB7162DDF7A77BD297B'.lower())
    # strlist=['爱剪辑-48.avi']
    # findTorrListByStr(strlist,'D:\\temp\\0555\\2022-03-01\\0555\\')
    # findTorrListByStr(strlist, 'D:\\temp\\0555\\2022-03-01\\0555\\b20\errfiles\\')

    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b30\\")
    # os._exit(0)
    # findTorrentByHashcodeInDir("D:\\temp\\0555\\2022-03-01\\",
    # "D:\\temp\\backup\\find\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b25\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\normal\\")

    # countHalfFiles(r'g:\down\0555\b43f\un',True)
    # countHalfFiles(r'G:\down\0555\b31\undone',True)
    #countHalfFiles(r'G:\down\0555\b37', True)

    # countHalfFiles(r'E:\down\0555\b43f\half',True)
    # filterDownFiles(r'C:\torrent\b43', r'g:\down\0555\b43f\half', 'half')
    # filterDownFiles(r'C:\torrent\b43', r'e:\down\0555\b43f\half', 'half')
    # countHalfFiles('d:\\down\\0555\\b42\\half\\',True)
    # genhalfTorrent('D:\\temp\\chachong\\')
    # filterDownFiles(r'D:\temp\b31', r'D:\temp\sp', 'y')
    # writeTorrDetail('D:\\360Downloads\\1228\\')
    # clearXunleiFile("G:\\down\\0555\\b40\\half\\")

    filterDownFiles(r'F:\2022-03-01\0555\b44', r'F:\down\0555\b44\un', 'y')
    countHalfFiles(r'F:\down\0555\b44\un\y', True)
    os._exit(0)
    # filterDownFiles(r'C:\torrent\b40', r'G:\down\0555\b40\half', 'halfing')
    # filterDownFiles(r'C:\torrent\b40', r'G:\down\0555\b40\stop', 'stop')
    filterDownFiles(r'C:\torrent\b43', r'g:\down\0555\b43f\un', 'y')
    filterDownFiles(r'C:\torrent\b43', r'e:\down\0555\b43f\un', 'y')
    filterDownFiles(r'C:\torrent\b42', r'd:\down\0555\b42\un', 'y')
    filterDownFiles(r'C:\torrent\b42', r'F:\down\0555\b42\un', 'y')

    filterDownFiles(r'C:\torrent\b40', r'G:\down\0555\b40\un', 'y')
    filterDownFiles(r'C:\torrent\b39', r'E:\down\0555\b39\un', 'y')
    filterDownFiles(r'C:\torrent\b40', r'F:\down\0555\b40\un', 'y')
    # getTorrDetail(r'C:\torrent\b39')
    # getTorrDetail(r'C:\torrent\b43')
    os._exit(0)


    # filterBigfiles('D:\\Program20190718\\2022-03-01\\1229\\1\\', 2000)
    # filterBigfiles('D:\\Program20190718\\2022-03-01\\1229\\5\\', 2000)
    # findTorrentByDirName('D:\\temp\\0555\\', 'Irisadamsone','thread-1')
    # findTorrentByDirName('D:\\temp\\0555\\2022-03-01\\0555\\', '373P', 'thread-21')
    # findTorrentByDirName('D:\\temp\\0555\\', '长腿高跟 脸穴同框自慰玩穴 开档骚丝袜 高清7', 'thread-1')
    # findTorrentByDirName('D:\\temp\\0555\\', '长腿高跟 脸穴同框自慰玩穴 开档骚丝袜 高清7','thread-1')


    # os._exit(0)

    #comparefiles("D:\\temp\\0555\\2.torrent","D:\\temp\\0555\\259\\")
    # filename="STP31812 穿情趣裝的美女狐狸精,全程露臉妩媚誘人,聽狼友指揮互動撩騷,揉奶玩逼自慰呻吟,表情好騷火辣豔舞別錯過"
    # print(repr(filename))
    # tormd5("C:\\Users\\Administrator\\Downloads\\best\\推特网红大屁股骚货kbamspbam，怀孕了还能挺着个大肚子拍照拍视频挣钱，太敬业了，奶头变黑 但白虎粉穴依然粉嫩.torrent")
    # os._exit(0)
    #getTorrDetail('D:\\temp\\0555\\')
    # getTorrDetail('D:\\Program20190718\\2022-03-01\\0555\\best\\')

    # removeFiles('H:\\down\\0333\\1\\un\\y\\')
    # removeFiles('H:\\down\\0323\\best\\un\\y\\')
    # removeFiles('J:\\done\\')
    # removeFiles('I:\\done\\')
    # removeFiles('h:\\done\\')
    # filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\20\\', 'I:\\down\\1229\\20\\un\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1119\\',
                    'I:\\down\\1119\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0322\\hj\\',
                    'I:\\down\\0322\\HJ\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0333\\best\\',
                    'H:\\down\\0333\\best\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0333\\best\\',
                    'J:\\down\\0333\\best\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0333\\best\\',
                    'I:\\down\\0333\\best\\un\\', 'y\\')

    filterDownFiles('D:\\Program20190718\\2022-03-01\\0333\\1\\',
                    'J:\\down\\0333\\1\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0333\\hj\\',
                    'J:\\down\\0333\\hj\\un\\', 'y\\')

    filterDownFiles('D:\\Program20190718\\2022-03-01\\0323\\',
                    'H:\\down\\0323\\best\\un\\', 'y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\0323\\',
                    'I:\\down\\0323\\un\\', 'y\\')

    filterDownFiles('D:\\Program20190718\\2022-03-01\\0555\\best\\',
                    'K:\\down\\0555\\best\\un\\', 'y\\')

    '''
    
    
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1117\\',
                  'H:\\down\\1117\\un\\','y\\')
    
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1112\\',
                  'J:\\down\\1112\\un\\','y\\')
    
        
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\5\\',
                  'I:\\down\\1229\\5\\un\\','y\\')
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\1\\',
                  'I:\\down\\1229\\1\\un\\','y\\')
    
    
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\13\\',
                  'I:\\down\\1229\\13\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\1\\',
                        'I:\\down\\1229\\1\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\5\\',
                        'I:\\down\\1229\\5\\un\\')
        '''

    # editXunleiFile('J:\\done\\1102\\字母界女神『荟萃』带坏淫戏调教母狗 露出训犬捆绑 调教金属光泽闪耀M奴之心 高清\\【极品稀缺 美乳】字母界女神『荟萃』带坏淫戏调教母狗')
    # getDulicateFiles()
    # getTorrDetail('D:\\temp\\593254315050521\\1024\\')
    # getTorrDetail('D:\\Program20190718\\2022-03-01\\1102\\')
    # getTorrDetail('D:\\Program20190718\\2022-03-01\\1228\\other\\')
    # writeTorrDetail('D:\\Program20190718\\2022-03-01\\1229\\')
    # getTorrDetail('D:\\Program20190718\\2022-03-01\\1102\\')
    #   filterDownFiles('D:\\Program20190718\\2022-03-01\\1201\\03\\',
    #              'I:\\down\\1201\\3\\un\\')

    # filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\11\\',
    #          'I:\\down\\1229\\11\\un\\')

    '''
      filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\12\\',
                  'J:\\down\\1229\\12\\un\\')
    
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\11\\',
                  'I:\\down\\1229\\11\\un\\')
    
    
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\9\\',
                  'I:\\down\\1229\\9\\
    filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\9\\',
                  'I:\\down\\1229\\9\\un\\')
    
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\10\\',
                  'I:\\down\\1229\\10\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\12\\',
                  'J:\\down\\1229\\12\\un\\')
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\13\\',
                  'I:\\down\\1229\\13\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\7\\',
                        'J:\\down\\1229\\7\\un\\')
    
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\1\\',
                  'I:\\down\\1229\\1\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\2\\',
                  'I:\\down\\1229\\2\\un\\')
    
        filterDownFiles('D:\\Program20190718\\2022-03-01\\1102\\',
                  'J:\\down\\20220301\\1102\\un\\') '''
# filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\3\\',
#              'J:\\down\\1228\\3\\un\\')
# filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\1\\', 'I:\\down\\1229\\1\\un\\')


# filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\12\\', 'J:\\down\\1229\\12\\un\\')
# filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\10\\', 'I:\\down\\1229\\10\\un\\')
# filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\11\\', 'I:\\down\\1229\\11\\un\\')

# filterDownFiles('D:\\Program20190718\\2022-03-01\\1229\\6\\', 'I:\\down\\1229\\6\\un\\')

# filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\5\\',
#              'I:\\down\\1228\\5\\un\\')
#   filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\7\\',
#                'I:\\down\\1228\\7\\un\\')
# filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\9\\','J:\\down\\1228\\9\\un\\')
#    filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\6\\','H:\\down\\1228\\6\\un\\')
# filterDownFiles('D:\\Program20190718\\2022-03-701\\1228\\10\\',
#                'I:\\down\\1228\\10\\un\\')

# filterDownFiles('D:\\Program20190718\\2022-03-01\\1228\\8\\',
#               'H:\\down\\1228\\8\\un\\')


# getTorrentByDetails('给哥哥买了新工具','D:\\temp\\593254315050521\\alltorr')


# removeFiles('I:\\done\\')
# removeFiles('I:\\down\\0322\\best2\\un\\y\\')
# removeFiles('H:\\done\\')
# removeFiles('I:\\down\\1229\\19\\un\\y\\')
# removeFiles('J:\\done\\')
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
