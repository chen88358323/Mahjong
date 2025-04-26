from transmission_rpc import Torrent

def parse_torrent_with_transmission_rpc(torrent_file_path):
    """
    使用 transmission_rpc 库解析 .torrent 文件并打印一些基本信息。
    """
    try:
        torrent = Torrent.from_torrent_file(torrent_file_path)
        print(f"文件名: {torrent.name}")
        print(f"Info Hash: {torrent.hashString}")
        print(f"创建者: {torrent.creator}")
        print(f"创建日期: {torrent.dateCreated}")
        print("Tracker URLs:")
        for tracker_tier in torrent.trackers:
            for tracker in tracker_tier:
                print(f"  - {tracker['announce']}")
        print("文件列表:")
        for file in torrent.files:
            print(f"  - {file['name']} ({file['length']} bytes)")
        print(f"总大小: {torrent.totalSize} bytes")
        print(f"私有种子: {torrent.isPrivate}")

    except FileNotFoundError:
        print(f"错误: 文件未找到: {torrent_file_path}")
    except Exception as e:
        print(f"解析 torrent 文件时发生错误: {e}")

if __name__ == "__main__":
    torrent_file = r"/test/util/cc/torrent/read_torr_demo/xx.torrent"  # 将 "your_torrent_file.torrent" 替换为你的文件路径
    parse_torrent_with_transmission_rpc(torrent_file)