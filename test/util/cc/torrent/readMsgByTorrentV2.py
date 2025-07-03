from torrentool.api import Torrent
import zipfile
from pathlib import Path

from deprecated import deprecated

from torrentool.exceptions import BencodeDecodingError
from torrent_download_files_check import DownLoadCheck
import os
import shutil
import loggerTemplate
from collections import defaultdict

loger = loggerTemplate.log
TORR_ERROR_DIRNAME = 'errorbak'
HALF_NAME_PREFIX = 'HALF-'
# logpath='D:\\temp\\0555\\'

array = ['【01axg.xyz】.jpg', '02AXG.XYZ.png', '03axg.XYZ.png', '8axg.xyz.png',
         'duplicatedirtyData.txt'
         ]


def removeFiles(filepath):
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath + "\\" + filename
                loger.info(absPath)
                os.remove(absPath)


def getDulicateFiles():
    filepath = 'D:\\temp\\593254315050521\\'
    prefix = '(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            absPath = dirpath + filename
            if (absPath.endswith(prefix)):
                loger.info(absPath)


#获取torrpath 当前文件夹的目录列表，文件列表
#todo  如果一个文件夹夹 02 有多个种子与对应下载文件会有问题
#不包含子目录
#返回值dir_dict{hcode,dir}  single_file_list 为路径名
def get_file_dir_list(down_files_path):
    single_file_list = []
    # 搜集已下载文件列表 TODO 增加单文件支持
    for filename in os.listdir(down_files_path):
        f = os.path.join(down_files_path, filename)
        if filename == 'y' and os.path.isdir(f):
            continue
        if (os.path.isfile(f)):
            single_file_list.append(filename)

    loger.debug('待处理单文件个数' + str(len(single_file_list)))
    return single_file_list


def findTorrListByStr(strlist, path):
    if strlist is None:
        return
    else:
        for str in strlist:
            loger.info('*************************' + str + '查找开始*******************************')
            getTorrentByDetails(str, path)
            loger.info('*************************' + str + '查找结束*******************************')


#加载种子，如果种子错误或者内容为空，返回空
def loadTorr(torrpath):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return my_torrent
    except BencodeDecodingError:
        loger.error("error " + torrpath)
        # slove_bencode_torr(torrpath)
        return None
    except IndexError:
        loger.error("error " + torrpath)
        return None


def loadTorr_and_fixTorr(torrpath, count):
    try:
        my_torrent = Torrent.from_file(torrpath)
        return my_torrent
    except BencodeDecodingError:
        count += 1
        loger.error("error " + torrpath)
        if (count < 2 and os.path.getsize(torrpath) > 1024):
            return slove_bencode_torr(torrpath)
        else:
            return None
    except IndexError:
        loger.error("error " + torrpath)
        return None


def slove_bencode_torr(torrfile):
    fix_torrent(torrfile)
    return loadTorr(torrfile)


def get_errordir_filename_from_fullpath(fullpath):
    file_path = Path(fullpath)
    # 获取文件名（含扩展名）
    file_name = file_path.name
    # 获取父目录路径
    error_path = file_path.parent.joinpath(TORR_ERROR_DIRNAME)  # 输出:路径
    return file_name, error_path, file_path.parent


def getTorrentByDetails(str, filepath):
    dirs = []
    # try:
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                path = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                my_torrent = loadTorr(path)
                if my_torrent is not None:
                    for torrfile in my_torrent.files:
                        # loger.info('name:'+torrfile.name)
                        if (torrfile.name.startswith(str)):
                            loger.info('t:==>' + path)
                            dirs.append(path)
                            # loger.info(my_torrent.total_size / len)
                            loger.info('str:==>' + str)
                            # loger.info(my_torrent.files)
                            break


def editXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix):
                loger.info('dirpath:' + dirpath)
                new = filename.replace(xunleisuffix, "")
                oldfile = filepath + os.sep + filename
                newfile = filepath + os.sep + new
                loger.info("修改前:" + oldfile)
                loger.info("修改后:" + newfile)
                os.renames(oldfile, newfile)


def clearXunleiFile(filepath):
    #filepath = 'D:\\temp\\593254315050521\\demo\\'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename.endswith(xunleisuffix) or filename.endswith(fdmsuffix) \
                    or filename.endswith(btcomet_suffix):
                fullname = os.path.join(dirpath, filename)
                try:
                    loger.info('file: ' + fullname)
                    os.remove(fullname)
                except UnicodeEncodeError:
                    # non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    # fullname=fullname.translate(non_bmp_map)
                    loger.info('full: ' + fullname)
                    os.remove(fullname)


'''
批量写子文件内容
'''


def writeTorrDetail(filepath):
    for i in os.listdir(filepath):
        path = filepath + i + os.path.sep
        if os.path.isdir(path):
            loger.info("writeTorrDetail path=====" + path)
            getTorrDetail(path)


