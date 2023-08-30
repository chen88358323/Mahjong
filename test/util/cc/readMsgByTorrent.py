from torrentool.api import Torrent
import os
import  shutil
import mysqlTemplate as dbtool
import time
import queue,threading
from typing import Any, Tuple
def removeFiles():
    filepath = 'D:\\temp\\593254315050521\\demo\\'
    array=['【01axg.xyz】.jpg','02AXG.XYZ.png','03axg.XYZ.png','04axg.xyz.png','05axg.xyz.png']
    prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath +"\\"+ filename
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
            txtfile.writelines(portion)
            # print("=================================")
            # print(portion)
            # 如果后缀是.xltd
            if portion[1] == ".xltd":
                print("need change")
                newnamee=portion[0].replace('.bt','')
                os.renames(filepath+portion[0]+portion[1],filepath+newnamee)
            if portion[1] == ".torrent":
                # print(torr)
                txtfile.writelines(torr+'\r')
                my_torrent = Torrent.from_file(torr)
                tlen=my_torrent.total_size / len
                txtfile.writelines(str(tlen)+'\r')
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
    batchlen = 10
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

                my_torrent = Torrent.from_file(torr)
                hash = my_torrent.info_hash
                path = os.path.dirname(torr)
                tobj = [hash, path, filename]
                datalist.append(tobj)
                if i == batchlen:
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
            # count+=1
            print("dbqueue is empty")
            time.sleep(3)
        else:
            datalist=dbqueue.get()
            count+=10
            if(count>3000):
                print("")
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
                writer = log("D:\\temp\\0555\\", "findDupulicate", True)
                writer.writelines("*************************" + '\r\n')
                writer.close()
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

            dbtool.recorderDulicateTorrent(tar[0],tar[1],tar[2])
            return  False


def log(filepath, name,append):
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
#根据路径名扫描入库
def scanTorrentsIntoDB(torrDir):
    p1 = threading.Thread(target=getTorListByDir, args=(torrDir,))

    p1.start()
    time.sleep(3)
    c1 = threading.Thread(target=converDatalist2DB)
    c1.start()



# def test():
#     list1=[[1,2,3],[45,6,7],[8,65,44]]
#     list2=[2,33,44,55,66]
#     for l in list1:
#         if l[1] in list2:
#             list1.remove(l)
#     print("list1"+str(list1))
if __name__ == '__main__':
    #test()
    #scanTorrentsIntoDB("D:\\temp\\0555\\t\\")
    scanTorrentsIntoDB("C:\\Users\\Administrator\\Downloads\\best\\")

    # scanTorrentsIntoDB("D:\\temp\\0555\\t\\0555\\b12\\")
    # tormd5("C:\\Users\\Administrator\\Downloads\\best\\推特网红大屁股骚货kbamspbam，怀孕了还能挺着个大肚子拍照拍视频挣钱，太敬业了，奶头变黑 但白虎粉穴依然粉嫩.torrent")
    #os._exit(0)
    # getDulicateFiles()
    # getTorrDetail('D:\\temp\\593254315050521\\1024\\')
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
