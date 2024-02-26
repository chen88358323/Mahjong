# -*- coding: utf-8 -*-
import shutil
import os
siteStr=['gc2048.com-','gc2048.com','rh2048.com','hhd800.com@',
         'hhd800.com','aavv38.xyz@','aavv38.xyz','@']
entertag='\r\n'
msize = 1 * 1024 * 1024
osseparator = os.path.sep
def clearDirName(clearPath):
    txt = log(clearPath, 'duplicate dirs', True)
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

def clearFileName(clearPath):
    txt = log(clearPath, 'duplicate filenames', True)
    for dirpath, dirnames, filenames in os.walk(clearPath):
        for f in filenames:
            for str in siteStr:
                if(f.startswith(str)):
                    newfilename=f.replace(str,'')
                    if len(newfilename)==0:#如果文件夹只是违禁网站，跳过
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
             '(_1024免翻 地址发布.chm'
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

def scanSmlFile(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath):
        for filename in filenames:
            fullfilepath = os.path.join(dirpath, filename)
            filesize = round(os.path.getsize(fullfilepath) / msize, 4)
            if filesize<=0.0001:
                print(fullfilepath)

if __name__ == '__main__':
    clearDirName('D:\\temp\\dist\\')
    removeDulicateFiles('D:\\temp\\593254315050521\\')

    # scanSmlFile("/media/cc/MOIVESOFT/")
    # scanSmlFile("/media/cc/PJYP/")
    # scanSmlFile("/media/cc/ZP/")
    # scanSmlFile("/media/cc/娱乐/")
    # scanSmlFile("/media/cc/文档/")
    # scanSmlFile("/media/cc/系统/")
    # scanSmlFile("/media/cc/软件/")

    removeGarbageFiles("I:")
    removeGarbageFiles("J:")
    removeGarbageFiles("K:")
    removeGarbageFiles("L:")
    removeGarbageFiles("M:")
    removeGarbageFiles("N:")
    removeGarbageFiles("X:")


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