# -*- coding: utf-8 -*-
import shutil
import hashlib
import os,time,mmap
from moviepy.video.io.VideoFileClip import VideoFileClip
# 相关的信息摘要算法
#显示文件单位 300M
bigsize = 300 * 1024 * 1024
big_file_read_size=100 * 1024 * 1024
msize=1 * 1024 * 1024
siteStr=['gc2048.com-','gc2048.com','rh2048.com','hhd800.com@',
         'hhd800.com','aavv38.xyz@','aavv38.xyz','kcf9.com-','@']
entertag='\r\n'
msize = 1 * 1024 * 1024
osseparator = os.path.sep
def clearDirName(clearPath):
    txt = log(clearPath, 'clearDirName', True)
    for dirpath, dirnames, filenames in os.walk(clearPath):
        for dirname in dirnames:
            for str in siteStr:
                if(dirname.startswith(str)):
                    newdirname=dirname.replace(str,'')
                    if len(newdirname)==0:#如果文件夹只是违禁网站，跳过
                        txt.writelines('******************'+entertag)
                        txt.writelines('存在重复文件'+dirname+entertag)
                        txt.writelines('******************'+entertag)
                        continue
                    if(newdirname in dirnames):#存在重复文件

                        txt.writelines('dirnames =>'+dirname+entertag)
                        txt.writelines('newdirname =>'+newdirname+entertag)
                    else:#不存在重复文件直接修改命名
                        txt.writelines('rename dir is done  ' + dirname+entertag)
                        fullpath = os.path.join(dirpath, dirname)
                        tarpath = os.path.join(dirpath, newdirname)
                        txt.writelines('dirnames =>' + fullpath+entertag)
                        txt.writelines('newdirname =>' + tarpath+entertag)

                        if os.path.exists(fullpath):
                            os.renames(fullpath,tarpath)
    txt.close()

#倒序排列文件列表
def get_oswalk_desc(path):
    # 创建一个空列表来存储遍历的结果
    walk_results = []

    # 遍历目录树，并将结果添加到列表中
    for dirpath, dirnames, filenames in os.walk(path):
        walk_results.append((dirpath, dirnames, filenames))
    # 对列表进行排序，这里假设我们想要根据目录路径进行排序
    walk_results.sort(key=lambda x: x[0], reverse=True)
    # 现在 walk_results 是按照目录路径倒序排列的
    return  walk_results
def clearFileName(clearPath):
    txt = log(clearPath, 'clearFileName', True)
    for dirpath, dirnames, filenames in os.walk(clearPath):
        for f in filenames:
            for str in siteStr:
                if(f.startswith(str)):
                    newfilename=f.replace(str,'')
                    if len(newfilename)==0:#如果文件夹只是违禁网站，或者替换后较短
                        continue
                    if(newfilename in filenames):#存在重复文件

                        txt.writelines('filename =>'+f+entertag)
                        txt.writelines('newfilename =>'+newfilename+entertag)
                    else:#不存在重复文件直接修改命名

                        fullpath=os.path.join(dirpath, f)
                        tarpath=os.path.join(dirpath, newfilename)
                        txt.writelines('rename dir is done  ' + f+entertag)
                        txt.writelines('filename =>' + fullpath+entertag)
                        txt.writelines('newfilename =>' + tarpath+entertag)
                        if os.path.exists(fullpath):
                            os.renames(fullpath,tarpath)
    txt.close()


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
def removeDulicateFiles(fpath):
    prefix = '(1).jpg'
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            absPath = dirpath + filename
            if (absPath.endswith(prefix)):
                print(absPath)
                if os.path.exists(absPath):
                    os.remove(absPath)
