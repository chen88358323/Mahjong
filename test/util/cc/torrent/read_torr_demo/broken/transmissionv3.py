from transmission_rpc import Torrent

def parse_torrent_with_transmission_rpc_alternative(torrent_file_path):
    """
    尝试使用 transmission_rpc 库解析 .torrent 文件的其他可能方法。
    """
    try:
        torrent = Torrent(torrent_file=torrent_file_path)  # 尝试直接初始化
        print(f"文件名: {torrent.name}")
        print(f"Info Hash: {torrent.hashString}")
        # ... 其他属性访问

    except FileNotFoundError:
        print(f"错误: 文件未找到: {torrent_file_path}")
    except AttributeError as e:
        print(f"属性错误: {e}")
        print("尝试使用 'torrent' 属性访问 torrent 信息...")
        try:
            # 有些版本可能将 torrent 信息放在 'torrent' 属性下
            torrent_info = torrent.torrent
            print(f"文件名: {torrent_info.name}")
            print(f"Info Hash: {torrent_info.hashString}")
            # ... 其他属性访问
        except AttributeError as e2:
            print(f"仍然无法访问 torrent 信息: {e2}")
    except Exception as e:
        print(f"解析 torrent 文件时发生错误: {e}")

if __name__ == "__main__":
    torrent_file = r"/test/util/cc/torrent/read_torr_demo/xxx.torrent"  # 将 "your_torrent_file.torrent" 替换为你的文件路径
    parse_torrent_with_transmission_rpc_alternative(torrent_file)