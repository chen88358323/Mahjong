# -*- coding: UTF-8 -*-
"""显示目录树状图"""
import time
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
        print('方法{}耗时：{}秒'.format(f.__name__,costtime))
        return res

    return inner