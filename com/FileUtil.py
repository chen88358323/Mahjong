import os


def removeFiles(filepath):
    array = ['【01axg.xyz】.jpg', '02AXG.XYZ.png', '03axg.XYZ.png',
             '04axg.xyz.png', '05axg.xyz.png',
             '( 1024网址PC端发布器 3.0 ).chm',
             '( 1024社区手机网址发布器 3.1 ).apk',
             '( 扫码下载1024安卓APP_3.0 ).png']
    # prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            #   print('f:'+filename)
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
    removeFiles('G:\\迅雷下载\\')
    removeFiles('F:\\迅雷下载\\')
