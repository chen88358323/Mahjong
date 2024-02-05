# -*- coding: UTF-8 -*-
"""显示目录树状图"""

    #清理路径中多余的// =>/
def clearpath(p):
    return  eval(repr(p).replace('\\\\', '\\'))