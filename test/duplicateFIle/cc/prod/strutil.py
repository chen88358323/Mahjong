# -*- coding: UTF-8 -*-
"""显示目录树状图"""
import time
import logger


# import  logger
    #清理路径中多余的// =>/
def clearpath(p):
    return  eval(repr(p).replace('\\\\', '\\'))\

#计算方法调用的时间
def getDbTime(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        costtime=e_time - s_time
        logger.log.info('数据库方法{}耗时：{}秒'.format(f.__name__, costtime))
        return res

    return inner

def pathsymbol_processing(folder_name):
    """目录名称中的特殊符号处理"""
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result_list = []
    for i in folder_name:
        if i in char_list:
            news_title_result_list.append('')
        else:
            news_title_result_list.append(i)
    news_title_result = ''.join(news_title_result_list)
    # logger.log.info("新的标题名：{}".format(news_title_result))
    return news_title_result


#含有特殊路径的字符打印
# def printPath(pathlist,logger):
#     if pathlist is not None and len(pathlist)>0:
#         for path in pathlist:
#             logger.log.info("原始路径:"+path)
#             logger.log.info("转义路径::"+os.path.normpath(path).replace('\\','/'))
#
#         for path in pathlist:
#             logger.log.info("转义路径::" + pathsymbol_processing(path).replace('\\', '/'))


if __name__ == '__main__':
    pathlist=['zp/【最新❤️性爱流出】漂亮花臂抖M妹妹与男友性爱私拍流出 情趣黑丝爆操丰臀嫩穴 轻虐滴蜡口爆 完美露脸 高清1080P版/V/1 (1).mp4','cc']
    # printPath(pathlist,logger)