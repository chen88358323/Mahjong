from torrentool.api import Torrent
from torrentool.api import TorrentFile
from torrentool.exceptions import BencodeDecodingError
import os
import  shutil
import mysqlTemplate as dbtool
import  readMsgByTorrent as torrimpl
import time,copy
import queue,threading
import sys
from typing import Any, Tuple
import loggerTemplate


loger=loggerTemplate.log
def testget_torrdetail(path):
    torrimpl.getTorrDetail(path)
# def test():
#     list1=[[1,2,3],[45,6,7],[8,65,44]]
#     list2=[2,33,44,55,66]
#     for l in list1:
#         if l[1] in list2:
#             list1.remove(l)
#     loger.info("list1"+str(list1))
if __name__ == '__main__':
    testget_torrdetail(r'D:\temp\b31\3')