def removeGarbageFiles(filepath):
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
             '解压错误请下载。原版无水印资源.txt',
             '暗香阁地址发布页.html',
             '暗香阁，暗香阁综合论坛，宅男资源搬运工 .html',
             '1t.jpg',
             '乐鱼体育-500223.com .mp4',
             '18s18 (44).jpg','下载教程.HTML',
             '关注Telegram电报频道不迷路.txt',
             '动漫游戏.HTML',
             '套图写真.HTML',
             '小说语音.HTML',
             '日韩欧美.HTML',
             '更多资源.rar',
             '最新自拍.HTML',
             '资源更新发布页地址（重要！！！！！请牢记）_副本.txt',
             '防和谐地址发布页_副本.url',
             '1t.jpg',
             '(  最新bt合集_3.0 ).html',
             '(  1024社区最新地址_3.0 ).htm',
             'gc2048.com-最新找回家包zz--保存收录很方便.txt',
             '1024草榴社區t66y.com.txt',
             '1080fuli@草榴社区.txt',
             'jialovexx@www.SexInSex.net 2016色中色地址收藏.txt',
             '免费观看油管，推特软件，让世界零距离.url',
             '收藏不迷路。原版无水印-网络热搜门事件，每日更新！.url',
             'limbowu@www.SexInSex.net 2016色中色地址收藏.txt',
             '关注Telegram电报频道不迷路.txt',
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
             'sbw99.cc---paco---CC.jpg','sis百万国产原创作品.png',
             '2048八社区扫码获取地址.png',
             'SIS.jpg',
             '抖淫短视频边看边赚钱的APP.png',
             '饿了么.png',
             '(_1024免翻 地址发布.chm',
             '.DS_Store',
             '2048地址发布器PC版.rar','★★★★美女在线一对一，免费试看.gif',
             '同城一YQ交友.gif',
             '台湾美女主播.jpg','2048 新片首发 每天更新 同步日韩.htm',
             '激情隨時看.gif','_萌萝社.jpg.bt.xltd','草榴社區.url','_1024精品无码大包种子.html',
             '海量高清美女图片地址访问.gif','SexInSex! BoardSexInSex! Board(正版SIS主域名：www.sexinsex.net）.url',
             '美女荷官竟然被....vip1196.mp4','(_2048免翻墙地址发布.htm','(_2048综合论坛最新地址.htm',
             '美女直播.mp4', '美女一对一.gif','規懶趴會 @ 伊莉論壇 -.txt.bt.xltd',
             '灣搭拉咩拉 @ 伊莉論壇.txt.bt.xltd', '灣搭拉咩拉 @ 無限討論區', '規懶趴會 @ 伊莉論壇 -.txt.bt.xltd',
             '(_1【av8.la】。原版无水印-网络热搜门事件，每日更新！.mhtml'
             ]

    # .textClipping 后缀
    # prefix='(1).jpg'
    osseparator = os.path.sep
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath + osseparator + filename
                print(absPath)
                os.remove(absPath)
            # torr = os.path.join(dirpath, filename)
            # absPath = dirpath + filename
            # if(absPath.endswith(prefix)):
            #     print(absPath)