#过滤大文件
#filterLen 过滤文件大小单位G
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
                loger.info('torr==' + torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                fileSize = my_torrent.total_size
                loger.info('size==' + str(fileSize))
                if fileSize > lenG:
                    shutil.move(torr, torrBigFilePath + filename)
                    loger.info('大文件')
                    bigfiles.append(my_torrent.name)
    loger.info('bigfiles size:' + str(len(bigfiles)))
    loger.info('bigfiles:' + str(bigfiles))


#判断pdf是否存在，存在， 转移至新路径
def movePdf(oldpdfpath, tarpath):
    oldpdf = nameTorr2Pdf(oldpdfpath)
    if os.path.isfile(oldpdf):
        #存在pdf 转移
        pdf_name = os.path.basename(oldpdf)
        loger.debug("迁移PDF文件 " + oldpdf + '至\n' + tarpath)

        shutil.move(oldpdf, tarpath + os.sep + pdf_name)


# 将种子路径转化为pdf路径
def nameTorr2Pdf(torrfullpath):
    if (torrfullpath is None):
        return
    else:

        path, ext = os.path.splitext(torrfullpath)
        pdfpath = path + '.pdf'
        return pdfpath


# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
#1.scan torr path,get dict  key 种子名称   val 种子路径
#2. find same move

###Q1. 需要给我hcode处理，单文件也需要处理
@deprecated(reason="此方法已弃用，请使用 filterDownFilesV2() 替代")
def filterDownFiles(torrpath, filepath, subDirName):
    # for dirpath, dirnames, filenames in os.walk(filepath):
    #     for dirname in dirnames:
    #         loger.info('dir:   ' +dirname)
    dirList = []
    #搜集已下载文件列表 TODO 增加单文件支持
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
            dirList.append(filename)
            loger.info('dirname   ' + filename)
    files = os.listdir(filepath)
    # clearMacConfigFile(dirList)
    # 根据种子路径生成词典  key 种子名称   val 种子路径 todo  key修改为hcode
    torrDict = geneTorrentDic(torrpath)
    torrlist = torrDict.keys()
    reset = set(dirList) & set(torrlist)
    #loger.info('dirList'+str(dirList))
    #loger.info('torrlist' + str(torrlist))
    rslist = list(reset)
    loger.info("  =====================  ")
    loger.info(rslist)

    torrDonePath = torrpath + os.path.sep + subDirName + os.path.sep
    mkdirs(torrDonePath)

    finishFilePath = filepath + os.path.sep + subDirName + os.path.sep
    mkdirs(finishFilePath)

    for samefile in rslist:
        loger.info(" ****   ")
        #loger.info(torrDict[samefile])
        loger.info(os.path.basename(torrDict[samefile]))
        newTorrFile = torrDonePath + os.path.basename(torrDict[samefile])

        finishFile = finishFilePath + samefile
        #已经移动了，删除原有的 并打印提示信息
        if os.path.isfile(newTorrFile):
            loger.error("****************有已经下载过得文件******************")
            loger.error("****************种子文件**************************")
            loger.error(newTorrFile)
            loger.error("****************重复文件**************************")
            loger.error(str(filepath + os.path.sep + samefile) + "   " + str(finishFile))
            os.remove(torrDict[samefile])
        else:  #移动种子
            loger.debug("********原种子地址*************")
            loger.debug(torrDict[samefile])
            loger.debug("********新种子地址*************")
            loger.debug(newTorrFile)
            shutil.move(torrDict[samefile], newTorrFile)

        #文件已经下载过了，重新命名复制
        if os.path.exists(finishFile):
            finishFile = finishFile + '_new'
            # base, ext = os.path.splitext(finishFile)
            # finishFile = f"{base}_new{ext}"  # 修改文件名以避免冲突
            mkdirs(finishFile)
        #移动完成文件
        shutil.move(filepath + os.path.sep + samefile, finishFile)
        loger.debug("********原文件地址*************")
        loger.debug(filepath + os.path.sep + samefile)
        loger.debug("********新文件地址*************")
        loger.debug(finishFile)
        # 判断pdf是否存在，存在， 转移至新路径
        movePdf(torrDict[samefile], finishFile)

    loger.info('移动种子文件：' + str(len(rslist)))


# torrpath 种子路径
# filepath 下载文件路径
# subDirName转移的子文件夹名称，有y ,half
# 1.scan torr path,get dict  key 种子名称   val 种子路径
# 2. find same move

###Q1. 文件夹下有多个种子文件，没做处理
def filterDownFilesV2(torrpath, filepath, subDirName):
    # dir_list = []
    # single_file_list=[]

    # 扫描下载完成文件夹
    dir_dict = query_torr_dir_dict_byDir(filepath, True, 'y')
    # 扫描下载完成单文件
    single_file_list = get_file_dir_list(filepath)

    #扫描种子文件夹
    single_files_torr_dict, muti_files_torr_dict = geneTorrentDicV2(torrpath)

    #生成转以后得文件夹
    torrDonePath = build_done_dir(torrpath, subDirName)
    finishFilePath = build_done_dir(filepath, subDirName)

    #1.dir filter
    filter_torr_dirs(dir_dict, muti_files_torr_dict,
                     torrpath, filepath,
                     torrDonePath, finishFilePath)
    #2.single file filter
    filter_torr_files(single_file_list, single_files_torr_dict,
                      torrpath, filepath,
                      torrDonePath, finishFilePath)

    # for samefile in rslist:
    #     loger.info(" ****   ")
    #     # loger.info(torrDict[samefile])
    #     loger.info(os.path.basename(torrDict[samefile]))
    #     newTorrFile = torrDonePath + os.path.basename(torrDict[samefile])
    #
    #     finishFile = finishFilePath + samefile
    #     # 已经移动了，删除原有的 并打印提示信息
    #     if os.path.isfile(newTorrFile):
    #         loger.error("****************有已经下载过得文件******************")
    #         loger.error("****************种子文件**************************")
    #         loger.error(newTorrFile)
    #         loger.error("****************重复文件**************************")
    #         loger.error(str(filepath + os.path.sep + samefile) + "   " + str(finishFile))
    #         os.remove(torrDict[samefile])
    #     else:  # 移动种子
    #         loger.debug("********原种子地址*************")
    #         loger.debug(torrDict[samefile])
    #         loger.debug("********新种子地址*************")
    #         loger.debug(newTorrFile)
    #         shutil.move(torrDict[samefile], newTorrFile)
    #
    #     # 文件已经下载过了，重新命名复制
    #     if os.path.exists(finishFile):
    #         finishFile = finishFile + '_new'
    #         # base, ext = os.path.splitext(finishFile)
    #         # finishFile = f"{base}_new{ext}"  # 修改文件名以避免冲突
    #         mkdirs(finishFile)
    #     # 移动完成文件
    #     shutil.move(filepath + os.path.sep + samefile, finishFile)
    #     loger.debug("********原文件地址*************")
    #     loger.debug(filepath + os.path.sep + samefile)
    #     loger.debug("********新文件地址*************")
    #     loger.debug(finishFile)
    #     # 判断pdf是否存在，存在， 转移至新路径
    #     movePdf(torrDict[samefile], finishFile)
    #
    # loger.info('移动种子文件：' + str(len(rslist)))

    #计算文件的大小，下载比例


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
    #todo


#根据种子路径生成词典  key 种子hcode   val 种子路径
#原则上不会有重复，毕竟文件名不可能重复
def geneTorrentDicV2(torrpath):
    torr_muti_file_hcode_list = []
    torr_single_file_hcode_list = []  #只有一个文件
    torr_muti_file_list = []
    torr_single_file_list = []  #只有一个文件
    torrNamelist = []
    torrent_num = 0

    for dirpath, dirnames, filenames in os.walk(torrpath):
        if dirpath == 'y':
            continue
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torrent_num += 1
                torr = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                # loger.info("len(my_torrent.files"+str(len(my_torrent.files)))
                if (len(my_torrent.files) == 1):
                    torr_single_file_hcode_list.append(my_torrent.info_hash.lower())
                    torr_single_file_list.append(my_torrent)
                else:
                    torr_muti_file_hcode_list.append(my_torrent.info_hash.lower())
                    torr_muti_file_list.append(my_torrent)

    # todo  id
    loger.debug("torrent总数:" + str(torrent_num))
    loger.debug("torrent 下载为文件夹总数:" + str(len(torr_single_file_hcode_list)))
    loger.debug("torrent 下载为单文件总数:" + str(len(torr_muti_file_hcode_list)))
    muti_files_torr_dict = dict(zip(torr_muti_file_hcode_list, torr_muti_file_list))
    single_files_torr_dict = dict(zip(torr_single_file_hcode_list, torr_single_file_list))

    return single_files_torr_dict, muti_files_torr_dict


#dir_dict  下载路径内的种子即可，key为种子code，val为该种子上级目录，即文件下载路径
#muti_files_torr_dict 为种子字典 ，key为种子code，val为该种子详细信息
#
def filter_torr_dirs(dir_dict, muti_files_torr_dict,
                     torrpath, filepath,
                     torrDonePath, finishFilePath):
    if dir_dict and len(dir_dict) > 0:
        downloaded_torr_code_list = dir_dict.keys()
        src_torr_code_list = muti_files_torr_dict.keys()
        torr_list = set(downloaded_torr_code_list) & set(src_torr_code_list)
        # loger.info("downloaded_torr_code_list")
        # loger.info(str(downloaded_torr_code_list))
        # loger.info("src_torr_code_list")
        # loger.info(str(src_torr_code_list))

        if torr_list is None or len(torr_list) == 0:
            loger.info("文件目录" + filepath + " 待处理文件数" + str(len(downloaded_torr_code_list)))
            loger.info("与种子目录" + torrpath + "没有合并" + " 种子文件数" + str(len(src_torr_code_list)))
        else:
            for code in torr_list:
                torr_obj = muti_files_torr_dict[code]
                torr_path = str(Path(torr_obj._filepath))
                file_dirname = dir_dict[code]
                loger.debug("code " + code)
                loger.debug("torr_path " + torr_path)
                loger.debug("file_dirname " + file_dirname)
                move_torr(torr_obj.name + '.torrent', torr_path, torrDonePath)
                tarpath = move_downloaded_files(file_dirname, file_dirname, finishFilePath)
                movePdf(torr_path, tarpath)
    else:
        loger.info(filepath + " 多文件列表为空")


def build_done_dir(fpath, subdirname):
    if fpath is None or subdirname is None:
        return
    else:
        if os.path.split(fpath) == subdirname:
            loger.error('文件夹无需创建')
            return fpath
        else:
            newpath = fpath + os.path.sep + subdirname + os.path.sep
            if not os.path.exists(newpath):
                mkdirs(newpath)
            return newpath


def move_torr(torr_name, torr_fullname, torr_done_path):
    loger.debug("********torr_name*************"+torr_name)
    loger.debug("********torr_fullname*************"+torr_fullname)
    if (torr_name is None):
        torr_name = os.path.split(torr_fullname)
    new_torr=torr_done_path+torr_name
    if os.path.exists(new_torr):
        loger.error("****************该种子文件已经下载过******************")
        loger.error(new_torr)
        if torr_fullname != new_torr:
            os.remove(torr_fullname)
    else:  # 移动种子
        loger.debug("********原种子地址*************")
        loger.debug(torr_fullname)
        loger.debug("********新种子地址*************")
        loger.debug(torr_done_path)
        shutil.move(torr_fullname, torr_done_path)


def move_downloaded_files(dirname, oldpath, finished_path):
    if (not dirname):
        dirname = os.path.split(oldpath)
        newpath = finished_path + dirname
        if (os.path.exists(newpath)):
            newpath = newpath + '_new'
            mkdirs(newpath)
            loger.debug("迁移下载文件 " + oldpath + ' 至 \n  ' + newpath)
            shutil.move(oldpath, newpath)
        return newpath
    else:
        loger.debug("迁移下载文件 " + oldpath + ' 至 \n  ' + finished_path)
        shutil.move(oldpath, finished_path)
        return finished_path


def filter_torr_files(single_file_list, single_files_torr_dict,
                      torrpath, filepath,
                      torrDonePath, finishFilePath):
    if not single_file_list or len(single_file_list) == 0:
        loger.info(filepath + " 下载的单文件列表为空")
    elif single_files_torr_dict and len(single_files_torr_dict) > 0:
        torrobj_list = single_files_torr_dict.values()
        for tobj in torrobj_list:
            try:
                tname = tobj.files[0].name
                if tname in single_file_list:
                    loger.info(tname + " 开始迁移")
                    new_torr_path = torrDonePath + tobj.name
                    f = filepath + os.path.sep + tname
                    loger.debug("迁移下载文件 " + f + '至\n' + finishFilePath)
                    shutil.move(f, finishFilePath)
                    tpath = str(Path(tobj._filepath))
                    loger.debug("迁移种子文件 " + tpath + '至\n' + torrDonePath)
                    shutil.move(tpath, torrDonePath)

                    movePdf(tpath, finishFilePath)

                    single_file_list.remove(tname)
            except IndexError:
                loger.error("tobj.files " + str(tname))
                loger.error("single_file_list " + str(single_file_list))
            except Exception as e:
                loger.error(f"迁移过程中发生错误: {e}")
    else:
        loger.info(filepath + " 单文件列表为空")


#根据种子路径生成词典  key 种子名称   val 种子路径
#原则上不会有重复，毕竟文件名不可能重复
def geneTorrentDic(torrpath):
    torrlist = []
    torrNamelist = []
    for dirpath, dirnames, filenames in os.walk(torrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # loger.info('torr=='+torr)
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                torrlist.append(my_torrent.name)
                torrNamelist.append(torr)
    torrDict = dict(zip(torrlist, torrNamelist))
    return torrDict

    #计算文件夹file_path的大小


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
        loger.info('mkdir:' + str(path))
        os.mkdir(path)


def getTorrDetail(filepath):
    filepath = filepath + os.path.sep
    dirname = os.path.dirname(filepath)
    #文件夹最后一层名称
    basename = os.path.split(dirname)[-1]
    txtpath = filepath + basename + '.txt'
    loger.info('basename==>' + basename)
    loger.info('dirname==>' + dirname)
    loger.info('txtfile===>' + txtpath)

    txtfile = open(txtpath, 'w+', encoding='utf-8')

    len = 1024 * 1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        # 跳过指定目录（修改dirnames列表）
        if TORR_ERROR_DIRNAME in dirnames:
            dirnames.remove(TORR_ERROR_DIRNAME)  # 从待遍历列表中移除，避免进入该目录

        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            txtfile.writelines("=================================" + '\r')
            if portion[1] == ".torrent":
                # loger.info(torr)
                txtfile.writelines(torr + '\r')
                my_torrent = loadTorr_and_fixTorr(torr, 0)
                if my_torrent is None or os.path.getsize(torr) < 500:
                    continue
                tlen = my_torrent.total_size / len
                txtfile.writelines(str(tlen) + '\r')
                txtfile.writelines(str(my_torrent.files) + '\r\n')
                txtfile.writelines(my_torrent.info_hash + '\r')

                # loger.info(my_torrent.total_size / len)
                # loger.info(my_torrent.comment)
                loger.info(portion[0] + '          ' + my_torrent.name)
                for torrfile in my_torrent.files:
                    if (torrfile.length > 100 * len):
                        txtfile.writelines(str(torrfile) + '\r')
                # filesor tf in list[my_torrent.files]:

    txtfile.close()


#有些种子文件，结尾有\r\n导致，解析错误，扫描一遍，将有错误的文件重新生成一遍
#torrdir  c:\\ttt
def pre_slove_error_torrs(torrdir):
    for filename in os.listdir(torrdir):
        file_path = os.path.join(torrdir, filename)

        portion = os.path.splitext(filename)
        if portion[1] == ".torrent":
            fix_torrent(file_path)


#修复种子数据内容，通常为结尾\r\n造成读取异常
#file_path 全路径
#filename 文件名称，含后缀
#err_back_path 异常文件夹
def fix_torrent(file_path):
    filename, err_back_path, dirpath = get_errordir_filename_from_fullpath(file_path)
    # 检查是否为文件
    if os.path.isfile(file_path) and file_path.endswith('.torrent'):

        if os.path.getsize(file_path) > 1000:
            # 读取文件内容
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # 检查文件是否以 \r\n 结尾
            if file_content.endswith(b'\r\n'):
                mkdirs(err_back_path)
                txt = log(str(dirpath), 'error', True)
                # 备份文件到 error 文件夹
                backup_path = os.path.join(err_back_path, filename)
                txt.writelines("************************待查找************  " + '\r\n')
                txt.writelines(file_path + " is deleteed \\r\\n" + '\r\n')
                txt.close()
                new_content = file_content[:-2]
                with open(file_path, 'wb') as file:
                    file.write(new_content)
        else:
            mkdirs(err_back_path)
            txt = log(str(dirpath), 'error', True)
            txt.writelines("************************待查找************  " + '\r\n')
            txt.writelines(file_path + " is error ，need redownload" + '\r\n')
            txt.close()
            shutil.copy(file_path, err_back_path)


#将异常种子，进行转移压缩备份
def zip_and_clear(torrdir):
    err_back_path = torrdir + os.sep + TORR_ERROR_DIRNAME
    err_back_zip = torrdir + '\errorbak.zip'
    # 压缩错误文件夹
    with zipfile.ZipFile(err_back_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(err_back_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, start=err_back_path))


#path 待扫描生成唯一hashcode的种子路径
def scan_torr_get_hashlist(path, txt):
    tarlist = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                torr = os.path.join(dirpath, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                hashcode = my_torrent.info_hash.lower()
                if txt is not None:
                    txt.writelines("hashcode  " + hashcode + '\r\n')
                tarlist.append(hashcode)


def findTorrentByHashcode(srctorrpath, tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcode', False)
    #遍历待查找的种子，生成集合
    tarlist = scan_torr_get_hashlist(tartorrpath, txt)
    txt.writelines("************************待查找************  " + '\r\n')
    srclist = scan_torr_get_hashlist(srctorrpath, None)

    dupdata = [dup for dup in tarlist if dup in srclist]
    for dirpath, dirnames, filenames in os.walk(srctorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                srctorrpath = os.path.join(dirpath, filename)
                srctorrent = loadTorr(srctorrpath)
                if srctorrent is None:
                    continue
                srccode = srctorrent.info_hash.lower()
                if srccode in tarlist:
                    txt.writelines("hashcode  " + srccode + '\r\n')
                    txt.writelines("dirpath  " + dirpath + '\r\n')
                    txt.writelines("filename  " + filename + '\r\n')

    txt.close()


# 根据文件路径，获取该文件夹下的，种子code及其对应列表
# def query_torr_dir_dict_byDir(dirpath):
#     torr_dir_dict={}
#     for dirpath, dirnames, filenames in os.walk(dirpath):
#         for filename in filenames:
#             portion = os.path.splitext(filename)
#             if portion[1] == ".torrent":
#                 torr = os.path.join(dirpath, filename)
#                 # txt.writelines("dirpath  "+dirpath+'\r\n')
#                 # txt.writelines("filename  " + filename + '\r\n')
#                 my_torrent = loadTorr(torr)
#                 if my_torrent is None:
#                     continue
#                 hashcode=my_torrent.info_hash.lower()
#                 torr_dir_dict[hashcode]=dirpath
#
#     loger.debug('待处理文件夹个数' + str(len(torr_dir_dict)))
#     return torr_dir_dict


# 根据文件路径，获取该文件夹下的，种子code及其对应列表
#dirpath扫描路径
#skiptag是否跳过指定文件夹
#指定文件夹名称
def query_torr_dir_dict_byDir(dirpath, skipTag, dname):
    torr_dir_dict = {}
    dir_torrent_count = defaultdict(int)
    # 先统计每个目录的torrent文件数量
    for root, dirs, files in os.walk(dirpath):
        if skipTag and dname in dirs:
            dirs.remove(dname)
        torrent_count = sum(1 for f in files if f.endswith('.torrent'))
        dir_torrent_count[root] = torrent_count
    # 再次遍历，只处理只有一个torrent文件的目录
    for root, dirnames, filenames in os.walk(dirpath):
        if skipTag and dname in dirnames:
            dirnames.remove(dname)
        if dir_torrent_count[root] != 1:
            continue
        for filename in filenames:
            if filename.endswith('.torrent'):
                torr = os.path.join(root, filename)
                # txt.writelines("dirpath  "+dirpath+'\r\n')
                # txt.writelines("filename  " + filename + '\r\n')
                my_torrent = loadTorr(torr)
                if my_torrent is None:
                    continue
                hashcode = my_torrent.info_hash.lower()
                torr_dir_dict[hashcode] = root

    loger.debug('待处理文件夹个数' + str(len(torr_dir_dict)))
    return torr_dir_dict


#srctorrpath  种子集散地
# tartorrpath  待查找种子
def findTorrentByHashcodeInDir(srctorrpath, tartorrpath):
    txt = log(tartorrpath, 'findTorrentByHashcodeInDir', False)
    torr_dir_dict = query_torr_dir_dict_byDir(tartorrpath, False, None)
    tarlist = torr_dir_dict.keys()
    #遍历待查找的种子，生成集合
    txt.writelines("************************待查找************  " + '\r\n')
    # for dirpath, dirnames, filenames in os.walk(tartorrpath):
    #     for filename in filenames:
    #         portion = os.path.splitext(filename)
    #         if portion[1] == ".torrent":
    #             torr = os.path.join(dirpath, filename)
    #             # txt.writelines("dirpath  "+dirpath+'\r\n')
    #             # txt.writelines("filename  " + filename + '\r\n')
    #             my_torrent = Torrent.from_file(torr)
    #             hashcode=my_torrent.info_hash.lower()
    #             txt.writelines("torr  " + torr + '\r\n')
    #             txt.writelines("hashcode  " + hashcode + '\r\n')
    #             tarlist.append(hashcode)
    # txt.writelines("************************待查找************  " + '\r\n')

    for dirpath, dirnames, filenames in os.walk(srctorrpath):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".torrent":
                srctorrpath = os.path.join(dirpath, filename)
                try:
                    srctorrent = loadTorr(srctorrpath)
                    srccode = srctorrent.info_hash.lower()
                    if srccode in tarlist:
                        txt.writelines("hashcode  " + srccode + '\r\n')
                        txt.writelines("dirpath  " + dirpath + '\r\n')
                        txt.writelines("filename  " + filename + '\r\n')
                except AttributeError:
                    loger.info('error file ' + srctorrpath)
                    continue
                except BencodeDecodingError:
                    # 种子下载失败了
                    loger.info('error file ' + srctorrpath)
                    continue
                except IndexError:
                    loger.info('error file ' + srctorrpath)
                    continue

    txt.close()


def log(filepath, name, append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]

    loger.info('basename==>' + basename)
    loger.info('dirname==>' + dirname)
    txtpath = filepath + os.sep + basename + name + '.txt'
    loger.info('txtfile===>' + txtpath)
    if (append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile


#用来扫描half文件夹下所有待扫描的半下载文件
# downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def countHalfFiles(downdir, deltag):
    for root, dirs, files_list in os.walk(downdir):
        for file_name in files_list:
            if file_name.endswith('torrent') and not str(file_name).startswith(HALF_NAME_PREFIX):
                tfile = os.path.join(root, file_name)
                loger.info("tfile:" + tfile)
                loger.info("root:" + root)
                comparefiles(tfile, root, deltag)


### downdir 下载目录，包含了种子文件的头目录
### 日志文件
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
def scanDownloadingFiles(downdir, deltag):
    downloadmap = {}
    for dirpath, dirnames, filenames in os.walk(downdir):
        loger.debug('dirpath' + dirpath + '\r\n')
        # loger.info('dirpath'+dirpath)
        # loger.info('dirnames' + dirnames)
        for filename in filenames:

            portion = os.path.splitext(filename)
            if deltag and filename.endswith(xunleisuffix):
                fullname = os.path.join(dirpath, filename)
                loger.debug("del path:" + fullname)
                os.remove(fullname)
            elif portion[1] != ".bt":  #处理待下载文件，
                fullname = os.path.join(dirpath, filename)
                fsize = os.path.getsize(fullname)
                #loger.info("full path:"+fullname)
                # fullname=os.path.join(dirpath, ' '+filename)#torrent的file会有空格， 很奇怪
                torrfilepath = fullname.replace(downdir, '')
                if str(torrfilepath).startswith(os.path.sep):  #fix py版本兼容性问题
                    torrfilepath = torrfilepath[1:]
                #txtfile.writelines("download :" + torrfilepath+ '\r\n')
                #loger.info("size"+str(round(fsize/m,2))+'mb')
                downloadmap.setdefault(torrfilepath, fsize)  #生成文件列表

    return downloadmap


xunleisuffix = '.bt.xltd'
fdmsuffix = '.fdmdownload'
btcomet_suffix = '.bc!'

dlcheck = DownLoadCheck()
# dlcheck.merge_blacklists(r".", "bl.json",False)
blacklist = dlcheck.load_blacklist(r"bl.json")


#tfiles 种子里的文件，
#downdir 下载目录，包含了种子文件的头目录
# deltag 是否删除.bt.xltd的文件 True 删除 False 不删除
# todo  写日志
def comparefiles(tfile, downdir, deltag):
    # txtfile = log(downdir, 'comparefiles',False)
    loger.debug('tfile' + tfile + '\r\n')
    loger.debug('downdir' + downdir + '\r\n')
    loger.debug('downdir' + downdir)
    torrentmap = {}
    my_torrent = loadTorr(tfile)
    if my_torrent is None:
        return
    for file in my_torrent.files:  # 遍历种子文件
        ## 种子内容格式 TorrentFile(name='359\\\尖叫视频.mht', length=325117)
        tfilename = file.name.replace('\\\\', os.path.sep)
        # loger.info('tfilename'+tfilename)
        #截取359目录，由于可能会改名，所以
        file_array = tfilename.split(os.path.sep, 1)
        if (len(file_array) == 1):
            print('len1  tfilename==>' + tfilename)
            continue
        else:
            subpath = file_array[1]

        if subpath.__contains__(os.path.sep):
            subname = os.path.basename(subpath)
        else:
            subname = subpath
        #subpath \尖叫视频.mht
        #loger.info('subpath'+str(subpath))
        if subname in blacklist:
            continue
        if subname not in array:
            if subname.__contains__('如果您看到此文件，请升级到BitComet'):
                loger.info(subname)
            else:
                loger.debug("subpath :" + subpath)
                torrentmap.setdefault(subpath, file.length)
        ## 待增加过滤无用文件实现
    downloadmap = scanDownloadingFiles(downdir, deltag)
    m = 1024 * 1024

    #loger.info(tfilename)
    #loger.info(str(file))
    downloadfilelist = list(downloadmap.keys())
    tfiellist = list(torrentmap.keys())
    #txtfile.writelines(str(tfiellist))
    loger.debug('*************************************************')
    loger.debug('downloadfilelist' + str(len(downloadfilelist)) + '   ' + '\r\n')  #+str(downloadfilelist)
    # for dfile in downloadfilelist:
    #loger.info('tfiellist bf' + str(len(tfiellist)) + '   ' + str(tfiellist))
    # for cleanfile in downloadfilelist:
    tfiellist = getUndownFileList(tfiellist, downloadfilelist)
    #     if cleanfile in tfiellist:
    #         tfiellist.remove(cleanfile)
    #loger.info('tfiellist af' + str(len(tfiellist)) + '   ' + str(tfiellist))
    downloadfilesize = 0
    loger.debug("********************v1.0 已下载文件个数" + str(
        len(downloadfilelist)) + "个***************************" + '\r\n')
    loger.debug(
        "********************v1.0 待下载文件列表" + str(len(tfiellist)) + "个***************************" + '\r\n')
    if tfiellist is None or len(tfiellist) == 0:
        return
    #未完成的文件列表，新建文件打印
    else:
        undone_file = log("" + downdir, '--undone', False)
        tfiellist = set(tfiellist)
        tfiellist_namelist = list()
        for needdownfile in tfiellist:
            tfsize = torrentmap.get(needdownfile)
            downloadfilesize += tfsize
            tfsize = round(tfsize / m, 2)
            fname = os.path.basename(needdownfile)
            tfiellist_namelist.append(fname)
            undone_file.writelines("\"" + fname + "\"," + '\r\n')
            # txtfile.writelines('size:'+str(tfsize)+"mb"+ '\r\n')
        undone_file.writelines('总占用空间":' + str(round(downloadfilesize / m, 2)) + "mb" + '\r\n')
        undone_file.close()
        dlcheck.gen_blacklist(tfiellist_namelist, None)


#tfiles  种子文件列表
# downedfiles  已下载文件列表
def getUndownFileList(tfiles, downedfiles):
    tmap = {}  #key 去除了路径中的所有空格， val原路径
    for tf in tfiles:
        ctf = tf.replace(" ", "")
        tmap.setdefault(ctf, tf)
    tflist = tmap.keys()
    dmap = {}
    for df in downedfiles:
        cdf = df.replace(" ", "")
        dmap.setdefault(cdf, df)
    dflist = dmap.keys()
    for dfile in dflist:
        if dfile in tflist:
            tmap.pop(dfile)

    return tmap.values()


if __name__ == '__main__':
    # getTorrDetail('D:\\360Downloads\\1228\\')
    filterDownFilesV2(r'D:\temp\112\tttt', r'D:\temp\112', 'y')
    os._exit(0)
    countHalfFiles(r'D:\temp\112\y', False)

    # clearXunleiFile("D:\\temp\\")
    # findTorrentByHashcodeInDir(r"D:\temp\0555\2022-03-01",r"D:\temp\0555\tttt")

    # test()
    # clearXunleiFile(r'G:\down\0555\others\half')
    # clearXunleiFile(r'F:\down\0555\b16')
    # clearXunleiFile(r'G:\down\0555\b51')
    # countHalfFiles(r'F:\down\0555\b39\un\y', False)
    # filterDownFiles(r'C:\torrent\2022-03-01\0555\b51',
    #                r'g:\down\0555\b51\un', 'y')
    # getTorrDetail(r'F:\down\0555\b54\un\y\ssss')
    # os._exit(0)
    # countHalfFiles(r'g:\down\0555\b51\un\y', False)

    # filterDownFiles(r'C:\torrent\2022-03-01\0555\b38',
    #                r'g:\down\0555\b38\un', 'y')

    # countHalfFiles(r'g:\down\0555\b38\un\y', False)
    # os._exit(0)
    # loger.info('C5AEA8F99A520790D421FEB7162DDF7A77BD297B'.lower())
    # strlist=['爱剪辑-48.avi']
    # findTorrListByStr(strlist,'D:\\temp\\0555\\2022-03-01\\0555\\')
    # findTorrListByStr(strlist, 'D:\\temp\\0555\\2022-03-01\\0555\\b20\errfiles\\')
    # countHalfFiles(r'F:\down\1102\un\y', False)
    # countHalfFiles(r'F:\down\0555\b16\half', True)

    # countHalfFiles(r'G:\down\1102', False)
    # countHalfFiles(r'F:\down\0555\b54\un\y\ssss', False)
    # countHalfFiles(r'F:\down\0555\b54\un\y\3333', False)
    filterDownFilesV2(r'C:\torrent\2022-03-01\0555\b58',
                      r'F:\down\0555\b58\un', 'y')

    countHalfFiles(r'F:\down\0555\b58\un\y', False)
    os._exit(0)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b55',
                    r'g:\down\0555\b55\un', 'y')

    countHalfFiles(r'g:\down\0555\b55\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0322\other',
                    r'G:\down\0322\other\un', 'y')
    countHalfFiles(r'G:\down\0322\other\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1127\1',
                    r'F:\down\1127\1\un', 'y')
    countHalfFiles(r'F:\down\1127\1\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1127\2',
                    r'F:\down\1127\2\un', 'y')
    countHalfFiles(r'F:\down\1127\2\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b40',
                    r'f:\down\0555\b40\un', 'y')

    countHalfFiles(r'f:\down\0555\b40\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b54',
                    r'f:\down\0555\b54\un', 'y')

    countHalfFiles(r'f:\down\0555\b54\un\y', False)
    os._exit(0)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b16',
                    r'f:\down\0555\b16\un', 'y')

    countHalfFiles(r'f:\down\0555\b16\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0333\other',
                    r'G:\down\0333\other\un', 'y')
    countHalfFiles(r'G:\down\0333\other\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\43',
                    r'G:\down\43\un', 'y')
    countHalfFiles(r'G:\down\43\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\14',
                    r'G:\down\14\un', 'y')

    countHalfFiles(r'G:\down\14\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b36',
                    r'G:\down\0555\b36\un', 'y')

    countHalfFiles(r'G:\down\0555\b36\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b51',
                    r'g:\down\0555\b51\un', 'y')
    countHalfFiles(r'g:\down\0555\b51\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b54',
                    r'f:\down\0555\b54\un', 'y')

    countHalfFiles(r'f:\down\0555\b54\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0322\other',
                    r'G:\down\0333\other\un', 'y')
    countHalfFiles(r'G:\down\0333\other\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0333\other',
                    r'G:\down\0333\other\un', 'y')
    countHalfFiles(r'G:\down\0333\other\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0333\best',
                    r'G:\down\0333\best\un', 'y')
    countHalfFiles(r'G:\down\0333\best\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0333\1',
                    r'G:\down\0333\1\un', 'y')
    countHalfFiles(r'G:\down\0333\1\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\33',
                    r'G:\down\33\un', 'y')

    countHalfFiles(r'G:\down\33\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0333\1',
                    r'G:\down\0333\1\un', 'y')
    countHalfFiles(r'G:\down\0333\1\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\26',
                    r'G:\down\26\un', 'y')
    countHalfFiles(r'G:\down\26\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\others',
                    r'f:\down\0555\other\un', 'y')
    countHalfFiles(r'f:\down\0555\other\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\others',
                    r'g:\down\0555\others\un', 'y')
    countHalfFiles(r'g:\down\0555\others\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1201\02',
                    r'e:\down\1201\02\un', 'y')
    countHalfFiles(r'e:\down\1201\02\un\y', False)

    os._exit(0)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b51',
                    r'g:\down\0555\b51\un', 'y')

    # countHalfFiles(r'g:\down\0555\b51\un\y', False)
    countHalfFiles(r'G:\down\0555\b51\un\needscan', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b43', r'g:\down\0555\b43\un', 'y')

    countHalfFiles(r'g:\down\0555\b43\un\y', False)

    # filterDownFiles(r'C:\torrent\2022-03-01\0555\b44', r'g:\down\0555\b44\un', 'y')

    # countHalfFiles(r'g:\down\0555\b44\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b39',
                    r'f:\down\0555\b39\un', 'y')

    countHalfFiles(r'f:\down\0555\b39\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b40',
                    r'f:\down\0555\b40\un', 'y')

    countHalfFiles(r'f:\down\0555\b40\un\y', False)
    os._exit(0)

    countHalfFiles(r'G:\down\0555\others\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b38',
                    r'g:\down\0555\b38\un', 'y')

    countHalfFiles(r'g:\down\0555\b40\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b40',
                    r'f:\down\0555\b40\un', 'y')

    countHalfFiles(r'f:\down\0555\b40\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\1201\02',
                    r'e:\down\1201\02\un', 'y')
    countHalfFiles(r'e:\down\1201\02\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1201\01',
                    r'd:\down\1201\01\un', 'y')
    countHalfFiles(r'd:\down\1201\01\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1112',
                    r'f:\down\1112\un', 'y')
    countHalfFiles(r'f:\down\1112\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b42',
                    r'f:\down\0555\b42\un', 'y')

    countHalfFiles(r'f:\down\0555\b42\un\y', False)

    os._exit(0)
    filterDownFiles(r'C:\torrent\2022-03-01\1102',
                    r'F:\down\1102\un', 'y')
    countHalfFiles(r'F:\down\1102\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\1201\02',
                    r'e:\down\1201\02\un', 'y')
    countHalfFiles(r'e:\down\1201\02\un\y', True)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b42',
                    r'f:\down\0555\b42\un', 'y')
    countHalfFiles(r'f:\down\0555\b42\un\y', False)

    # filterDownFiles(r'C:\torrent\2022-03-01\0555\b31',
    #               r'G:\down\0555\b31\un', 'y')
    filterDownFiles(r'C:\torrent\2022-03-01\1201\01',
                    r'D:\down\1201\01\un', 'y')
    countHalfFiles(r'D:\down\1201\01\un\y', True)
    filterDownFiles(r'C:\torrent\2022-03-01\1201\02',
                    r'e:\down\1201\02\un', 'y')
    countHalfFiles(r'e:\down\1201\02\un\y', True)

    # countHalfFiles(r'G:\down\0322\HJ\half', True)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b43',
                    r'G:\down\0555\b43\un', 'y')
    countHalfFiles(r'F:\down\0555\b40\un\y', False)

    countHalfFiles(r'G:\down\0555\b43\half\half', True)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'G:\down\0555\b41\un', 'y')

    countHalfFiles(r'G:\down\0555\b41\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'f:\down\0555\b41\un', 'y')

    countHalfFiles(r'f:\down\0555\b41\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'F:\down\0555\b41\un', 'y')

    countHalfFiles(r'F:\down\0555\b41\half', True)

    countHalfFiles(r'G:\down\0555\b31\half', True)
    countHalfFiles(r'G:\down\0555\b37\half', True)
    countHalfFiles(r'G:\down\0555\b38\half', True)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'F:\down\0555\b41\un', 'y')
    countHalfFiles(r'F:\down\0555\b41\un\y', False)
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'G:\down\0555\b41\un', 'y')
    countHalfFiles(r'G:\down\0555\b41\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b41',
                    r'G:\down\0555\b41\half', 'half')
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b31',
                    r'G:\down\0555\b31\half', 'half')
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b37',
                    r'G:\down\0555\b37\half', 'half')
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b38',
                    r'G:\down\0555\b38\half', 'half')
    filterDownFiles(r'C:\torrent\2022-03-01\0555\b38',
                    r'G:\down\0555\b38\un', 'y')
    countHalfFiles(r'G:\down\0555\b38\un\y', False)

    countHalfFiles(r'G:\down\0555\b38\un\y', False)

    filterDownFiles(r'C:\torrent\2022-03-01\0555\b43',
                    r'G:\down\0555\b43f\un', 'y')

    countHalfFiles(r'G:\down\0555\b43f\un\y\161', False)
    # getTorrDetail(r'D:\temp\0555\2022-03-01\0555\b38')
    os._exit(0)
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b30\\")
    # os._exit(0)

    filterDownFiles(r'D:\t7\2022-03-01\0555\b31', r'G:\down\0555\b31\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b32', r'G:\down\0555\b32\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b33', r'G:\down\0555\b33\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b34', r'G:\down\0555\b34\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b35', r'G:\down\0555\b35\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b36', r'G:\down\0555\b36\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b37', r'G:\down\0555\b37\un', 'y')
    os._exit(0)
    countHalfFiles(r'D:\temp\112\2', False)
    os._exit(0)
    getTorrDetail(r'D:\temp\0555\2022-03-01\0555\b38')
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b30\\")
    # os._exit(0)

    filterDownFiles(r'D:\t7\2022-03-01\0555\b31', r'G:\down\0555\b31\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b32', r'G:\down\0555\b32\un', 'y')
    # filterDownFiles(r'D:\t7\2022-03-01\0555\b33', r'G:\down\0555\b33\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b34', r'G:\down\0555\b34\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b35', r'G:\down\0555\b35\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b36', r'G:\down\0555\b36\un', 'y')
    filterDownFiles(r'D:\t7\2022-03-01\0555\b37', r'G:\down\0555\b37\un', 'y')
    os._exit(0)

    # findTorrentByHashcodeInDir("D:\\temp\\0555\\2022-03-01\\","D:\\temp\\backup\\find\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\b25\\")
    # scanTorrentsIntoDB("D:\\temp\\0555\\2022-03-01\\0555\\normal\\")

    # genhalfTorrent('D:\\temp\\chachong\\')
    # filterDownFiles(r'D:\temp\b31', r'D:\temp\sp', 'y')
    # writeTorrDetail('D:\\360Downloads\\1228\\')
    os._exit(0)

    #
    path = r'D:\temp\0555\2022-03-01\0555\b43'
    # path=r'D:\temp\b31y'
    # removeFiles(path)
    # truncatetable()
    # scanTorrentsIntoDB(path)

    # removeFiles('f:\\')
    # removeFiles('g:\\')
    # removeFiles('h:\\')

# removeFiles('E:\\PDF\\')
# removeFiles('G:\\CC\\BOOKS\\')

# scanTorrentsIntoDB("C:\\Users\\Administrator\\Downloads\\best\\")

# scanTorrentsIntoDB("D:\\temp\\0555\\t\\0555\\b37\\")
# tormd5("C:\\Users\\Administrator\\Downloads\\best\\推特网红大屁股骚货kbamspbam，怀孕了还能挺着个大肚子拍照拍视频挣钱，太敬业了，奶头变黑 但白虎粉穴依然粉嫩.torrent")
#
# getDulicateFiles()


# getTorrDetail('D:\\360Downloads\\1228\\')
# writeTorrDetail('D:\\temp\\1228\\')
# filterBigfiles('D:\\360Downloads\\test\\', 1000)

# getTorrDetail('D:\\temp\\593254315050521\\1210-best\\1\\')

# getTorrentByDetails('','D:\\temp\\0555\\2022-03-01\\0555\\')

# for i in range(51):
#     dirpath='D:\\temp\\593254315050521\\alltorr\\'+str(i)+os.path.sep+str(i)+'\\y'
#     if(os.path.isdir(dirpath)):
#         # loger.info('D is '+dirpath)
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
