# -*-coding:utf8-*-
import os


def editXunleiFile(filepath):
    # filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith('.bt.xltd'):
                # print('dirpath:'+dirpath)
                new = filename.replace(".bt.xltd", "")
                oldfile = dirpath + os.sep + filename
                newfile = dirpath + os.sep + new
                # print("修改前:" + oldfile)
                # print("修改后:" + newfile)
                os.renames(oldfile, newfile)


def removeFiles(filepath):
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
             '免费资源实时更新.png'
             ]
    # prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            # print('f:'+filename)
            if filename in array:
                absPath = dirpath + "\\" + filename
                print(absPath)
                os.remove(absPath)
            # torr = os.path.join(dirpath, filename)
            # absPath = dirpath + filename
            # if(absPath.endswith(prefix)):
            #     print(absPath)


if __name__ == '__main__':
    # getDulicateFiles()
    # getTorrDetail()
    # removeFiles('G:\\迅雷下载\\2022-03-01\\49\\y\\')
    # removeFiles('F:\\迅雷下载\\\2022-03-01\\15\\y\\24\\')
    # removeFiles('G:\\迅雷下载\\2022-03-01\\13\\y\\')

    editXunleiFile('F:\\迅雷下载\\2022-03-01\\best4\un\\y\\v')
    # removeFiles('O:\\F\\cd1014\\11\\26\\')
    # removeFiles('G:\\迅雷下载\\2022-03-01\\1112\\y\\')
    ###removeFiles('F:\\迅雷下载\\2022-03-01\\1112\\y\\')
    # removeFiles('F:\\迅雷下载\\2022-03-01\\1102\\y\\')
    removeFiles('F:\\迅雷下载\\2022-03-01\\1127-22\\')
    removeFiles('F:\\迅雷下载\\2022-03-01\\hj\\un\\')
    removeFiles('F:\\迅雷下载\\2022-03-01\\best3\\un\\')
    removeFiles('G:\\迅雷下载\\2022-03-01\\best3\\un\\')
    removeFiles('G:\\迅雷下载\\2022-03-01\\best\\y\\un\\')
    removeFiles('F:\\迅雷下载\\2022-03-01\\best\\y\\un\\')
    # removeFiles('G:\\done\\')
    # removeFiles('F:\\done\\')