#scanSpecifFile + scanZeroSizeVideo
def scanZeroAndSpecifFile(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            for prefix in filepefix:
                if(filename.endswith(prefix)):
                    fullfilepath = os.path.join(dirpath, filename)
                    print('findfile: '+fullfilepath)
                    break
            for prefix in videoType:
                fullfilepath = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(fullfilepath)  # 文件原本大小
                except FileNotFoundError:
                    print("发生异常，文件打不开:" + filename)
                if (filename.endswith(prefix) and size == 0):
                    print('findfile: ' + fullfilepath)
                    break


filepefix = ['bt.xltd', 'torrent', 'textClipping']
def scanSpecifFile(fpath):

    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            for prefix in filepefix:
                if(filename.endswith(prefix)):
                    fullfilepath = os.path.join(dirpath, filename)
                    print('findfile: '+fullfilepath)
                    break
videoType = ['.avi', '.mp4', '.ts', '.flv', '.mkv', '.mov', '.rmvb', '.rm', '.mpeg', '.wmv']
def scanZeroSizeVideo(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            for prefix in videoType:
                fullfilepath = os.path.join(dirpath, filename)
                if (filename.endswith(prefix) and os.path.getsize(fullfilepath) == 0):
                    print('findfile: ' + filename)
                    break
#对比差异文件
def dirDiff(srcDir,tarDir):
    srcMap=getDicFromDir(srcDir)
    tarMap=getDicFromDir(tarDir)

    srcmapcopy=srcMap.copy()
    tarmapcopy=tarMap.copy()

    keylist = list(set(tarMap.keys()) & set(srcMap.keys()))
    for k in keylist:
        srcmapcopy.pop(k)
        tarmapcopy.pop(k)
    print('**************************************************************')
    print('处理前 '+str(len(srcMap))+'个处理后 '+str(len(srcmapcopy))+'个   在'+srcDir)
    print('处理前 '+str(len(tarMap))+'个处理后 ' +str( len(tarmapcopy) )+ '个   在' + tarDir)
    map={}
    map.update(srcmapcopy)
    map.update(tarmapcopy)
    print('合并后 map总长度' + str(len(map)))
    for(key ,val ) in map.items():
        print('val:' + val)
        # print('key' + str(key))



#根据目录路径生成 code ,filepath的map
def getDicFromDir(fpath):
    hclist =[]
    namelist=[]
    filemap={}
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            fullfilepath = os.path.join(dirpath, filename)
            hcode=calc_file_hash(fullfilepath)
            hclist.append(hcode)
            namelist.append(fullfilepath)
    if(len(hclist)>0 and len(hclist)==len(namelist)):
        filemap=dict(zip(hclist,namelist))
    return filemap
def scanSmlFile(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            fullfilepath = os.path.join(dirpath, filename)
            filesize = round(os.path.getsize(fullfilepath) / msize, 4)
            if filesize<=0.0001:
                print(fullfilepath)


defaultHcode='1111111111111111'
def calc_file_hash(filename):
    size =0
    try:
        size=os.path.getsize(filename) #文件原本大小
    except FileNotFoundError:
        print("发生异常，文件打不开:"+filename)
        return defaultHcode
    fsize = round(size / msize, 4)#格式化后的实际大小
    fsize =str(fsize)
    if size==0:
        print("zero file " + filename + ' size:' + str(size))
        return  defaultHcode
    md5hasher = hashlib.md5()
    ''' 
    Calculate the file hash.
    In order to have better performance, if the file is larger than 4MiB,
    only the first and last 100MiB content of the file will take into consideration
    '''
    if size <= bigsize:
        with open(filename, "rb") as f:
            with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mmapfile:
                md5hasher.update(mmapfile)
                hcode=md5hasher.hexdigest()
                print(hcode + '   ' + fsize + 'Mb     ' + filename)
                return md5hasher.hexdigest(),fsize
    else:
        with open(filename, 'rb') as f:
         #偏移量，大于300M的文件，读取前100M以及最后面的100M
            md5hasher.update(f.read(big_file_read_size))
            f.seek(size - big_file_read_size)
            md5hasher.update(f.read(big_file_read_size))
            hcode = md5hasher.hexdigest()
            print(hcode + '   ' + fsize + 'Mb     ' + filename)
            return hcode,fsize

def cutVideoHead(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            fullfilepath = os.path.join(dirpath, filename)
            newfile=os.path.join(dirpath,'改'+filename)
            filesize = round(os.path.getsize(fullfilepath) / msize, 4)
            if filesize>0:

                # 创建视频剪辑
                video = VideoFileClip(fullfilepath)
                # 剪辑开头2秒钟的视频
                video_cut = video.subclip(30)

                # 保存新视频文件
                video_cut.write_videofile(newfile)
                print(newfile)


if __name__ == '__main__':
    cutVideoHead('I:\\done\\daifenlei\\《震撼精品 推薦》私密資源交換區Q群'
                 '貼吧T群内部收集整理各種反差婊母狗自拍不雅視圖美女如雲基本露臉短小精悍637P 295V\\视图\\V\\1')
    # clearDirName('D:\\temp\\dist\\')
    # removeDulicateFiles('D:\\temp\\593254315050521\\')
    dirDiff('D:\\360Download\\2\\','D:\\360Download\\仓鼠管家\\')
    # scanSmlFile("/media/cc/MOIVESOFT/")
    # scanSmlFile("/media/cc/PJYP/")
    # scanSmlFile("/media/cc/ZP/")
    # scanSmlFile("/media/cc/娱乐/")
    # scanSmlFile("/media/cc/文档/")
    # scanSmlFile("/media/cc/系统/")
    # scanSmlFile("/media/cc/软件/")

    # removeGarbageFiles("I:")
    # removeGarbageFiles("J:")
    # removeGarbageFiles("K:")
    # removeGarbageFiles("L:")
    # removeGarbageFiles("M:")
    # removeGarbageFiles("N:")
    # removeGarbageFiles("X:")


    # removeGarbageFiles("/media/cc/MOIVESOFT/")
    # removeGarbageFiles("/media/cc/PJYP/")
    # removeGarbageFiles("/media/cc/ZP/")
    # removeGarbageFiles("/media/cc/娱乐/")
    # removeGarbageFiles("/media/cc/文档/")
    # removeGarbageFiles("/media/cc/系统/")
    # removeGarbageFiles("/media/cc/软件/")
    # clearDirName('/media/cc/文档/of/minichu/')
    # clearFileName('/media/cc/PJYP/daifenlei/1228-6/牛人约炮大神『浮生若梦』最新日常性爱分享 调教啪啪人妻少妇 极品身材 完美露脸高清 / P / ')
    # removeDupFile('/media/cc/文档/of/露脸才是王道！万人求购Onlyfans甜美女神网红反差婊babyss顶级私拍被金主各种玩肏/P/')