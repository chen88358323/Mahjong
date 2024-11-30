import os
from torrentool.api import Torrent
import json
import time
import glob
from torrentool.exceptions import BencodeDecodingError

class DownLoadCheck():
    # 功能1: 生成黑名单数据文件
    #filename
    #filetype F 表示文件 D 表示文件夹  FS表示文件列表
    def generate_blacklist(self,seed_path, filename, filetype):
        torrent_info = Torrent.from_file(seed_path)
        file_list = torrent_info.files

        blacklist = set()

        # 遍历torrlist并根据filetype和filename进行过滤和处理
        for torr in file_list:
            # 提取name的最后一部分作为文件/文件夹名
            file_or_dir_name = torr.name.split('\\')[-1]

            # 判断filetype
            if filetype == 'F':
                # 如果是文件类型，并且filename不匹配（因为要排除1.html）
                if file_or_dir_name != filename:
                    # 将最后一部分添加到黑名单列表
                    blacklist.add(file_or_dir_name)
            elif filetype == 'D':
                # 如果是文件夹类型
                # 将name按\\分割成多个部分
                parts = torr.name.split('\\')
                # 检查是否包含指定的文件夹名（但不是顶级文件夹或文件名）
                # 这里我们只查看(1, n-1)部分是否包含指定的文件夹名
                if filename in parts[1:-1]:
                    # 如果包含指定的文件夹名，则跳过该文件（即不将其添加到黑名单中）
                    continue
                # 如果不包含指定的文件夹名，则将最后一部分添加到黑名单中
                blacklist.add(parts[-1])
            elif filetype=='FS':
                if filename in file_or_dir_name:
                    continue
                blacklist.add(file_or_dir_name)

        # 生成以毫秒数命名的黑名单文件
        self.gen_blacklist(blacklist,None)

    #根据数据列表导出blacklist文件，并打印
    def gen_blacklist(self,blacklist,filename):
        blacklist=list(blacklist)
        # 生成以毫秒数命名的黑名单文件
        timestamp = int(time.time() * 1000)
        if filename is not None:
            blacklist_file=filename
        else:
            blacklist_file = f"blacklist_{timestamp}.json"
        with open(blacklist_file, "w", encoding='utf-8') as f:
            json.dump(blacklist, f, ensure_ascii=False, indent=4)

        # 打印黑名单
        print(f"Blacklist generated and saved to {blacklist_file}")
        for item in blacklist:
            print("\""+item+"\",")
    def querystr_in_blacklist(self,str,black_list_path):
        blist=self.load_blacklist(black_list_path)
        if(blist is not None and len(blist)>0):
            if str in blist:
                print("blacklist has "+str)
            else:
                print(str+" not in blacklist  " )
    def load_blacklist(self,blacklist_path):
        with open(blacklist_path, "r", encoding='utf-8') as f:
            blacklist = json.load(f)
            return  blacklist
    def print_blacklist(self,blacklist_path):
        with open(blacklist_path, "r", encoding='utf-8') as f:
            blacklist = json.load(f)
            for content in blacklist:
                print(content)
    # 功能2: 生成下载报告
    def generate_report(self,seed_path, downloaded_dir,blacklist_file):
        torrent_info = Torrent.from_file(seed_path)
        file_list = torrent_info.files

        with open(blacklist_file, "r") as f:
            blacklist = json.load(f)

        downloaded_files = []
        not_downloaded_files = []
        total_files = 0

        for file_item in file_list:
            # 只考虑不在黑名单中的文件
            if file_item.path not in blacklist:
                total_files += 1
                file_path = os.path.join(downloaded_dir, file_item.path)
                if os.path.exists(file_path):
                    downloaded_files.append(file_item.path)
                else:
                    not_downloaded_files.append(file_item.path)

        if total_files == 0:
            print("No files to download after applying blacklist.")
            return

        downloaded_percentage = len(downloaded_files) / total_files * 100

        print(f"Downloaded files percentage: {downloaded_percentage:.2f}%")
        print("Downloaded files:")
        for file in downloaded_files:
            print(file)

        print("Not downloaded files:")
        for file in not_downloaded_files:
            print(file)


    # 功能3: 合并多个黑名单数据文件
    def merge_blacklists(self,folder_path, output_file):
        blacklist_files = glob.glob(os.path.join(folder_path, "blacklist_*.json"))
        merged_blacklist = []

        for file in blacklist_files:

            with open(file, "r", encoding='utf-8') as f:
                blacklist = json.load(f)
                merged_blacklist.extend(blacklist)

        # 去重
        merged_blacklist = list(set(merged_blacklist))

        # 将合并后的黑名单写入文件
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(merged_blacklist, f, ensure_ascii=False, indent=4)

        print(f"Merged blacklist saved to {output_file}")


dlcheck=DownLoadCheck()
if __name__ == '__main__':
    # dlcheck.merge_blacklists(r"D:\CODE\github\mahjong\python-mahjong\test\util\cc\torrent\bl", "bl.json")

# blacklist=dlcheck.load_blacklist(r"merged_blacklist.json")
#torrpath 中文文件目录
# 示
# readtorr(r"D:\temp\112\1 (1).torrent")
    dlcheck.generate_blacklist(r"D:\temp\112\111.torrent", "六月最新極品泄密流出 極品反差婊氣質眼鏡美女王璐璐與研究生男友自拍性愛視頻", "FS")
#     dlcheck.querystr_in_blacklist('JavLand.Link.jpg',r'D:\CODE\github\mahjong\python-mahjong\test\util\cc\torrent\bl.json')
#generate_blacklist(r"D:\temp\112\1 (7).torrent", "mp4", "FS")

# merge_blacklists(r"D:\CODE\github\mahjong\python-mahjong\test\util\cc\torrent\blacklist",
#                 r"merged_blacklist.json")
# print_blacklist(r"merged_blacklist.json")

# 注意：请根据需要取消注释示例调用，并确保正确安装了torrentool库。
