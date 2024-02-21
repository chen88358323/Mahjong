# -*- coding: UTF-8 -*-
"""文件计算唯一标识"""
import hashlib
from test.util.cc.duplicateFIle.utils import logger
import os,time,mmap
# 相关的信息摘要算法
#显示文件单位 300M
bigsize = 300 * 1024 * 1024
big_file_read_size=100 * 1024 * 1024
msize=1 * 1024 * 1024
def mdavMD5( path):
    md5file = open(path, 'rb')
    md5 = hashlib.md5(md5file.read()).hexdigest()
    md5file.close()
    fsize = os.path.getsize(path) / bigsize
    logger.log.info(md5 + '   ' + str(round(fsize, 2)) + 'Mb     ' + path)
    return md5

#计算方法调用的时间
def getMethodTime(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        costtime = e_time - s_time
        print('方法{}耗时：{}秒'.format(f.__name__,costtime))
        return res

    return inner


# 相关的信息摘要算法  高性能
@getMethodTime
def mdavMD5HighPerform( path):
    with open(path, 'rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            md5_hasher = hashlib.md5(mmapped_file)
            md5 = md5_hasher.hexdigest()
            fsize = os.path.getsize(path) / bigsize
            logger.log.info(md5 + '   ' + str(round(fsize, 2)) + 'Mb     ' + path)
            return md5



    return md5_hasher.hexdigest()
@getMethodTime
def calc_file_hash(filename):
    size=os.path.getsize(filename)
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
                logger.log.info(hcode + '   ' + str(round(size / msize, 2)) + 'Mb     ' + filename)
                return md5hasher.hexdigest()
    else:
        with open(filename, 'rb') as f:
         #偏移量，大于300M的文件，读取前100M以及最后面的100M
            md5hasher.update(f.read(big_file_read_size))
            f.seek(size - big_file_read_size)
            md5hasher.update(f.read(big_file_read_size))
            hcode = md5hasher.hexdigest()
            logger.log.info(hcode + '   ' + str(round(size / msize, 2)) + 'Mb     ' + filename)
            return hcode
@getMethodTime
def calculate_md5_high_performance(file_path):
    md5_hasher = hashlib.md5()
    with open(file_path, 'rb', buffering=0) as file:
        for chunk in iter(lambda: file.read(8192), b''):
            md5_hasher.update(chunk)
    return md5_hasher.hexdigest()


def mdavSHA1( path):
    sha1file = open(path, 'rb')
    sha1 = hashlib.sha1(sha1file.read()).hexdigest()
    sha1file.close()
    logger.log.info(sha1)
    return sha1


def mdavSHA128( path):
    sha1file = open(path, 'rb')
    sha128 = hashlib.shake_128(sha1file.read()).hexdigest()
    sha1file.close()
    logger.log.info(sha128)
    return sha128


def _mdavSHA256( path):
    sha1file = open(path, 'rb')
    sha256 = hashlib.sha_256(sha1file.read()).hexdigest()
    sha1file.close()
    logger.log.info(sha256)
    return sha256


def mdavSHA512( path):
    sha512file = open(path, 'rb')
    sha512 = hashlib.sha512(sha512file.read()).hexdigest()
    sha512file.close()
    logger.log.info(sha512)
    return sha512

