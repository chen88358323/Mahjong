import transmission_rpc

# 创建客户端连接
client = transmission_rpc.Client(
    host='localhost',
    port=9091,
    username='cc',
    password='1qaz2wsx'
)

# 添加种子文件并获取元数据
torrent = client.get_torrent('ttt.torrent')
print(f"种子ID: {torrent.id}")
print(f"文件名称: {torrent.name}")  # 输出主文件名:ml-citation{ref="3" data="citationList"}
print(f"哈希值: {torrent.hashString}")  # 获取唯一标识符:ml-citation{ref="3" data="citationList"}
