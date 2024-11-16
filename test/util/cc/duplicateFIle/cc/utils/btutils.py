# -*- coding:utf-8 -*-
#!/usr/bin/env python
# import shutil
# import tempfile
# import libtorrent as lt
# from time import sleep
import os.path as pt
import os
import sys
from torrentp import TorrentDownloader
from time import sleep

#magnet 磁力链接
#torrname 种子名称
#output_name 种子保存路径
# def magnet2torrent(magnet,torrname, output_name):
#     if output_name and \
#             not pt.isdir(output_name) and \
#             not pt.isdir(pt.dirname(pt.abspath(output_name))):
#         print("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
#         print("")
#         sys.exit(0)
#     tempdir = tempfile.mkdtemp()
#     ses = lt.session()
#     params = {
#         'save_path': tempdir,
#         'duplicate_is_error': True,
#         'storage_mode': lt.storage_mode_t(2),
#         'paused': False,
#         'auto_managed': True,
#         'duplicate_is_error': True
#     }
#     handle = lt.add_magnet_uri(ses, magnet, params)
#     print("Downloading Metadata (this may take a while)")
#     while (not handle.has_metadata()):
#         try:
#             sleep(1)
#         except KeyboardInterrupt:
#             print("Aborting...")
#             ses.pause()
#             print("Cleanup dir " + tempdir)
#             shutil.rmtree(tempdir)
#             sys.exit(0)
#     ses.pause()
#     print("Done")
#     torinfo = handle.get_torrent_info()
#     torfile = lt.create_torrent(torinfo)
#     # output = pt.abspath(torinfo.name() + ".torrent")
#     if output_name:
#         if pt.isdir(output_name):
#             output = pt.abspath(pt.join(
#                 output_name, torrname + ".torrent"))
#         elif pt.isdir(pt.dirname(pt.abspath(output_name))):
#             output = pt.abspath(output_name)
#     print("Saving torrent file here : " + output + " ...")
#     torcontent = lt.bencode(torfile.generate())
#     f = open(output, "wb")
#     f.write(lt.bencode(torfile.generate()))
#     f.close()
#     print("Saved! Cleaning up dir: " + tempdir)
#     ses.remove_torrent(handle)
#     shutil.rmtree(tempdir)
#     return output
#根据magnet路径下载文件
def downTfileByMagnet(magnetLink,torrpath):
    torrent_file = TorrentDownloader(magnetLink, torrpath)
    torrent_file.start_download()

    # response=requests.get(magnetLink)
    # with open(torrpath,'wb') as file:
    #     file.write(response.content)

def genFileByMagnetLinks():
    map=readfile('magnet.txt')
    if map is not None:
         for (key,val) in map.items():
             print(key+'======>'+val)
             # magnet 磁力链接
             # torrname 种子名称
             # output_name 种子保存路径
             # magnet2torrent(val, key, os.getcwd())
             torrpath=os.getcwd()+'/'+key
             downTfileByMagnet(val,'.')
             sleep(3)
             # magnet2torrent(val, key, '/home/cc/code/python/downtorr/')
def showHelp():
    print("")
    print("USAGE: " + pt.basename(sys.argv[0]) + " MAGNET [OUTPUT]")
    print("  MAGNET\t- the magnet url")
    print("  OUTPUT\t- the output torrent file name")
    print("")

def readfile(fpath):
    fnlist=[]#种子文件名列表
    magnetlist=[]#磁力链接列表
    map={}
    with open(fpath, "r",encoding='utf-8') as f:#,encoding='utf-8'
        lines = f.readlines()
        for line in lines:
            line =str(line).strip()

            if(line !='' and line!='b\'\\r\\n\''):
                if(line.startswith('magnet')):
                    magnetlist.append(line)
                else:
                    fnlist.append(line)
    if(len(fnlist)>0):
        map=dict(zip(fnlist,magnetlist))
    return map



if __name__ == "__main__":
    genFileByMagnetLinks()