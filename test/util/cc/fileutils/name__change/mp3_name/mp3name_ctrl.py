import os
import re
import shutil

def process_mp3_files(root_dir):
    """
    处理指定目录下的 MP3 文件。

    Args:
        root_dir (str): 包含 MP3 文件的根目录。
    """

    origin_dir = os.path.join(root_dir, "origin")
    convert_dir = os.path.join(root_dir, "convert")

    # 创建目标文件夹（如果不存在）
    os.makedirs(origin_dir, exist_ok=True)
    os.makedirs(convert_dir, exist_ok=True)

    all_mp3_files = [f for f in os.listdir(root_dir) if f.endswith(".mp3")]
    print(f"1. 目录 {root_dir} 下的 MP3 文件数量: {len(all_mp3_files)}")

    processed_count = 0
    for filename in list(all_mp3_files):  # 使用 list 创建副本，避免在迭代时修改列表
        if "-" in filename:
            parts = filename.replace(".mp3", "").split("-")
            if len(parts) == 2 and parts[1].isdigit():
                # 符合条件的文件
                new_filename = f"{parts[1]}-{parts[0]}.mp3"
                old_path = os.path.join(root_dir, filename)
                new_path = os.path.join(convert_dir, new_filename)
                shutil.move(old_path, new_path)
                processed_count += 1
                all_mp3_files.remove(filename) # 从原始列表中移除已处理的文件
            else:
                # 不符合条件的文件，移动到 origin 文件夹
                old_path = os.path.join(root_dir, filename)
                new_path = os.path.join(origin_dir, filename)
                shutil.move(old_path, new_path)
                all_mp3_files.remove(filename) # 从原始列表中移除已处理的文件
        else:
            # 不带 "-" 的文件，移动到 origin 文件夹
            old_path = os.path.join(root_dir, filename)
            new_path = os.path.join(origin_dir, filename)
            shutil.move(old_path, new_path)
            all_mp3_files.remove(filename) # 从原始列表中移除已处理的文件

    origin_file_count = len([f for f in os.listdir(origin_dir) if f.endswith(".mp3")])
    convert_file_count = len([f for f in os.listdir(convert_dir) if f.endswith(".mp3")])

    print(f"4. 目录 {origin_dir} 下的 MP3 文件数量: {origin_file_count}")
    print(f"4. 目录 {convert_dir} 下的 MP3 文件数量: {convert_file_count}")

if __name__ == "__main__":
    root_directory = r"D:\DOC\person\官司\吴为民案件\证据\录音整理\互传"  # 替换为你的实际目录
    process_mp3_files(root_directory)