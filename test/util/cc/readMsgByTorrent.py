from torrentool.api import Torrent
import os


def removeFiles():
    filepath = 'D:\\temp\\593254315050521\\demo\\'
    array=['【01axg.xyz】.jpg','02AXG.XYZ.png','03axg.XYZ.png','04axg.xyz.png','05axg.xyz.png']
    prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            if filename in array:
                absPath = dirpath +"\\"+ filename
                print(absPath)
                os.remove(absPath)
            # torr = os.path.join(dirpath, filename)
            # absPath = dirpath + filename
            # if(absPath.endswith(prefix)):
            #     print(absPath)

def getDulicateFiles():
    filepath = 'D:\\temp\\593254315050521\\'
    prefix='(1).jpg'
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            absPath = dirpath + filename
            if(absPath.endswith(prefix)):
                print(absPath)


def getTorrDetail(filepath):

    print('path===>'+filepath)
    len=1024*1024
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            torr = os.path.join(dirpath, filename)
            portion = os.path.splitext(filename)
            print(portion)
            # 如果后缀是.xltd
            if portion[1] == ".xltd":
                print("need change")
                newnamee=portion[0].replace('.bt','')
                os.renames(filepath+portion[0]+portion[1],filepath+newnamee)
            if portion[1] == ".torrent":
                print(torr)
                my_torrent = Torrent.from_file(torr)
                print(my_torrent.total_size / len)
                # print(my_torrent.comment)
                print(portion[0]  +'          '+ my_torrent.name)
                for torrfile in my_torrent.files:
                    if(torrfile.length>100*len):
                        print(torrfile)
                # filesor tf in list[my_torrent.files]:

if __name__ == '__main__':
    # getDulicateFiles()
    #getTorrDetail('D:\\temp\\best\\')
    # getTorrDetail('D:\\temp\\1011\\')
    getTorrDetail('D:\\temp\\593254315050521\\16\\')

    # removeFiles()



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
    #         webbrowser.open(urk)
