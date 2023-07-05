# -*- coding: utf-8 -*-
from torrentool.api import Torrent
import os
import platform
import shutil


def removeFiles(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
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
             '解压错误请下载。原版无水印资源.txt'

             ]
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
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith('.bt.xltd'):
                print('dirpath:' + dirpath)
                new = filename.replace(".bt.xltd", "")
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
                my_torrent = Torrent.from_file(torr)
                fileSize = my_torrent.total_size
                print('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr, torrBigFilePath + filename)
                    print('大文件')
                    bigfiles.append(my_torrent.name)
    print('bigfiles size:' + str(len(bigfiles)))
    print('bigfiles:' + str(bigfiles))


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
            print('dirname   ' + filename)
        # else:
        #     portion = os.path.splitext(filename)
        #     print('00000  ' + portion[0])
        #     dirList.append(portion[0])

    # clearMacConfigFile(dirList)

    torrDict = geneTorrentDic(torrpath)
    torrlist = torrDict.keys()

    # print('dict===='+str(torrDict))
    reset = set(dirList) & set(torrlist)
    # print('dirList'+str(dirList))
    # print('torrlist' + str(torrlist))
    rslist = list(reset)
    print("  =====================  ")
    print(rslist)

    torrDonePath = torrpath + subDirName
    mkdirs(torrDonePath)

    finishFilePath = filepath + subDirName
    mkdirs(finishFilePath)

    for samefile in rslist:
        print(" ****   ")
        # print(torrDict[samefile])
        print(os.path.basename(torrDict[samefile]))
        newTorrFile = torrDonePath + os.path.basename(torrDict[samefile])

        finishFile = finishFilePath + samefile
        # 已经移动了，删除原有的
        if os.path.isfile(newTorrFile):
            os.remove(torrDict[samefile])
        else:  # 移动种子
            shutil.move(torrDict[samefile], newTorrFile)
        # 移动完成文件
        shutil.move(filepath + samefile, finishFile)
        print('finishFile:' + finishFile)

    print('移动种子文件：' + str(len(rslist)))

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
        print('mkdir:' + path)
        os.mkdir(path)


def getTorrDetail(filepath):
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + '.txt'
    print('basename==>' + basename)
    print('dirname==>' + dirname)
    print('txtfile===>' + txtpath)

    txtfile = open(txtpath, 'w+', encoding='utf-8')

    len = 1024 * 1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("=================================" + '\r')
            txtfile.writelines(portion)
            print("=================================")
            print(portion)
            # 如果后缀是.xltd
            if portion[1] == ".xltd":
                print("need change")
                newnamee = portion[0].replace('.bt', '')
                os.renames(filepath + portion[0] + portion[1], filepath + newnamee)
            if portion[1] == ".torrent":
                print(torr)
                txtfile.writelines(torr + '\r')
                my_torrent = Torrent.from_file(torr)
                tlen = my_torrent.total_size / len
                txtfile.writelines(str(tlen) + '\r')
                # print(my_torrent.total_size / len)
                # print(my_torrent.comment)
                print(portion[0] + '          ' + my_torrent.name)
                for torrfile in my_torrent.files:
                    if (torrfile.length > 100 * len):
                        txtfile.writelines(str(torrfile) + '\r')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()


if __name__ == '__main__':
    # filterBigfiles('D:\\Program20190718\\2022-03-01\\1229\\1\\', 2000)
    # filterBigfiles('D:\\Program20190718\\2022-03-01\\1229\\5\\', 2000)

    # getTorrDetail('D:\\Program20190718\\2022-03-01\\1119\\')
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
