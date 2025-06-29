import logging
import os
def initlog():
    # 创建一个logger
    log = logging.getLogger('torr')
    log.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('torrscan.log', encoding='utf-8')
    fh.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    log.addHandler(fh)
    log.addHandler(ch)
    return log
log=initlog()
def file_writer(filepath, name,append):
    mkdirs(filepath)
    dirname = os.path.dirname(filepath)
    # 文件夹最后一层名称
    basename = os.path.split(dirname)[-1]

    log.info('basename==>' + basename)
    log.info('dirname==>' + dirname)
    txtpath = filepath +os.path.sep+ basename + name + '.txt'
    log.info('txtfile===>' + txtpath)
    if(append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile
#filepath
#filename
#append 文件是否追加，True追加，False覆盖
def file_writer_straght(filepath, filename,append):
    mkdirs(filepath)
    # 文件夹最后一层名称
    txtpath = filepath +os.path.sep+ filename + '.txt'
    log.info('txtfile===>' + txtpath)
    if(append):
        txtfile = open(txtpath, 'a', encoding='utf-8')
    else:
        txtfile = open(txtpath, 'w', encoding='utf-8')
    return txtfile
def mkdirs(path):
    if (not os.path.exists(path)):
        log.info('mkdir:' + str(path))
        os.mkdir(path)
