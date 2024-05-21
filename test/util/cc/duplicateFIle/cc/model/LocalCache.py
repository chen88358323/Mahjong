import datetime
import os,sys
import pickle
from test.util.cc.duplicateFIle.cc.utils import logger,encryutil,dirutil
localCacheName='filescan.cache'

#本地缓存文件  提高多次扫描效率
# def create_snapshot(directory,snapshot):
#     if(snapshot==None or len(snapshot)==0):
#         logger.log.info('路径'+directory+"  无缓存")
#     else:
#
#     """
#     Create a snapshot of the given directory by hashing each file.
#     Returns a dictionary containing file paths as keys and their hashes as values.
#     """
#     for root, _, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_hash,fsize=encryutil.calc_halffile_hash(file_path)
#             snapshot[file_path] = file_hash
#     return snapshot
#根据给定路径计算，然后缓存位置
def save_snapshot(directory,snapshot):
    if (snapshot == None or len(snapshot) == 0):
        logger.log.info('路径' + directory + "  无缓存")
    else:
        cachePath=getCachePath(directory)
        #Save the snapshot to a file using pickle.
        with open(cachePath, 'wb') as f:
            pickle.dump(snapshot, f)
        logger.log.info('路径' + directory + "  保存缓存成功,条数"+str(len(snapshot)))
        snapshot.clear()

#根据给定路径计算缓存位置，并加载
def load_snapshot(path):
    driverpath = dirutil.getDriverPath(path) + localCacheName
    if os.path.isfile(driverpath):  # 缓存文件存在
        #Load a snapshot from a file using pickle.
        with open(driverpath, 'rb') as f:
            snapshot = pickle.load(f)
        return snapshot
    else:
        logger.log.info('缓存文件不存在' + driverpath)
        return None

#根据指定的key列表删除元素
#返回更新后的cache与删除字典列表
def clearCacheByKeyList(cache,klist):
    if klist is None or len(klist)==0:
        return cache,None
    cachep=cache.copy()
    delcache=dict()
    for key in cache.keys():
        if key in klist:
            hcode=cachep.pop(key)
            delcache[key]=hcode
    # logger.log.info('缓存文件' + driverpath)
    return  cachep,delcache


def getCachePath(dirpath):
    driverpath=dirutil.getDriverPath(dirpath)+localCacheName
    return  driverpath

# def cacheExist(dirpath):
#     driverpath = dirutil.getDriverPath(dirpath) + localCacheName
#     if os.path.isfile(driverpath):
#         return  True
#     else:
#         return False




def compare_snapshots(snapshot1, snapshot2):
    """
    Compare two snapshots and return files added and deleted.
    """
    added_files = [file for file in snapshot2 if file not in snapshot1]
    deleted_files = [file for file in snapshot1 if file not in snapshot2]
    return added_files, deleted_files

if __name__ == '__main__':
    # str=getCachePath('D:\\360Download\\仓鼠管家\\')
    # print(str)
    path='D:\\360Download\\仓鼠管家\\'
    cache=load_snapshot(path)
    if cache is not None and len(cache)>0:
        i=0
        for k,v in cache.items():
            i+=1
            print('code '+v)
            print('file ' + k)
    print('sum '+str(i))
    # newcache=cache.copy()
    # newcache.pop(r'D:\360Download\仓鼠管家\曼昆经济学原理中文版_高清pdf.pdf')
    # save_snapshot(path ,newcache)