#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
"""显示目录树状图"""
import os,sys
import glob
import shutil

#不扫码的文件夹
black_dir_list=['$RECYCLE.BIN','System Volume Information','FriendlyElec-H3']
#路径分隔符 \\ /
osseparator=os.path.sep
def getdriver( path, platform):
    if (platform == 'Windows'):
        driver, rem = os.path.splitdrive(path)
    else:
        driver = path
    return driver

def getDriverAndPlatForm(path):
    p=getPlatform()
    return  getdriver(path,p),p

def getDriverPath(path):
    return  getdriver(path,getPlatform())+os.path.sep
def isScanDir( path):
    for dir in black_dir_list:
        if (dir in path):
            return True
    return False
# 获取当前系统信息
def getPlatform():
    if sys.platform.startswith('linux'):
        current_os = "Linux"
    elif sys.platform.startswith('win'):
        current_os = "Windows"
    elif sys.platform.startswith('darwin'):
        current_os = "MAC"
    else:
        current_os = str(sys.platform)
    return current_os

def generate_file_tree_local(path: str, depth: int, site: list):
    """
    递归打印文件目录树状图（使用局部变量）

    :param path: 根目录路径
    :param depth: 根目录、文件所在的层级号
    :param site: 存储出现转折的层级号
    :return: None
    """
    void_num = 0
    filenames_list = os.listdir(path)

    for item in filenames_list:
        string_list = ["│   " for _ in range(depth - void_num - len(site))]
        for s in site:
            string_list.insert(s, "    ")

        if item != filenames_list[-1]:
            string_list.append("├── ")
        else:
            # 本级目录最后一个文件：转折处
            string_list.append("└── ")
            void_num += 1
            # 添加当前已出现转折的层级数
            site.append(depth)
        # print("\033[44m".join(string_list) + item+"\033[0m")

        new_item = path + '/' + item
        if os.path.isdir(new_item):
            print("".join(string_list) + item + '=>test')
            generate_file_tree_local(new_item, depth + 1, site)
        else:
            print("".join(string_list) + "\033[44m"+item + "\033[0m")
        if item == filenames_list[-1]:
            void_num -= 1
            # 移除当前已出现转折的层级数
            site.pop()

#根据txt删除指定文件
def delfilebytxt(txtpath):
    with open(txtpath, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            line=line.strip()
            if(line is not None and os.path.isfile(line)):
                print('remove ==>'+line)
                os.remove(line)
            else:
                print("File does not exist "+line)
#根据文件全路径，生成文件名，去除驱动器后的路径值
def splitPath2fnameDname(fullpath, driver):
    filename = os.path.basename(fullpath)
    filedir = os.path.dirname(fullpath)
    # dirpath  filename portion[1]
    filedir = filedir.replace(driver, '')
    filedir = filedir.replace(filename, '')
    return filename,filedir+osseparator

#视频类型分类
category=['spj','sp','ds','hj','mj','md','pic','jvid','xz','sm','of','tui','pic','zp',]

#虚拟分区，为区分每个分区的唯一性
virtualLocation=['ZB','SPJ','SP','SPJ-A','SPJHJ','E','H','I','J','K','G','O','V','X','N','T','','Z',]
def getVirtualPathByROOTDir(root_path, file_extension):

        # 确保扩展名前有一个点
        if not file_extension.startswith('.'):
            file_extension = '.' + file_extension



def getVirtualPath(path, file_extension):
    driver=getDriverPath(path)
     # 获取根目录下的所有文件和目录名
    files_in_root = os.listdir(driver)

    # 筛选出匹配指定扩展名的文件
    files = [f for f in files_in_root if f.endswith(file_extension)]
    if(len(files)>0):
        for f in files:
            farray = os.path.splitext(f)
            if(farray[0] in virtualLocation):
                print('VirtualPath  is '+farray[0] )
                return farray[0]
    return 'None'

if __name__ == '__main__':

    # root_path = input("请输入根目录路径：")
    # root_path = "D:\\temp\\0555\\"
    # print(os.path.abspath(root_path))
    # generate_file_tree_local(root_path, depth=0, site=[])
    # 示例用法

    # 查找根目录下所有的 .txt 文件
    txt_files = getVirtualPath('D:\\temp\\','.ini')
    print(txt_files)
    # 打印找到的文件路径

