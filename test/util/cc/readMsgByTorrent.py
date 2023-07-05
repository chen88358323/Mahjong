from torrentool.api import Torrent
import os
import platform
import  shutil

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

if __name__ == '__main__':
    # getDulicateFiles()
    # getTorrDetail('D:\\temp\\593254315050521\\1024\\')
    # getTorrDetail('D:\\temp\\best2\\best4\\')
    #getTorrDetail('D:\\360Downloads\\1228\\')
    # writeTorrDetail('D:\\temp\\1228\\')
    filterBigfiles('D:\\360Downloads\\test\\', 1000)
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
