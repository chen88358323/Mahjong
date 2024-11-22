# 假设TorrentFile是一个具有name和length属性的类
from torrentool.api import Torrent
class TorrentFile:
    def __init__(self, name, length):
        self.name = name
        self.length = length


# 假设torrlist是TorrentFile对象的列表
torrlist = [
    TorrentFile(name='AA\\102\\1021版\\_1024社区_最新网址.html', length=1359319),
    TorrentFile(name='AA\\102\\1021版\\_1024社区备用网址.html', length=1355836),
    # ... (其他TorrentFile对象)
    TorrentFile(name='AA\\233\\233.jpg', length=169081),
    TorrentFile(name='AA\\233\\234.url', length=126),
    # ... (其他TorrentFile对象)
    TorrentFile(name='AA\\233vzzfgg\\233vzzfgg.url', length=124),
    # ... (其他TorrentFile对象)
]

# 假设filename和filetype是给定的参数
filename = '1.html'  # 示例值，可以根据实际情况修改
filetype = 'F'  # 'F'表示文件，'D'表示文件夹

# 初始化黑名单列表
blacklist = []
torrent_info = Torrent.from_file('')
file_list = torrent_info.files
# 遍历torrlist并根据filetype和filename进行过滤和处理
for torr in torrlist:
    # 提取name的最后一部分作为文件/文件夹名
    file_or_dir_name = torr.name.split('\\')[-1]

    # 判断filetype
    if filetype == 'F':
        # 如果是文件类型，并且filename不匹配（因为要排除1.html）
        if file_or_dir_name != filename:
            # 将最后一部分添加到黑名单列表
            blacklist.append(file_or_dir_name)
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
        blacklist.append(file_or_dir_name)

# 打印黑名单列表
print(blacklist)
