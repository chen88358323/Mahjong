# -*- coding: utf-8 -*-
import shutil
import os
siteStr=['gc2048.com-','gc2048.com','rh2048.com','hhd800.com@',
         'hhd800.com','aavv38.xyz@','aavv38.xyz','@']
entertag='\r\n'
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

if __name__ == '__main__':
    clearDirName('D:\\temp\\dist\\')